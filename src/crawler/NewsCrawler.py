from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import re
import requests
import json
import pandas as pd
import urllib
import time
from datetime import datetime
from tqdm import tqdm
from TR import TextRank

def set_chrome_driver() :
    chrome_options = wd.ChromeOptions()
    driver = wd.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def to_Excel(save_path, ranking_type, data_list) :  
    # 엑셀 파일 생성
    if ranking_type == 'popular' :
        article_df = pd.DataFrame({'date' : data_list[0],
                                                   'press' : data_list[1],
                                                   'ranking' : data_list[2],
                                                   'views' : data_list[3],
                                                   'section' : data_list[8],
                                                   'title' : data_list[4],
                                                   'link' : data_list[5],
                                                   'content' :data_list[6],
                                                   'keywords' : data_list[7]})
                                                    
    elif ranking_type == 'comment' :
        article_df = pd.DataFrame({"date" : data_list[0],
                                                   "press" : data_list[1],
                                                   "ranking" : data_list[2],
                                                   "comments" : data_list[3],
                                                   'section' : data_list[8],
                                                   "title" : data_list[4],
                                                   "link" : data_list[5],
                                                   "content" :data_list[6],
                                                   "keywords" : data_list[7]})
        
    elif ranking_type == 'keyword' :
        article_df = pd.DataFrame({"date" : data_list[0],
                                                   "press" : data_list[1],
                                                   "reactions" : data_list[4],
                                                   "section" : data_list[8],
                                                   "title" : data_list[2],                                                
                                                   "link" : data_list[3],
                                                   "content" :data_list[5],
                                                   "keywords" : data_list[6]})

    print(f"extract article num : {len(article_df)}")
    article_df.to_excel(f"{save_path}.xlsx", index=False)

def to_Json(save_path, ranking_type, data_list) :

    data_dict = {}
    for idx in range (0, len(data_list[0])) :
        if ranking_type == 'popular' :
            data_dict[str(idx+1)] = {'date' : data_list[0][idx], 'press' : data_list[1][idx], 'ranking' : data_list[2][idx], 'views' : data_list[3][idx], 'section' : data_list[8][idx], 'title' : data_list[4][idx], 'link' : data_list[5][idx], 'content' : data_list[6][idx], 'keyword' : data_list[7][idx]}
        elif ranking_type == 'comment' :
            data_dict[str(idx+1)] = {'date' : data_list[0][idx], 'press' : data_list[1][idx], 'ranking' : data_list[2][idx], 'comments' : data_list[3][idx], 'section' : data_list[8][idx], 'title' : data_list[4][idx], 'link' : data_list[5][idx], 'content' : data_list[6][idx], 'keyword' : data_list[7][idx]}
        elif ranking_type == 'keyword' :
            data_dict[str(idx+1)] = {'date' : data_list[0][idx], 'press' : data_list[1][idx], 'reactions' : data_list[4][idx], 'section' : data_list[8][idx], 'title' : data_list[2][idx], 'link' : data_list[3][idx], 'content' : data_list[5][idx], 'keyword' : data_list[6][idx]}
        
    j = json.dumps(data_dict, ensure_ascii=False, indent="\t") 
    with open(f"{save_path}.json", 'w', encoding="utf-8") as f:
        f.write(j)


#########################
# 언론사별 랭킹뉴스 검색 #
#########################


def get_rankingNews(save_path, target_date, ranking_type) :

    crawl_date = f"{target_date[:4]}.{target_date[4:6]}.{target_date[6:]}"
    
    date_list, press_list, ranking_list, num_list, title_list, link_list, content_list, keyword_list = [], [], [], [], [], [], [], []
    section_list = []
    date_list, press_list, ranking_list, num_list, title_list, link_list = get_rankingNews_infos(crawl_date=crawl_date, ranking_type=ranking_type)
    data_list = [date_list, press_list, ranking_list, num_list, title_list, link_list]

    content_list, keyword_list, section_list = get_article_contents(link_list)
    data_list.append(content_list)
    data_list.append(keyword_list)
    data_list.append(section_list)

    #to_Excel(save_path, ranking_type, data_list)
    to_Json(save_path, ranking_type, data_list)


