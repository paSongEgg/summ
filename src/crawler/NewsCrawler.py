from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import os
import re
import requests
import json

import numpy as np
import pandas as pd
import urllib
import time
from datetime import datetime, timedelta
from tqdm import tqdm

from TR import TextRank

import math

from eunjeon import Mecab
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity


def set_chrome_driver() :
    chrome_options = wd.ChromeOptions()
    driver = wd.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver


def getNews(save_path) :

    press_list, section_list, date_list, title_list, link_list, cmt_list, content_list, keyword_list = [], [], [], [], [], [], [], []
    sections = {'1' : '정치', '2' : '경제', '3' : '사회', '4' : '생활', '5' : '세계', '6' : 'IT'}

    driver = set_chrome_driver()

    pl, sl, dl, tl, ll, cl = [], [], [], [], [] ,[]
    for s in sections.values() :
        section = s
        pl, sl, dl, tl, ll, cl = get_News_infos(driver=driver, section=section)
        press_list.extend(pl)
        section_list.extend(sl)
        date_list.extend(dl)
        title_list.extend(tl)
        link_list.extend(ll)
        cmt_list.extend(cl)

    driver.close()

    content_list, keyword_list = get_contents(link_list)

    for keyword in keyword_list :
        if (keyword == 'None') :
            idx = keyword_list.index(keyword)
            del press_list[idx]
            del section_list[idx]
            del date_list[idx]
            del title_list[idx]
            del link_list[idx]
            del cmt_list[idx]
            del content_list[idx]
            del keyword_list[idx]

    data_list = [press_list, section_list, date_list, title_list, link_list, cmt_list, content_list, keyword_list]

    to_Excel(save_path, data_list)


def get_News_infos(driver, section) :

    headers = {
        'referer' : 'https://www.naver.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
        }  
    
    press_list, section_list, date_list, title_list, link_list, cmt_list = [], [], [], [], [], []

    press_id = {'경향신문' : '032', '국민일보' : '005', '동아일보' : '020', '서울신문' : '081', '조선일보' : '023', '중앙일보' : '025', '한겨레' : '028', '한국일보' : '469',
                'JTBC' : '437', 'KBS' : '056', 'MBC' : '214', 'SBS' : '055', 'YTN' : '052', '연합뉴스' : '001', '매일경제' : '009', '서울경제' : '011', '아시아경제' : '277', '한국경제 ' : '015', '헤럴드경제' : '016'}

    section_id = {'정치' : '100', '경제' : '101', '사회' : '102', '생활' : '103', '세계' : '104', 'IT' : '105'}
    sid = section_id[section]

    for press_name, pid in press_id.items() :

        url = f'https://media.naver.com/press/{pid}?sid={sid}'

        driver.get(url)

        res = driver.page_source
        soup = BeautifulSoup(res, 'lxml')

        press = press_name
        now = datetime.now()

        try :
            edit_news_boxes = soup.select('div._tab_panel > div.press_edit_news')

            for box in edit_news_boxes :
                edit_news_lists = box.select('ul > li')

                for li in edit_news_lists :

                    # 제목
                    title = li.select_one('a > span.press_edit_news_text > span.press_edit_news_title').text
                    # 날짜
                    date = li.select_one('a > span.press_edit_news_text > span.r_ico_b.r_modify > b')
                    date = re.sub('\t|\r|\n|<b>|</b>', '', str(date))

                    if '분' in date :
                        index = date.find('분')
                        date = date[0:index]
                        before_mins = now - timedelta(minutes=int(date))
                        date = before_mins.strftime('%y-%m-%d')

                    elif '시' in date :
                            index = date.find('시')
                            date = date[0:index]
                            before_hours = now - timedelta(hours=int(date)+1)
                            date = before_hours.strftime('%y-%m-%d')

                    elif '일' in date :
                            index = date.find('일')
                            date = date[0:index]
                            before_days = now - timedelta(days=int(date))
                            date = before_days.strftime('%y-%m-%d')

                    else :
                        date = now.strftime('%y-%m-%d')

                    # 링크
                    link = li.select_one('a')["href"]
                    
                    # 댓글 수
                    try :
                        cmt_link = li.select_one('a.ico_cmt.cmt._template')["href"]
                    except :
                        # 댓글 10개 미만인 경우 뉴스 본문이 아닌 댓글 페이지 따로 열어 댓글 수만 추출
                        article_num = link.split('/', maxsplit=5)[5].split('?')[0]
                        cmt_link = f"https://n.news.naver.com/article/comment/{pid}/{article_num}"
                    finally :
                        driver.get(cmt_link)
                        time.sleep(1)
                        ress = driver.page_source
                        soupp = BeautifulSoup(ress, 'lxml')
                        cmt = soupp.select_one('#cbox_module > div.u_cbox_wrap > div.u_cbox_comment_count_wrap > ul > li:nth-child(1) > span').text
                        cmt = int(cmt.replace(",", ""))
                         
                title_list.append(title)
                date_list.append(date)
                link_list.append(link)    
                press_list.append(press)
                section_list.append(section)
                cmt_list.append(cmt)
                        
        except Exception as e:
            print(e, "\n:", link)
            continue

    return press_list, section_list, date_list, title_list, link_list, cmt_list


