import numpy as np
from konlpy.tag import Kkma
from konlpy.tag import Okt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import normalize

class SentenceTokenizer(object) :
    def __init__(self) :
        #형태소 분석기
        self.kkma = Kkma()
        self.okt = Okt()
        #불용어
        self.stop_words_list = ["머니투데이", "이데일리" , "연합뉴스", "데일리", "동아일보", "중앙일보", "조선일보", "YTN", "News1", "기자", "특파원", "아", "어",
             "나", "우리", "저희", "따라", "의해", "을", "를", "에", "의", "가", "이", "있", "하", "것", "들", "그", "되", "수", "보", "않", "없", "사람", "주", "아니", "등", 
             "같", "때", "년", "한", "지", "대하", "오", "말", "일", "그렇", "위해", "때문", "그것", "두", "말하", "알", "그러나", "받", "못하", "일", "그런", "또", "문제", "더",
             "많", "그리고", "좋", "크", "따르", "중", "나오", "가지", "씨", "시키", "만들", "지금", "생각하", "그러", "속", "하나", "집", "살", "모르", "적", "월", "데", "자신",
             "안", "어떤", "내", "경우", "생각", "시간", "그녀", "다시", "이런", "앞", "보이", "번", "다른", "어떻", "개", "전", "들", "사실", "이렇", "점", "싶", "말", "정도",
             "좀", "원", "잘", "통하", "소리", "놓", "비추어", "형식으로", "의해서", "만큼", "즉", "인하여", "까닭으로", "오늘", "내일", "모레", "뉴스", "지난"]

    def text2sentences(self, text) :
        #문장 분리하여 리스트 생성
        sentences = self.kkma.sentences(text)
        #길이에 따라 문장 합치기
        for idx in range(0, len(sentences)):  
            if len(sentences[idx]) <= 10:
                sentences[idx-1] += (' ' + sentences[idx])
                sentences[idx] = ''
                
        return sentences

    #명사 추출
    def get_nouns(self, sentences) :
        nouns = []
        for s in sentences :
            if s != '':
                nouns.append(' '.join([noun for noun in self.okt.nouns(str(s))
                                      if noun not in self.stop_words_list and len(noun) > 1]))
                
        return nouns

class GraphMatrix(object) :
    def __init__(self) :
        self.cnt_vec = CountVectorizer() #단어 출현 빈도로 문서 벡터화
        self.graph_sentence = []
    
    def build_words_graph(self, sentence) :
        #명사로 이루어진 문장 입력 받고 matrix 생성 후 word graph와 {idx : word} 형태의 dic 리턴
        cnt_vec_mat = normalize(self.cnt_vec.fit_transform(sentence).toarray().astype(float), axis=0)
        vocab = self.cnt_vec.vocabulary_
        
        return np.dot(cnt_vec_mat.T, cnt_vec_mat), {vocab[word] : word for word in vocab}

class Rank(object):
    def get_ranks(self, graph, d=0.85) : #d = damping factor
        A = graph
        matrix_size = A.shape[0]
        for id in range(matrix_size):
            A[id, id] = 0 #대각선 부분 0으로
            link_sum = np.sum(A[:,id])
            if link_sum != 0:
                A[:, id] /= link_sum
            A[:, id] *= -d
            A[id, id] = 1

        B = (1-d) * np.ones((matrix_size, 1))
        ranks = np.linalg.solve(A, B) #연립방정식 Ax = b
        
        return {idx: r[0] for idx, r in enumerate(ranks)}

class TextRank(object) :
    def __init__(self, text) :
        self.st = SentenceTokenizer()

        self.sentences = self.st.text2sentences(text)

        self.nouns = self.st.get_nouns(self.sentences)

        self.graph_matrix = GraphMatrix()
        self.words_graph, self.idx2word = self.graph_matrix.build_words_graph(self.nouns)

        self.rank = Rank()

        self.word_rank_idx = self.rank.get_ranks(self.words_graph)
        self.sorted_word_rank_idx = sorted(self.word_rank_idx, key=lambda k: self.word_rank_idx[k], reverse=True)

    def keywords(self, word_num=5):
        rank = Rank()
        rank_idx = rank.get_ranks(self.words_graph)
        sorted_rank_idx = sorted(rank_idx, key=lambda k: rank_idx[k], reverse=True)
        
        keywords = []
        index=[]
        
        for idx in sorted_rank_idx[:word_num]:
            index.append(idx)
        
        index.sort()
        for idx in index:
            keywords.append(self.idx2word[idx])
        
        return keywords