def get_rankingNews_infos(crawl_date, ranking_type) :
    
    headers = {
        'referer' : 'https://www.naver.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
        }

    date_list, press_list, ranking_list, num_list, title_list, link_list = [], [], [], [], [], []


    press_id = {'경향신문' : '032', '국민일보' : '005', '동아일보' : '020', '문화일보' : '021', '서울신문' : '081', '세계일보' : '022'}
    #press_id = {'경향신문' : '032', '국민일보' : '005', '동아일보' : '020', '문화일보' : '021', '서울신문' : '081', '세계일보' : '022',
                #'조선일보' : '023', '중앙일보' : '025', '한겨레' : '028', '한국일보' : '469', 'JTBC' : '437', 'KBS' : '056', 'MBC' : '214', 'MBN' : '057',
               #'SBS' : '055', 'SBS Biz' :  '374', 'TV 조선' : '448', 'YTN' : '052', '뉴스1' : '421', '뉴시스' : '003', '연합뉴스' : '001', '연합뉴스TV' : '422', '채널A' : '449', '한국경제TV' : '215',
                #'매일경제' : '009', '서울경제' : '011', '아시아경제' : '277', '한국경제 ' : '015', '헤럴드경제' : '016', '머니투데이' : '008', '이데일리' : '018', '조선비즈' : '366'}

    for pid in list(press_id.values()) :
        url = f"https://media.naver.com/press/{pid}/ranking?type={ranking_type}&date={target_date}"

        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'lxml')

        press = soup.select_one('div.press_hd_main_info > div > h3 > a').text
        press = re.sub('\xa0|\t|\r|\n|', '', press)

        press_ranking_boxes = soup.select('div.press_ranking_home > div.press_ranking_box')

        for box in press_ranking_boxes :
            rankingnews_lists = box.select('ul > li')

            for li in rankingnews_lists :
                ranking = li.select_one('em.list_ranking_num').text
                ranking_list.append(ranking)

                title = li.select_one('.list_content > strong').text
                title_list.append(title)

                if ranking_type == 'popular' :
                    try :
                        cnt = li.select_one('.list_content > span').text.replace('조회수', '')
                        cnt = cnt.strip()
                        num_list.append(cnt)
                    except :
                        num_list.append('미제공')
                    
                elif ranking_type == 'comment' :
                    try :
                        cnt = li.select_one('.list_content > span').text.replace('댓글', '')
                        cnt = cnt.strip()
                        num_list.append(cnt)
                    except :
                        num_list.append('미제공')

                link = li.select_one('a')["href"]
                link_list.append(link)

                date_list.append(crawl_date)
                press_list.append(press)

    return date_list, press_list, ranking_list, num_list, title_list, link_list


def get_article_contents(link_list) :
    headers = {
        'referer' : 'https://www.naver.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
        }

    content_list, keyword_list = [], []
    section_list = []

    for article_link in link_list :
        if article_link == '' :
            content_list.append('')
            keyword_list.append('')
            section_list.append('')
            continue

        res = requests.get(article_link, headers=headers)
        soup = BeautifulSoup(res.text, 'lxml')

        try : 
            content = soup.find('div',{'id' : 'articleBodyContents'}).text # 섹션탭에서 직접 선택하는 경우
            section = soup.select_one('#articleBody > div.guide_categorization > a > em').text
        except :
            try : 
                content = soup.find('div', {'id' : 'dic_area'}).text #랭킹뉴스 통하는 경우
                section = soup.select_one('#contents > div.media_end_categorize > a > em').text
            except :
                try :
                    content = soup.find('div', {'id' : 'newsEndContents'}).text # 스포츠
                    section = soup.select_one('#wa_categorize_tooltip').text[:3]
                except :
                    try :
                        content = soup.find('div',{'id' : 'articeBody'}).text # 연예
                        section = soup.select_one('#content > div.end_ct > div > div.guide_categorization > a > em').text[:2]
                    except :
                        continue
        finally :
            content = re.sub('\xa0|\t|\r|\n|', '', content)
            special = re.compile(r'[^ A-Za-z0-9가-힣+]')
            content = special.sub(' ', content)
            content_list.append(content)

            textrank = TextRank(content)
            keyword_list.append(textrank.keywords())
            
            section_list.append(section)
                    
    return content_list, keyword_list, section_list


