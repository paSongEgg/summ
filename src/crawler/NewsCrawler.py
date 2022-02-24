import requests
import re
from bs4 import BeautifulSoup
from konlpy.tag import Kkma
from konlpy.tag import Okt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import normalize
import numpy as np


def get_href(soup, option) :
    result = []

    if "날짜" in option : 
        div = soup.find('div', { 'class' : 'list_body newsflash_body'})

        for dt in div.find_all('dt', {'class' : 'photo'}) :
            result.append(dt.find('a')['href'])

    elif "키워드" in option :
        try :
            ul_list = soup.find('ul', {'class' : 'list_news'})
            li_list = ul_list.find_all('li', {'id' : re.compile('sp_nws.*')})
            area_list = [li.find('div', {'class' : 'news_area'}) for li in li_list]
            info_list = [area.find('div', {'class' : 'news_info'}) for area in area_list]
            group_list = [info.find('div', {'class' : 'info_group'}) for info in info_list]
            a_list = []
            
            for group in group_list :
                a = group.find('a', {'class' : 'info'})
                a2 = a.next_sibling.next_sibling
                a_list.append(a2)

            for al in a_list :
                al = al.get('href')
                result.append(al)

        except AttributeError as e :
            print("e")

    return result

def get_request_ds(date, section) :
    headers = {
        'referer' : 'https://www.naver.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }

    url = "https://news.naver.com/main/list.nhn"

    sections = { "정치" : 100, "경제" : 101, "사회" : 102, "생활문화" : 103, "세계" : 104, "IT과학" : 105}
    req = requests.get(url, headers = headers, params = { "date" : date, "sid1" : sections[section]})
    
    return req

def get_request_sp(search, period) :
    
        headers = {
        'referer' : 'https://www.naver.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }

        pds = { "1" : 7, "2" : 8, "3" : 9, "4" : 10, "5" : 11, "6" : 12}

        url = "https://search.naver.com/search.naver?"
        req = requests.get(url, headers = headers, params = { "where" : "news", "sm" : "tab_opt", "sort" : "0", "query" : search, "pd" : pds[period]})

        return req

def crawling_news(soup) :
    dic = {}
    #제목
    try : 
        title = soup.find('div', {'class' : 'article_info'}).find('h3').string
    except AttributeError :
        title = soup.find('div', {'class' : 'end_ct_area'}).find('h2').string
    except Exception as e :
        print("에러 발생")

    title = re.sub('\t|\r|\n| ', '', title)
    
    #본문
    try :
        content = soup.find('div',{'id' : 'articleBodyContents'}).text
    except AttributeError :
        content = soup.find('div',{'id' : 'articeBody'}).text
    except Exception as e :
        print("에러 발생")
        
    content = re.sub('\xa0|\t|\r|\n|', '', content)

    return {'title' : title, 'content' : content}


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
            A[id, id] = 0 ##대각행렬 원소 1을 0으로 치환
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


def main(date, section) :
    headers = {
        'referer' : 'https://www.naver.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }
        
    href_list = []
    news_content = {}
    i = 0

    option = input("날짜 검색 or 키워드 검색 : ")

    if "날짜" in option :
        date = input("날짜 검색 (ex.YYYYMMDD) : ")
        section = input("검색할 섹션 선택 (정치 / 경제 / 사회 / 생활문화 / 세계 / IT과학) : ")
        req = get_request_ds(date, section)
        soup = BeautifulSoup(req.text, "html.parser")

        href_list = get_href(soup, option)

        for href in href_list :
            if(href is None) :
                continue
            href_req = requests.get(href, headers = headers)
            href_soup = BeautifulSoup(href_req.text, "html.parser")
            news_content[i] = {'title' : crawling_news(href_soup).get('title'), 'content' : crawling_news(href_soup).get('content')}

        
    elif "키워드" in option :
        search = input("검색할 키워드 : ")
        period= input("최근 몇 시간 동안의 뉴스를 검색하시겠습니까? (1~6) : ")

        req = get_request_sp(search, period)
        soup = BeautifulSoup(req.text, 'html.parser')

        href_list = get_href(soup, option)

        for href in href_list :
            if(href is None) :
                continue
            href_req = requests.get(href, headers = headers)
            href_soup = BeautifulSoup(href_req.text, 'html.parser')
            news_content[i] = {'title' : crawling_news(href_soup).get('title'), 'content' : crawling_news(href_soup).get('content')}
            
    print(len(news_content), "개의 기사가 검색됨.")
    print()

    for idx in range(0, len(href_list)) :
        print("링크 : ")
        print(href_list[idx])
        print()
        print("제목 : ")
        print(news_content[idx]['title'])
        print("본문 : ")
        print(news_content[idx]['content'])
        print()

        textrank = TextRank(news_content[idx]['title'] + " " + news_content[idx]['content'])
        print(" 키워드 : ", textrank.keywords())
        print("\n\n\n")
        

if __name__ == "__main__" :
    main()