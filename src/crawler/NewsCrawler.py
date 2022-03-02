from selenium import webdriver as wd
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import os
import re
import requests

import numpy as np
import pandas as pd
import urllib
import time
from datetime import datetime
from tqdm import tqdm

from konlpy.tag import Kkma
from konlpy.tag import Okt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import normalize


def set_chrome_driver() :
    chrome_options = wd.ChromeOptions()
    driver = wd.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver


# 기사 본문, 키워드 끌어오는 함수 (네이버 뉴스 링크가 있어야만 가능)
def get_article_contents(nlink_list) :

    headers = {
        'referer' : 'https://www.naver.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }

    content_list = []
    keyword_list = []

    for naver_article_link in nlink_list :
        if naver_article_link == "" :
            content_list.append("")
            keyword_list.append("")
            continue

        orig_html = requests.get(naver_article_link, headers=headers)
        html = BeautifulSoup(orig_html.text, "html.parser")

        try :
            content = html.find('div',{'id' : 'articleBodyContents'}).text
            content = re.sub('\xa0|\t|\r|\n|', '', content)
            textrank = TextRank(content)
            
            content_list.append(content)
            keyword_list.append(textrank.keywords())


        except Exception as e :
            try :
                content = html.find('div',{'id' : 'articeBody'}).text
                content = re.sub('\xa0|\t|\r|\n|', '', content)
                textrank = TextRank(content)
                
                content_list.append(content)
                keyword_list.append(textrank.keywords())

            except Exception as e :
                content = html.find('div', {'id' : 'newsEndContents'}).text
                content = re.sub('\xa0|\t|\r|\n|', '', content)
                textrank = TextRank(content)

                content_list.append(content)
                keyword_list.append(textrank.keywords())
                
    return content_list, keyword_list



def get_article_infos(driver, crawl_date, press_list, title_list, link_list, nlink_list, date_list, more_news_base_url=None, more_news=False) :

    headers = {
        'referer' : 'https://www.naver.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }

    more_news_url_list = []
    
    while True :
        html_src = driver.page_source # driver.page_source 크롬 개발자 도구의 Element 탭 내용과 동일
        soup = BeautifulSoup(html_src, 'lxml')

        
        # 관련뉴스
        more_news_infos = soup.select('a.news_more')
        
        if more_news :
            for more_news_info in more_news_infos:
                more_news_url = f"{more_news_base_url}{more_news_info.get('href')}"
                more_news_url_list.append(more_news_url)
                
        article_infos = soup.select("div.news_area")

        if not article_infos :
            break

        for article_info in article_infos :
            # 언론사명
            press_info = article_info.select_one("div.info_group > a.info.press")

            if press_info is None :
                press_info = article_info.select_one("div.info_group > span.info.press")
                
            press = press_info.text.replace("언론사 선정", "")
            press_list.append(press)

            # 기사 제목
            article = article_info.select_one("a.news_tit")           
            title = article.get('title')
            title_list.append(title)

            # 기사 링크
            link = article.get('href')
            link_list.append(link)

            # 네이버 기사 링크 (없으면 공란 처리)
            naver_article = article_info.select_one("div.info_group > a:nth-child(3)")

            if not naver_article :
                naver_article_link = ""
            else :
                naver_article_link = naver_article["href"]

            nlink_list.append(naver_article_link)
            
            # 날짜
            date_list.append(crawl_date)

        time.sleep(2.0)
        next_btn_status = soup.select_one("a.btn_next").get("aria-disabled")

        if next_btn_status == 'true' :
            break

        time.sleep(1.0)
        next_page_btn = driver.find_element_by_css_selector("a.btn_next").click()

    return press_list, title_list, link_list, nlink_list, more_news_url_list



def get_news_infos(keyword, save_path, target_date, ds_de, sort=0, remove_duplicate=False) :
    crawl_date = f"{target_date[:4]}.{target_date[4:6]}.{target_date[6:]}" # target_date 자르기 ex. 20220301 => 2022.03.01
    driver = set_chrome_driver()

    encoded_keyword = urllib.parse.quote(keyword)
    url = f"https://search.naver.com/search.naver?where=news&query={encoded_keyword}&sm=tab_opt&sort={sort}&photo=0&field=0&pd=3&ds={ds_de}&de={ds_de}&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Ar%2Cp%3Afrom{target_date}to{target_date}&is_sug_officeid=0"
    more_news_base_url = "https://search.naver.com/search.naver"
    
    driver.get(url)

    press_list, title_list, link_list, nlink_list, content_list, keyword_list, date_list, more_news_url_list = [], [], [], [], [], [], [], []

    press_list, title_list, link_list, nlink_list, more_news_url_list = get_article_infos(driver=driver,
                                                                                         crawl_date=crawl_date,
                                                                                         press_list=press_list,
                                                                                         title_list=title_list,
                                                                                         link_list=link_list,
                                                                                         nlink_list=nlink_list,
                                                                                         date_list=date_list,
                                                                                         more_news_base_url=more_news_base_url,
                                                                                         more_news=True)

    content_list, keyword_list = get_article_contents(nlink_list)

    driver.close()

    if len(more_news_url_list) > 0:
        more_news_url_list = list(set(more_news_url_list))
        for more_news_url in more_news_url_list:
            driver = set_chrome_driver()
            driver.get(more_news_url)
            
            press_list, title_list, link_list, nlink_list, more_news_url_list = get_article_infos(driver=driver,
                                                                                                 crawl_date=crawl_date,
                                                                                                 press_list=press_list,
                                                                                                 title_list=title_list,
                                                                                                 link_list=link_list,
                                                                                                 nlink_list=nlink_list,
                                                                                                 date_list=date_list)

            content_list, keyword_list = get_article_contents(nlink_list)
                      
            driver.close()

    article_df = pd.DataFrame({"날짜": date_list, "언론사": press_list, "제목": title_list, "링크": link_list, "네이버 기사 링크":nlink_list, "본문":content_list, "키워드":keyword_list})
    
                              
    print(f"크롤링한 뉴스 기사 수 : {len(article_df)}")
    if remove_duplicate:
        article_df = article_df.drop_duplicates(['링크'], keep='first')
        print(f"after remove duplicate -> {len(article_df)}")

    article_df.to_excel(save_path, index=False)



def crawl_news_data(keyword, year, month, start_day, end_day, save_path):
    year = int(year)
    month = int(month)
    start_day = int(start_day)
    end_day = int(end_day)
    
    for day in tqdm(range(start_day, end_day+1)):
        date_time_obj = datetime(year=year, month=month, day=day)
        target_date = date_time_obj.strftime("%Y%m%d") #strftime 날짜/시간을 스트링으로 변환
        ds_de = date_time_obj.strftime("%Y.%m.%d")

        get_news_infos(keyword=keyword, save_path=f"{save_path}/{keyword}/{target_date}_{keyword}_.xlsx", target_date=target_date, ds_de=ds_de, remove_duplicate=False)



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


if __name__ == "__main__" :

    keyword = input("키워드 입력 : ")
    print("뉴스 검색할 날짜 입력 (YYYYMMDD 형태로)")
    start_date = input("검색 시작일 : ")
    end_date = input("검색 종료일 : ")
    year = start_date[:4]
    month = start_date[4:6]
    start_day = start_date[6:]
    end_day = end_date[6:]
    save_path = "./crawling_result"

    os.makedirs(f"{save_path}/{keyword}")

    print("크롤링 시작")
    crawl_news_data(keyword=keyword, year=year, month=month, start_day=start_day, end_day=end_day, save_path=save_path)