##############
# 키워드 검색 #
##############


def date_setting(keyword, year, month, start_day, end_day, save_path):

    year = int(year)
    month = int(month)
    start_day = int(start_day)
    end_day = int(end_day)
    
    for day in tqdm(range(start_day, end_day+1)):
        date_time_obj = datetime(year=year, month=month, day=day)
        target_date = date_time_obj.strftime("%Y%m%d")
        ds_de = date_time_obj.strftime("%Y.%m.%d")

        get_keywordNews(keyword=keyword, save_path=f"{save_path}/{keyword}/{target_date}_{keyword}", target_date=target_date, ds_de=ds_de)


def get_keywordNews(keyword, save_path, target_date, ds_de, sort=0) :

    crawl_date = f"{target_date[:4]}.{target_date[4:6]}.{target_date[6:]}"
    driver = set_chrome_driver()

    encoded_keyword = urllib.parse.quote(keyword)
    url = f"https://search.naver.com/search.naver?where=news&query={encoded_keyword}&sm=tab_opt&sort={sort}&photo=0&field=0&pd=3&ds={ds_de}&de={ds_de}&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Ar%2Cp%3Afrom{target_date}to{target_date}&is_sug_officeid=0"
    more_news_base_url = "https://search.naver.com/search.naver"
    driver.get(url)

    date_list, press_list, num_list, title_list, link_list, content_list, keyword_list, more_news_url_list = [], [], [], [], [], [], [], []
    section_list = []
    date_list, press_list, title_list, link_list, more_news_url_list = get_keywordNews_infos(driver=driver,
                                                                                            crawl_date=crawl_date,
                                                                                            date_list=date_list,
                                                                                            press_list=press_list,
                                                                                            title_list=title_list,
                                                                                            link_list=link_list,                                                                                    
                                                                                            more_news_base_url=more_news_base_url,
                                                                                            more_news=True)
    
    content_list, keyword_list, num_list, section_list = get_kN_article_content(driver, link_list)
    driver.close()

    if len(more_news_url_list) > 0:
        more_news_url_list = list(set(more_news_url_list))
        for more_news_url in more_news_url_list:
            driver = set_chrome_driver()
            driver.get(more_news_url)
            
            date_list, press_list, title_list, link_list, more_news_url_list = get_keywordNews_infos(driver=driver,
                                                                                        crawl_date=crawl_date,
                                                                                        date_list=date_list,
                                                                                        press_list=press_list,
                                                                                        title_list=title_list,
                                                                                        link_list=link_list)
                                                                                        

            content_list, keyword_list, num_list, section_list = get_kN_article_content(driver, link_list)       
            driver.close()

    ranking_list = [] # 빈 리스트
    data_list = [date_list, press_list, title_list, link_list, num_list, content_list, keyword_list, ranking_list, section_list]
    ranking_type = 'keyword'
    
    #to_Excel(save_path, ranking_type, data_list)
    to_Json(save_path, ranking_type, data_list)


def get_keywordNews_infos(driver, crawl_date, date_list, press_list, title_list, link_list, more_news_base_url=None, more_news=False) :
    
    more_news_url_list = []
    while True :
        html_src = driver.page_source
        soup = BeautifulSoup(html_src, 'lxml')

        # 관련뉴스
        more_news_infos = soup.select('a.news_more')
        
        if more_news :
            for more_news_info in more_news_infos:
                more_news_url = f"{more_news_base_url}{more_news_info.get('href')}"
                more_news_url_list.append(more_news_url)
                          
        article_infos = soup.select('div.news_area')
        if not article_infos :
            break

        for article_info in article_infos :
                
            naver_article = article_info.select_one('div.info_group > a:nth-child(3)')
            if not naver_article :
                continue
            else :
                article_link = naver_article['href']
                
            link_list.append(article_link)
            
            # 언론사명
            press_info = article_info.select_one('div.info_group > a.info.press')
            if press_info is None :
                press_info = article_info.select_one('div.info_group > span.info.press')
                
            press = press_info.text.replace('언론사 선정', '')
            press_list.append(press)

            # 기사 제목
            article = article_info.select_one('a.news_tit')
            title = article.get('title')
            title_list.append(title)
            
            # 날짜
            date_list.append(crawl_date)
        
        time.sleep(2.0)

        next_btn_status = soup.select_one('a.btn_next').get('aria-disabled')
        if next_btn_status == 'true' :
            break

        time.sleep(1.0)
        next_page_btn = driver.find_element(By.CSS_SELECTOR, 'a.btn_next').click()
                      
    return date_list, press_list, title_list, link_list, more_news_url_list


