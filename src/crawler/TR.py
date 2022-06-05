import numpy as np
from eunjeon import Mecab
from kiwipiepy import Kiwi
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import normalize

class SentenceTokenizer(object) :
    def __init__(self) :
        self.mecab = Mecab()
        self.kiwi = Kiwi()
        self.stop_words_list = ["아", "어", "나", "우리", "저희", "따라", "의해", "을", "를", "에", "의", "가", "으로", "로", "의거", "근거", "입각", "기준", "저", "다른", "물론", "또한", "그리고", "그러나", "그런데",
                                "등", "등등", "얼마간", "약간", "다소", "좀", "조금", "다수", "몇", "얼마", "각", "각각", "여러분", "각종", "각자", "제각기", 
                                "왜", "어느때", "언제", "야","및", "몇", "거의", "이젠", "만큼", "좀", "다시", "이상", "함께", "양자", "모두", "다른", "매", "매번", "들", "모", "어느것", "어느", "어디",  "어느", "어느쪽", "어느것", "어느해", "어느 년도", 
                                "어느 것", "저기", "저쪽", "저것", "그럼", "그래", "그때", "그저", "할", "줄", "너", "너희", "당신", "그", "다음", "버금", "두 번째", "기타", "첫 번째", "나머지",
                                "단지", "반대로", "전후", "전자", "앞의 것", "남들", "예컨대", "어떻게", "만약", "만일", "잠시", "잠깐", "시각", "무렵", "시간", 
                                "네", "예", "우선", "누구", "누가", "아무도", "그", "너희", "그들", "너희들", "타인", "것", "것들", "너", "여부", "운운", "우리들", "이쪽", "여기", "이것", "이번", 
                                "여러분", "후", "혼자", "자기", "자신", "참", "봐", "아니", "년", "월", "일", "영", "일", "이", "삼", "사", "오", "육", "륙", "칠", "팔", "구", "하나", "둘", "셋", "넷", "다섯", "여섯", "일곱", "여덟", "아홉", "있", "하", "것", "들", 
                                "영", "일", "이", "삼", "사", "오", "육", "륙", "칠", "팔", "구", "하나", "둘", "셋", "넷", "다섯", "여섯", "일곱", "여덟", "아홉", "있", "하", "것", "들", "그", "되", "수", "이", "보", "않", "없", "나", "사람", "주", "아니", "같",
                                "때", "가", "한", "지", "대하", "오", "말", "일", "때문", "그것", "일", "문제", "더", "사회", "중", "씨", "지금", "속", "하나", "집", "살", "적", "월", "데", "자신", "안", "내", "경우", "명", "생각", "시간", "그녀", "다시",
                                "지금", "속", "하나", "집", "살", "적", "월", "데", "앞", "번", "나", "개", "전", "들", "사실", "점", "싶", "말", "정도", "좀", "원", "잘", "오늘", "내일", "모레",
                                "경향신문", "국민일보", "동아일보" , "서울신문", "조선일보", "중앙일보", "한겨레", "한국일보", "JTBC", "KBS", "MBC", "SBS", "YTN", "연합뉴스", "매일경제", "서울경제", "아시아경제", "한국경제", "헤럴드경제",
                                "기자", "특파원", "앵커", "뉴스", "후보", "사례", "원인", "언급", "해결", "감안", "해당", "안팎", "이날", "관련", "가능", "직후", "최소한", "이게", "모습", "최근"]


    def text2sentences(self, text) :
        sents = self.kiwi.split_into_sents(text)
        sentences = []
        for i in range(len(sents)) :
            sentences.append(sents[i][0])
        
        return sentences

    def get_nouns(self, sentences) :
        nouns = []
        for s in sentences :   
            if s != '':
                nouns.append(' '.join([noun for noun in self.mecab.nouns(str(s))
                                      if noun not in self.stop_words_list and len(noun) > 1]))
                
        return nouns


class GraphMatrix(object) :

    def __init__(self) :
        self.cnt_vec = CountVectorizer()
        self.graph_sentence = []

    def build_words_graph(self, sentence) :
        cnt_vec_mat = normalize(self.cnt_vec.fit_transform(sentence).toarray().astype(float), axis=0)
        vocab = self.cnt_vec.vocabulary_

        return np.dot(cnt_vec_mat.T, cnt_vec_mat), {vocab[word] : word for word in vocab}


class Rank(object) :

    def get_ranks(self, graph, d=0.85) :
        A = graph
        matrix_size = A.shape[0]
        for id in range(matrix_size):
            A[id, id] = 0
            link_sum = np.sum(A[:,id])
            if link_sum != 0:
                A[:, id] /= link_sum
            A[:, id] *= -d
            A[id, id] = 1

        B = (1-d) * np.ones((matrix_size, 1))
        ranks = np.linalg.solve(A, B)
        
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
        sorted_word_rank_idx = sorted(rank_idx, key=lambda k: rank_idx[k], reverse=True)

        keywords = {}
        index=[]

        for idx in sorted_word_rank_idx[:word_num]:
            index.append(idx)
        
        for idx in index:
            keywords[self.idx2word[idx]] = f"{rank_idx[idx]:.3f}"
            
        return keywords