def get_contents(link_list) :
    headers = {
        'referer' : 'https://www.naver.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
        }

    content_list, keyword_list = [], []

    for article_link in link_list :
        
        res = requests.get(article_link, headers=headers)
        soup = BeautifulSoup(res.text, 'lxml')

        try :
            content = soup.find('div', {'id' : 'dic_area'}).text
        except :
            try : 
                content = soup.find('div',{'id' : 'articleBodyContents'}).text
            except :
                try :
                    content = soup.find('div', {'id' : 'newsEndContents'}).text # 스포츠
                except :
                    try :
                        content = soup.find('div',{'id' : 'articeBody'}).text # 연예
                    except :
                        content_list.append('None')
                        keyword_list.append('None')
                        print("오류 발생\n : ", article_link)
                        continue
                        
        content = re.sub('\xa0|\t|\r|\n|', '', content)
        content = content.replace('// flash 오류를 우회하기 위한 함수 추가\nfunction _flash_removeCallback() {}','')
        #special = re.compile(r'[^ A-Za-z0-9가-힣+]')
        #content = special.sub(' ', content)
        content_list.append(content)

        textrank = TextRank(content)
        keyword_list.append(textrank.keywords())

    return content_list, keyword_list


def to_Excel(save_path, data_list) :

    article_df = pd.DataFrame({'press' : data_list[0],
                                                'section' : data_list[1],
                                               'date' : data_list[2],
                                               'title' : data_list[3],
                                               'link' : data_list[4],
                                               'comment' : data_list[5],
                                               'content' :data_list[6],
                                               'keywords' : data_list[7]})


    print(f"extract article num : {len(article_df)}")
    article_df.to_excel(f"{save_path}.xlsx", index=False)
    #article_df.to_json(f"{save_path}.json", orient='records', force_ascii=False, indent=3)
    print("파일 생성 완료")

    clustering(save_path=save_path, level=2, ranking_type='whole', article_df=article_df)
    clustering(save_path=save_path, level=3, ranking_type='section', article_df=article_df)
    clustering(save_path=save_path, level=4, ranking_type='section', article_df=article_df)