def get_kN_article_content(driver, link_list) :
    
    headers = {
        'referer' : 'https://www.naver.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }
    
    content_list, keyword_list, num_list = [], [], []
    section_list = []

    for article_link in link_list :
        if article_link == '' :
            content_list.append('')
            keyword_list.append('')
            num_list.appned('')
            section_list.append('')
            continue

        res = requests.get(article_link, headers=headers)
        soup = BeautifulSoup(res.text, 'lxml')
        time.sleep(3)

        try : 
            content = soup.find('div',{'id' : 'articleBodyContents'}).text
            section = soup.select_one('#articleBody > div.guide_categorization > a > em').text
        except :
            try : 
                content = soup.find('div', {'id' : 'dic_area'}).text
                section = soup.select_one('#contents > div.media_end_categorize > a > em').text
            except :
                try :
                    content = soup.find('div', {'id' : 'newsEndContents'}).text
                    section = soup.select_one('#wa_categorize_tooltip').text[:3]
                except :
                    try :
                        content = soup.find('div',{'id' : 'articeBody'}).text
                        section = soup.select_one('#content > div.end_ct > div > div.guide_categorization > a > em').text[:2]
                    except :
                        continue
        finally :
            content = re.sub('\xa0|\t|\r|\n|', '', content)
            special = re.compile(r'[^ A-Za-z0-9가-힣+]')
            content = special.sub(' ', content)
            content_list.append(content)

            textrank = TextRank(content)
            keyword_list.append(textrank.keywords())
            
            section_list.append(section)

        driver = set_chrome_driver()
        driver.get(article_link)
        time.sleep(3)

        html_src = driver.page_source
        soup = BeautifulSoup(html_src, 'lxml')

        try :
            cnt = soup.select_one('.media_end_head_info_variety_likeit > ._reactionModule.u_likeit.nv_notrans > a > span.u_likeit_text._count.num').text
        except :
            try :
                cnt = soup.select_one('.btn_wrap > ._reactionModule.u_likeit > a > span.u_likeit_text._count').text  # 연예
            except :
                try :
                    cnt = soup.select_one('.count > ._reactionModule.u_likeit > a > span.u_likeit_text._count').text  # 스포츠
                except :
                    cnt = ''
        finally :
            if cnt == '공감' :
                cnt = '0'
            
            num_list.append(cnt)
            time.sleep(1)
            driver.close()

    return content_list, keyword_list, num_list, section_list


if __name__ == "__main__" :

    print("1. 언론사별 랭킹뉴스\n2. 키워드 검색\n")
    option = input("option (번호 입력) : ")
    save_path = "./crawling_result"

    if option == "1" :
        try :
            os.makedirs(f"{save_path}/언론사별 랭킹뉴스")
        except :
            pass

        target_date = input("검색일 : ")
        ranking_type = input("랭킹 타입 (1. 많이 본 , 2. 댓글 많은) : ")
        if '1' in ranking_type :
            ranking_type = 'popular'
        elif '2' in ranking_type :
            ranking_type = 'comment'

        print("Crawling start...")
        get_rankingNews(save_path=f"{save_path}/언론사별 랭킹뉴스/{target_date}_언론사별 랭킹뉴스", target_date=target_date, ranking_type=ranking_type)

        
    elif option == "2" :
        keyword = input("검색 키워드 : ")
        start_date = input("검색 시작일 : ")
        end_date = input("검색 종료일 : ")
        
        year = start_date[:4]
        month = start_date[4:6]
        start_day = start_date[6:]
        end_day = end_date[6:]

        try : 
            os.makedirs(f"{save_path}/{keyword}")
        except :
            pass

        print("Crawling start...")
        date_setting(keyword=keyword, year=year, month=month, start_day=start_day, end_day=end_day, save_path=save_path)