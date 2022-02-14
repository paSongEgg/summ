import requests
import re
from bs4 import BeautifulSoup
from konlpy.tag import Kkma
from konlpy.tag import Okt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import normalize
import numpy as np


def get_href(soup) :
    result = []
    div = soup.find("div", class_="list_body newsflash_body")

    for dt in div.find_all("dt", class_="photo") :
        result.append(dt.find("a")["href"])

    return result

def get_request(date, section) :
    headers = {
        'referer' : 'https://www.naver.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }

    url = "https://news.naver.com/main/list.nhn"

    sections = { "정치" : 100, "경제" : 101, "사회" : 102, "생활문화" : 103, "세계" : 104, "IT과학" : 105}
    req = requests.get(url, headers = headers, params = { "date" : date, "sid1" : sections[section]})
    
    return req

def crawling_news(soup) :
    #제목
    title = soup.find("div", "article_info").find("h3").string
    title = re.sub('\t|\r|\n| ', '', title)
    #본문
    content = soup.find("div","_article_body_contents").text
    content = re.sub('\xa0|\t|\r|\n|', '', content)
    
    return title + content


class SentenceTokenizer(object) :
    def __init__(self) :
        #형태소 분석기
        self.kkma = Kkma()
        self.okt = Okt()
        #불용어
        self.stopwords = ["연합뉴스", "데일리", "동아일보", "중앙일보", "조선일보", "YTN", "News1", "기자", "따라", "의해", "을", "를", "에", "의", "가"]

    
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
                                      if noun not in self.stopwords and len(noun) > 1]))
                
        return nouns


class GraphMatrix(object) :
    def __init__(self) :
        self.cnt_vec = CountVectorizer()
    
    def build_words_graph(self, sentence) :
        #명사로 이루어진 문장 입력 받고 matrix 생성 후 word graph와 {idx : word} 형태의 dic 리턴
        cnt_vec_mat = normalize(self.cnt_vec.fit_transform(sentence).toarray().astype(float), axis=0)
        vocab = self.cnt_vec.vocabulary_
        
        return np.dot(cnt_vec_mat.T, cnt_vec_mat), {vocab[word] : word for word in vocab}


class Rank(object):
    #Text Rank
    def get_ranks(self, graph, d=0.85) : #d = damping factor
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
        sorted_rank_idx = sorted(rank_idx, key=lambda k: rank_idx[k], reverse=True)
        
        keywords = []
        index=[]
        
        for idx in sorted_rank_idx[:word_num]:
            index.append(idx)
        
        index.sort()
        for idx in index:
            keywords.append(self.idx2word[idx])
        
        return keywords


def main() :
    headers = {
        'referer' : 'https://www.naver.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }
        
    href_list = []
    news_content = []

    date = input("날짜 검색 (ex.YYYYMMDD) : ")
    section = input("검색할 섹션 선택 (정치 / 경제 / 사회 / 생활문화 / 세계 / IT과학) : ")
    req = get_request(date, section)
    soup = BeautifulSoup(req.text, "html.parser")

    href_list = get_href(soup)

    for href in href_list :
        href_req = requests.get(href, headers = headers)
        href_soup = BeautifulSoup(href_req.text, "html.parser")
        news_content.append(crawling_news(href_soup))

    print()
    print(len(news_content), "개의 기사가 검색됨.")
    print()

    for i in range(len(news_content)) :
    #본문 가져오기

        print("뉴스 기사 링크 >\n")
        print(href_list[i])
        print()
        print("뉴스 기사 본문 >\n")
        print(news_content[i])
        print()

        textrank = TextRank(news_content[i])
        print(" 키워드 > ", textrank.keywords())
        print("\n\n\n")

        

if __name__ == "__main__" :
    main()