def clustering(save_path, level, ranking_type, article_df) :

    df = article_df
            
    mecab = Mecab()
    noun_list = []
    for content in tqdm(df['content']) :
        if content != '' :
            nouns = mecab.nouns(str(content))
            noun_list.append(nouns)

    df['nouns'] = noun_list

    text = [' '.join(noun) for noun in df['nouns']]

    tfidf_vectorizer = TfidfVectorizer(min_df = 0.01, ngram_range=(1,5))
    vector = tfidf_vectorizer.fit_transform(text)
    vector = vector.toarray()

    article_num = len(df)
    k = int(math.sqrt((article_num/2)/2))
    kmeans = KMeans(n_clusters = k, random_state = 10)
    kmeans.fit(vector)

    cluster_label = kmeans.fit_predict(vector)
    df['cluster_label'] = cluster_label

    for n in range(k) :
        print()
        globals()['cluster{}'.format(n)] = df[df['cluster_label'] == n].index
        print("카테고리 " + str(n) + "에 포함된 기사 인덱스\n", globals()['cluster{}'.format(n)])
        print()
        comparison_article = df.iloc[globals()['cluster{}'.format(n)][0]]['title']
        print("유사도 비교 기준 기사 :", comparison_article)
        print()

        similarity = cosine_similarity(vector[[globals()['cluster{}'.format(n)][0]]], vector[globals()['cluster{}'.format(n)]])
        similarity = similarity.tolist()
        print("유사도 : ") 
        print(similarity)
        print("----------------------------------------------------------------------------------------------------")        

        drop_index_list = []
        for idx in range(len(similarity)-1) :
            if (similarity[0][idx+1] >= 0.9) :
                drop_index_list.append(idx)
            else :
                continue

    df = df.drop(drop_index_list)
    df = df.sort_values(by='cluster_label')
    df.index = range(len(df))


    if ranking_type == 'whole' :

        df = df.sort_values(by=['cluster_label', 'comment'], ascending=[True, False]).groupby('cluster_label').head(60/k)

        if len(df) > 60 :
            num = len(df) - 60
            index = df.sort_values(by='comment', ascending=True).head(num).index
            df = df.drop(index)

        df = df.sort_values(by='comment', ascending=False)
        df.index = range(len(df))
        df['id'] = (df.index)+1
        final_df = df[['id', 'cluster_label','date', 'press', 'section', 'comment', 'title', 'link', 'content', 'keywords']]
        save_path = save_path + "_clustering_lv2"

    elif ranking_type == 'section' :

        sections = {'1' : '정치', '2' : '경제', '3' : '사회', '4' : '생활', '5' : '세계', '6' : 'IT'}
        df_s = df.sort_values(by ='comment', ascending=False)
        df_sort_group_top = pd.DataFrame()
        df_sort_group = pd.DataFrame()

        for section in sections.values() :
            temp = df_s[df_s['section'] == section]
            df_sort_group = pd.DataFrame()
            for label in range(k) :
                try :
                    if level == 3  :
                        tmp = temp[temp['cluster_label'] == label].head(1)
                    elif level == 4 :
                        tmp = temp[temp['cluster_label'] == label].head(2)
                    df_sort_group = pd.concat([df_sort_group, tmp])
                except Exception as e:
                    continue
                
                num = 0
                if (level == 3) and  (len(df_sort_group) > 3) :
                    num = len(df_sort_group) - 3
                    index = df_sort_group.sort_values(by='comment', ascending=True).head(num).index                      
                    df_sort_group = df_sort_group.drop(index)
                
                elif (level == 4) and  (len(df_sort_group) > 5) :
                    num = len(df_sort_group) - 5
                    index = df_sort_group.sort_values(by='comment', ascending=True).head(num).index                      
                    df_sort_group = df_sort_group.drop(index)

            df_sort_group_top= pd.concat([df_sort_group_top, df_sort_group])

        df_sg = df_sort_group_top.sort_values(by=['comment'], ascending=False)
        df_sg.index = range(len(df_sg))
        df_sg['id'] = (df_sg.index)+1
        final_df = df_sg[['id', 'cluster_label', 'date', 'press', 'section', 'comment', 'title', 'link', 'content', 'keywords']]
        
        if (level == 3) :
            save_path = save_path + "_clustering_lv3"
        else :
            save_path = save_path + "_clustering_lv4"

    if os.path.exists(f"{save_path}.xlsx") :
        os.remove(f"{save_path}.xlsx")
    final_df.to_excel(f"{save_path}.xlsx", index=False)


if __name__ == "__main__" :

    save_path = "./crawling_result" # 경로 설정
    date = datetime.now().strftime('%y%m%d')

    save_path = f"./crawling_result/{date}"
    try :
            os.makedirs(f"{save_path}")
    except :
            pass
    getNews(save_path=f"{save_path}")