from konlpy.tag import Mecab
from konlpy.tag import Mecab
from collections import Counter
from collections import defaultdict
from tqdm import tqdm
from konlpy.tag import Komoran
'''
m=Mecab('C:\\mecab\\mecab-ko-dic')
word=m.nouns("창준님의 비밀병기")
print(word)
'''
import numpy as np
import pymysql
import pandas as pd
 
import FinanceDataReader as fdr
import yfinance as yf
from pykrx import bond
from pykrx import stock

import time
from datetime import datetime, timedelta
import schedule

from bs4 import BeautifulSoup as bs
import requests

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import joblib
import matplotlib.pyplot as plt 
import seaborn as sns

from pykrx import stock

import platform
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix, f1_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestClassifier
from catboost import CatBoostClassifier
from xgboost import XGBClassifier
from keras.models import Sequential
from keras.layers import Dense
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.layers import LSTM
from keras.backend import clear_session
from sklearn.metrics import classification_report
import warnings
from keras.models import load_model


#날짜 설정
current_time = datetime.now()  

start_date = current_time.strftime('%Y-%m-%d')
start_date = datetime.strptime(start_date, "%Y-%m-%d")
start_date = datetime.strptime('2022-12-28', "%Y-%m-%d") #테스트
now_date = start_date.strftime('%Y-%m-%d')




#거시지표 업데이트
def MacroeconomicIndicators_day_update(start_date):
    print('MacroeconomicIndicators등록 시작!!!')

    yesterday7_date = start_date
    yesterday7_date -= timedelta(days=7)
    end_date = start_date
    end_date += timedelta(days=1)

    yesterday7_date = str(yesterday7_date.date())
    nowdate = str(start_date.date())
    enddate = str(end_date.date())
    
    
    new_yesterday7_date = yesterday7_date.replace('-', '')
    new_nowdate = nowdate.replace('-', '')
    

    dfplus = pd.DataFrame()
    dfs = fdr.DataReader('KS11', yesterday7_date,enddate)  # 코스피i
    dfs = dfs.ffill()
    dfs = dfs.tail(1)
    dfplus["KOSPI"] = dfs['Close']
    

    dfs = fdr.DataReader('US500', yesterday7_date,enddate)  # S&P500
    dfs = dfs.ffill()
    dfs = dfs.tail(1)
    dfplus["SP500"] = dfs['Close'][0]
    

    dfs = fdr.DataReader('ZG', yesterday7_date,enddate)  # 금
    
    dfplus["Gold"] = dfs['Close'][0]
    

    dfs=yf.download('HG=F', yesterday7_date, enddate, auto_adjust=True)
    dfs = dfs.ffill()
    dfs = dfs.tail(1)
    dfplus["Copper"] = dfs['Close'][0]
    

    dfs = bond.get_otc_treasury_yields(new_yesterday7_date, new_nowdate, "국고채3년")
    dfs = dfs.ffill()
    dfs = dfs.tail(1)
    dfplus["Kgov3"] = dfs['수익률'][0]
    

    dfs = fdr.DataReader('USD/KRW', yesterday7_date,enddate)  # 환율
    dfs = dfs.ffill()
    dfs = dfs.tail(1)
    dfplus["USD-K"] = dfs['Close'][0]
    

    dfplus['Date'] = dfplus.index  # 인덱스값을 컬럼으로
    dfplus.reset_index(drop=True, inplace=True)  # 인덱스 제거

    stockai_db = pymysql.connect(host='localhost', user='root', password='aivle', db='stockai', charset='utf8')

    try:
        curs = stockai_db.cursor()
        sql = "INSERT INTO MacroeconomicIndicators(date_time,kospi,america_top_500,gold,copper,k_gov3,usd_k) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        
        curs.execute(sql, (dfplus['Date'][0],dfplus['KOSPI'][0],dfplus['SP500'][0],dfplus['Gold'][0],dfplus['Copper'][0],dfplus['Kgov3'][0],dfplus['USD-K'][0]))
        stockai_db.commit()

    finally:
        stockai_db.close()
        print('MacroeconomicIndicators등록 완료!!!')

#종목데이터 업데이트
def StockData_day_update(start_date):
    print("StockData등록 시작!!")
    code_list = ['000060', '000100', '000270', '000660', '000720', '000810', '003490', '003550', '003670', '004020', '004990', '005380', '005490', '005830', '005930', '005935', '005940', '006400', '006800', '007070', '008560', '008770', '009150', '009540', '009830', '010130', '010140', '010620', '010950', '011070', '011170', '011200', '011780', '011790', '012330', '012450', '015760', '016360', '017670', '018260', '018880', '021240', '024110', '028050', '028260', '028300', '029780', '030200', '032640', '032830', '033780', '034020', '034220', '034730', '035250', '035420', '035720', '036460', '036570', '047810', '051900', '051910', '055550', '066570', '066970', '068270', '071050', '078930', '086280', '086790', '088980', '090430', '091990', '096770', '097950', '105560', '128940', '137310', '138040', '161390', '207940', '241560', '247540', '251270', '259960', '267250', '271560', '282330', '293490', '302440', '316140', '323410', '326030', '329180', '352820', '361610', '373220', '377300', '383220', '402340']

    start = str(start_date.date())
    end = str(start_date.date())

    stockai_db = pymysql.connect(host='localhost', user='root', password='aivle', db='stockai', charset='utf8')

    try:
        curs = stockai_db.cursor()
        sql = "INSERT INTO StockData(stock_code,data_time,start_open,high,low,end_close,trading_volume,transaction_amount,end_rate_change,institutional_total,other_corporations,individual,foreigner_total,short_selling,short_buying,short_importance) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        
        for code in code_list:
            time.sleep(1)
            df1 = stock.get_market_ohlcv(start, end, code, "d")
            df2 = stock.get_market_trading_value_by_date(start, end, code)
            df3 = stock.get_shorting_volume_by_date(start, end, code)

            df_all = pd.concat([df1, df2, df3], axis=1)
            df_all['종목코드'] = "A"+code
            df_all.reset_index(inplace=True)

            curs.execute(sql, (df_all['종목코드'][0],df_all['날짜'][0],df_all['시가'][0],df_all['고가'][0],df_all['저가'][0],df_all['종가'][0],df_all['거래량'][0],df_all['거래대금'][0],df_all['등락률'][0],df_all['기관합계'][0],df_all['기타법인'][0],df_all['개인'][0],df_all['외국인합계'][0],df_all['공매도'][0],df_all['매수'][0],df_all['비중'][0]))
            stockai_db.commit()
            print(f"{code}등록 완료...")
    finally:
        stockai_db.close()
        print("StockData등록 완료!!")

#네이버 뉴스 본문+제목 크롤링 및 거시지표에 추가
def NaverNews_day_update(start_date):
    title_list =[]
    date_time_list =[]
    href_list = []
    newspaper_list = []
    content_list =[]

    start_date = start_date
    last_date = start_date


    while start_date <= last_date:
        today = start_date.strftime("%Y.%m.%d")

        url = 'https://search.naver.com/search.naver?where=news&query=증시%20심리%20코스피%20전망&sm=tab_opt&sort=2&photo=0&field=0&pd=3&ds='+str(today)+'&de='+str(today)+'&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Ar%2Cp%3Afrom20170228to20211231&is_sug_officeid=0'

        response = requests.get(url)
        time.sleep(1)
        html_text=response.text

        soup = bs(html_text, 'html.parser')

        titles = soup.select('ul.list_news > li > div > div > a')

        date_times = soup.select('ul.list_news > li > div > div > div.news_info > div.info_group > span')

        newspapers = soup.select('ul.list_news > li > div > div > div.news_info > div.info_group')

        for i in titles:
            title = i["title"]
            href = i["href"]
            title_list.append(title)
            href_list.append(href)

        for i in date_times:
            date_time = i.get_text()
            if("면" not in date_time):
                date_time = date_time[:-1]
                if(len(date_time) < 10):#x일전, x시간 전
                    new_date_time = str(today).replace('.', '-')
                else:
                    new_date_time = date_time.replace('.', '-')
                date_time_list.append(new_date_time)

        for i in newspapers:
            newspaper = i.get_text()
            newspaper_list.append(newspaper)
            
        print(today + "네이버 뉴스 크롤링 시작!")
        # 하루 더하기
        start_date += timedelta(days=1)
    
    href_len = len(href_list)
    
    for i in range(href_len):
        try:
            if("아주경제" in newspaper_list[i]):
                con_url = href_list[i]
                con_response = requests.get(con_url, headers={'User-Agent':'Mozilla/5.0'})
                time.sleep(1)
                con_html_text=con_response.text

                soup = bs(con_html_text, 'html.parser')

                contents = soup.select('#articleBody')

                tem_str = ''
                for con in contents:
                    tem_str = tem_str + con.get_text()

                content_list.append(tem_str)
            elif("에너지경제" in newspaper_list[i]):
                con_url = href_list[i]
                con_response = requests.get(con_url, headers={'User-Agent':'Mozilla/5.0'})
                time.sleep(1)
                con_html_text=con_response.text

                soup = bs(con_html_text, 'html.parser')

                contents = soup.select('#news_body_area_contents')

                tem_str = ''
                for con in contents:
                    tem_str = tem_str + con.get_text()

                content_list.append(tem_str)
            elif("디지털타임스" in newspaper_list[i]):
                con_url = href_list[i]

                con_response = requests.get(con_url, headers={'User-Agent':'Mozilla/5.0'})
                time.sleep(1)
                soup = bs(con_response.content.decode('euc-kr','replace'), 'html.parser') #한국어 깨짐 해결

                contents = soup.select('#article_body > div')

                tem_str = ''
                for con in contents:
                    tem_str = tem_str + con.get_text()

                content_list.append(tem_str)
            elif("세계일보" in newspaper_list[i]):
                con_url = href_list[i]
                con_response = requests.get(con_url, headers={'User-Agent':'Mozilla/5.0'})
                time.sleep(1)
                con_html_text=con_response.text

                soup = bs(con_html_text, 'html.parser')

                contents = soup.select('#article_txt > article')

                tem_str = ''
                for con in contents:
                    tem_str = tem_str + con.get_text()

                content_list.append(tem_str)
            elif("국제신문" in newspaper_list[i]):
                con_url = href_list[i]
                con_response = requests.get(con_url, headers={'User-Agent':'Mozilla/5.0'})
                time.sleep(1)
                soup = bs(con_response.content.decode('euc-kr','replace'), 'html.parser') #한국어 깨짐 해결

                contents = soup.select('#news_textArea > div.news_article')

                tem_str = ''
                for con in contents:
                    tem_str = tem_str + con.get_text()

                content_list.append(tem_str)
            elif("아시아투데이" in newspaper_list[i]):
                con_url = href_list[i]
                con_response = requests.get(con_url, headers={'User-Agent':'Mozilla/5.0'})
                time.sleep(1)
                con_html_text=con_response.text

                soup = bs(con_html_text, 'html.parser')

                contents = soup.select('#font')

                tem_str = ''
                for con in contents:
                    tem_str = tem_str + con.get_text()

                content_list.append(tem_str)
            elif("머니투데이" in newspaper_list[i]):
                con_url = href_list[i]
                con_response = requests.get(con_url, headers={'User-Agent':'Mozilla/5.0'})
                time.sleep(1)
                con_html_text=con_response.text

                soup = bs(con_html_text, 'html.parser')
                
                contents = soup.select('#textBody')

                tem_str = ''
                for con in contents:
                    tem_str = tem_str + con.get_text()

                content_list.append(tem_str)
            elif("브릿지경제" in newspaper_list[i]):
                con_url = href_list[i]
                con_response = requests.get(con_url, headers={'User-Agent':'Mozilla/5.0'})
                time.sleep(1)
                con_html_text=con_response.text

                soup = bs(con_html_text, 'html.parser')
                
                contents = soup.select('#container > div.con_left > div.view_left_warp > div.left_text_box')

                tem_str = ''
                for con in contents:
                    tem_str = tem_str + con.get_text()

                content_list.append(tem_str)
            elif("이데일리" in newspaper_list[i]):
                con_url = href_list[i]
                con_response = requests.get(con_url, headers={'User-Agent':'Mozilla/5.0'})
                time.sleep(1)
                con_html_text=con_response.text

                soup = bs(con_html_text, 'html.parser')
                
                contents = soup.select('#contents > section.center1080.position_r > section.aside_left > div.article_news > div.newscontainer > div.news_body')

                tem_str = ''
                for con in contents:
                    tem_str = tem_str + con.get_text()

                content_list.append(tem_str)

            elif("전자신문" in newspaper_list[i]):
                con_url = href_list[i]
                con_response = requests.get(con_url, headers={'User-Agent':'Mozilla/5.0'})
                time.sleep(1)
                con_html_text=con_response.text

                soup = bs(con_html_text, 'html.parser')
                
                contents = soup.select('body > section > section > article > div.article_body')

                tem_str = ''
                for con in contents:
                    tem_str = tem_str + con.get_text()

                content_list.append(tem_str)
            elif("매경이코노미" in newspaper_list[i]):
                con_url = href_list[i]
                con_response = requests.get(con_url, headers={'User-Agent':'Mozilla/5.0'})
                time.sleep(1)

                soup = bs(con_response.content.decode('utf-8','replace'), 'html.parser') #한국어 깨짐 해결
                
                contents = soup.select('#article_body')

                tem_str = ''
                for con in contents:
                    tem_str = tem_str + con.get_text()

                content_list.append(tem_str)
            elif("데일리안" in newspaper_list[i]):
                con_url = href_list[i]
                con_response = requests.get(con_url, headers={'User-Agent':'Mozilla/5.0'})
                time.sleep(1)
                con_html_text=con_response.text

                soup = bs(con_html_text, 'html.parser')
                
                contents = soup.select('#contentsArea > div:nth-child(1) > div:nth-child(5) > div.news-contents > div.article')

                tem_str = ''
                for con in contents:
                    tem_str = tem_str + con.get_text()

                content_list.append(tem_str)
            elif("뉴스핌" in newspaper_list[i]):
                con_url = href_list[i]
                con_response = requests.get(con_url, headers={'User-Agent':'Mozilla/5.0'})
                time.sleep(1)
                con_html_text=con_response.text

                soup = bs(con_html_text, 'html.parser')

                contents = soup.select('#news-contents')


                tem_str = ''
                for con in contents:
                    tem_str = tem_str + con.get_text()

                content_list.append(tem_str)
            elif("매일경제" in newspaper_list[i]):
                con_url = href_list[i]
                con_response = requests.get(con_url, headers={'User-Agent':'Mozilla/5.0'})
                time.sleep(1)
                con_html_text=con_response.text

                soup = bs(con_html_text, 'html.parser')

                contents = soup.select('#container > section > div.news_detail_body_group > section > div.min_inner > div.sec_body > div.news_cnt_detail_wrap')

                tem_str = ''
                for con in contents:
                    tem_str = tem_str + con.get_text()

                content_list.append(tem_str)
            elif("위키리크스한국" in newspaper_list[i]):
                con_url = href_list[i]
                con_response = requests.get(con_url, headers={'User-Agent':'Mozilla/5.0'})
                time.sleep(1)
                con_html_text=con_response.text

                soup = bs(con_html_text, 'html.parser')

                contents = soup.select('#article-view-content-div')

                tem_str = ''
                for con in contents:
                    tem_str = tem_str + con.get_text()

                content_list.append(tem_str)
            elif("뉴시스" in newspaper_list[i]):
                con_url = href_list[i]
                con_response = requests.get(con_url, headers={'User-Agent':'Mozilla/5.0'})
                time.sleep(1)
                con_html_text=con_response.text

                soup = bs(con_html_text, 'html.parser')

                contents = soup.select('#content > div.articleView > div.view > div.viewer > article')

                tem_str = ''
                for con in contents:
                    tem_str = tem_str + con.get_text()

                content_list.append(tem_str)
            elif("서울경제" in newspaper_list[i]):
                con_url = href_list[i]
                con_response = requests.get(con_url, headers={'User-Agent':'Mozilla/5.0'})
                time.sleep(1)
                con_html_text=con_response.text

                soup = bs(con_html_text, 'html.parser')

                contents = soup.select('#v-left-scroll-in > div.article_con > div.con_left > div.article_view')

                tem_str = ''
                for con in contents:
                    tem_str = tem_str + con.get_text()

                content_list.append(tem_str)
            elif("주간조선" in newspaper_list[i]):
                con_url = href_list[i]
                con_response = requests.get(con_url, headers={'User-Agent':'Mozilla/5.0'})
                time.sleep(1)
                con_html_text=con_response.text

                soup = bs(con_html_text, 'html.parser')

                contents = soup.select('#article-view-content-div')

                tem_str = ''
                for con in contents:
                    tem_str = tem_str + con.get_text()

                content_list.append(tem_str)
            elif("머니투데이" in newspaper_list[i]):
                con_url = href_list[i]
                con_response = requests.get(con_url, headers={'User-Agent':'Mozilla/5.0'})
                time.sleep(1)
                con_html_text=con_response.text

                soup = bs(con_html_text, 'html.parser')

                contents = soup.select('#textBody')

                tem_str = ''
                for con in contents:
                    tem_str = tem_str + con.get_text()

                content_list.append(tem_str)
            elif("뉴스토마토" in newspaper_list[i]):
                con_url = href_list[i]
                con_response = requests.get(con_url, headers={'User-Agent':'Mozilla/5.0'})
                time.sleep(1)
                con_html_text=con_response.text

                soup = bs(con_html_text, 'html.parser')

                contents = soup.select('#main-top > section > div > div.rn_sontent.pt0px > section > div')

                tem_str = ''
                for con in contents:
                    tem_str = tem_str + con.get_text()

                content_list.append(tem_str)
            elif("EBN" in newspaper_list[i]):
                con_url = href_list[i]
                con_response = requests.get(con_url, headers={'User-Agent':'Mozilla/5.0'})
                time.sleep(1)
                con_html_text=con_response.text

                soup = bs(con_html_text, 'html.parser')

                contents = soup.select('#newsContents')

                tem_str = ''
                for con in contents:
                    tem_str = tem_str + con.get_text()

                content_list.append(tem_str)
            elif("글로벌이코노믹" in newspaper_list[i]):
                con_url = href_list[i]
                con_response = requests.get(con_url, headers={'User-Agent':'Mozilla/5.0'})
                time.sleep(1)
                con_html_text=con_response.text

                soup = bs(con_html_text, 'html.parser')

                contents = soup.select('body > div.vcon > div.vcon_in > div.v_lt > div > div.mi_lt > div.v1d > div.vtxt.detailCont')

                tem_str = ''
                for con in contents:
                    tem_str = tem_str + con.get_text()

                content_list.append(tem_str)
            elif("오피니언뉴스" in newspaper_list[i]):
                con_url = href_list[i]
                con_response = requests.get(con_url, headers={'User-Agent':'Mozilla/5.0'})
                time.sleep(1)
                con_html_text=con_response.text

                soup = bs(con_html_text, 'html.parser')

                contents = soup.select('#article-view-content-div')

                tem_str = ''
                for con in contents:
                    tem_str = tem_str + con.get_text()

                content_list.append(tem_str)
            
            elif("파이낸셜뉴스" in newspaper_list[i]):
                con_url = href_list[i]
                con_response = requests.get(con_url, headers={'User-Agent':'Mozilla/5.0'})
                time.sleep(1)
                con_html_text=con_response.text

                soup = bs(con_html_text, 'html.parser')

                contents = soup.select('#article_content')

                tem_str = ''
                for con in contents:
                    tem_str = tem_str + con.get_text()

                content_list.append(tem_str)
            elif("매일일보" in newspaper_list[i]):
                con_url = href_list[i]
                con_response = requests.get(con_url, headers={'User-Agent':'Mozilla/5.0'})
                time.sleep(1)
                con_html_text=con_response.text

                soup = bs(con_html_text, 'html.parser')

                contents = soup.select('#article-view-content-div')

                tem_str = ''
                for con in contents:
                    tem_str = tem_str + con.get_text()

                content_list.append(tem_str)
            elif("아시아경제" in newspaper_list[i]):
                con_url = href_list[i]
                con_response = requests.get(con_url, headers={'User-Agent':'Mozilla/5.0'})
                time.sleep(1)
                con_html_text=con_response.text

                soup = bs(con_html_text, 'html.parser')

                contents = soup.select('#txt_area')

                tem_str = ''
                for con in contents:
                    tem_str = tem_str + con.get_text()

                content_list.append(tem_str)
            elif("머니S" in newspaper_list[i]):
                con_url = href_list[i]
                con_response = requests.get(con_url, headers={'User-Agent':'Mozilla/5.0'})
                time.sleep(1)
                con_html_text=con_response.text

                soup = bs(con_html_text, 'html.parser')

                contents = soup.select('#textBody > div')

                tem_str = ''
                for con in contents:
                    tem_str = tem_str + con.get_text()

                content_list.append(tem_str)
            elif("이투데이" in newspaper_list[i]):
                con_url = href_list[i]
                con_response = requests.get(con_url, headers={'User-Agent':'Mozilla/5.0'})
                time.sleep(1)
                con_html_text=con_response.text

                soup = bs(con_html_text, 'html.parser')

                contents = soup.select('body > div.wrap > article.containerWrap > section.view_body_moduleWrap > div.l_content_module > div > div > div.view_contents > div.articleView')

                tem_str = ''
                for con in contents:
                    tem_str = tem_str + con.get_text()

                content_list.append(tem_str)
            elif("이투데이" in newspaper_list[i]):
                con_url = href_list[i]
                con_response = requests.get(con_url, headers={'User-Agent':'Mozilla/5.0'})
                time.sleep(1)
                con_html_text=con_response.text

                soup = bs(con_html_text, 'html.parser')

                contents = soup.select('body > div.wrap > article.containerWrap > section.view_body_moduleWrap > div.l_content_module > div > div > div.view_contents > div.articleView')

                tem_str = ''
                for con in contents:
                    tem_str = tem_str + con.get_text()

                content_list.append(tem_str)
            elif("연합뉴스" in newspaper_list[i]):
                con_url = href_list[i]
                con_response = requests.get(con_url, headers={'User-Agent':'Mozilla/5.0'})
                time.sleep(1)
                con_html_text=con_response.text

                soup = bs(con_html_text, 'html.parser')

                contents = soup.select('#articleWrap > div.content01.scroll-article-zone01 > div > div > article')

                tem_str = ''
                for con in contents:
                    tem_str = tem_str + con.get_text()

                content_list.append(tem_str)
            elif("서울파이낸스" in newspaper_list[i]):
                con_url = href_list[i]
                con_response = requests.get(con_url, headers={'User-Agent':'Mozilla/5.0'})
                time.sleep(1)
                con_html_text=con_response.text

                soup = bs(con_html_text, 'html.parser')

                contents = soup.select('#article-view-content-div')

                tem_str = ''
                for con in contents:
                    tem_str = tem_str + con.get_text()

                content_list.append(tem_str)
            elif("연합인포맥스" in newspaper_list[i]):
                con_url = href_list[i]
                con_response = requests.get(con_url, headers={'User-Agent':'Mozilla/5.0'})
                time.sleep(1)
                con_html_text=con_response.text

                soup = bs(con_html_text, 'html.parser')

                contents = soup.select('#article-view-content-div')

                tem_str = ''
                for con in contents:
                    tem_str = tem_str + con.get_text()

                content_list.append(tem_str)
            elif("화이트페이퍼" in newspaper_list[i]):
                con_url = href_list[i]
                con_response = requests.get(con_url, headers={'User-Agent':'Mozilla/5.0'})
                time.sleep(1)
                con_html_text=con_response.text

                soup = bs(con_html_text, 'html.parser')

                contents = soup.select('#article-view-content-div')

                tem_str = ''
                for con in contents:
                    tem_str = tem_str + con.get_text()

                content_list.append(tem_str)
            elif("헤럴드경제" in newspaper_list[i]):
                con_url = href_list[i]
                con_response = requests.get(con_url, headers={'User-Agent':'Mozilla/5.0'})
                time.sleep(1)
                con_html_text=con_response.text

                soup = bs(con_html_text, 'html.parser')

                contents = soup.select('#articleText')

                tem_str = ''
                for con in contents:
                    tem_str = tem_str + con.get_text()

                content_list.append(tem_str)
            elif("일간NTN" in newspaper_list[i]):
                con_url = href_list[i]
                con_response = requests.get(con_url, headers={'User-Agent':'Mozilla/5.0'})
                time.sleep(1)
                con_html_text=con_response.text

                soup = bs(con_html_text, 'html.parser')

                contents = soup.select('#PTLT_title')

                tem_str = ''
                for con in contents:
                    tem_str = tem_str + con.get_text()

                content_list.append(tem_str)
            elif("이코노믹리뷰" in newspaper_list[i]):
                con_url = href_list[i]
                con_response = requests.get(con_url, headers={'User-Agent':'Mozilla/5.0'})
                time.sleep(1)
                con_html_text=con_response.text

                soup = bs(con_html_text, 'html.parser')

                contents = soup.select('#article-view-content-div')

                tem_str = ''
                for con in contents:
                    tem_str = tem_str + con.get_text()

                content_list.append(tem_str)
            elif("비즈니스워치" in newspaper_list[i]):
                con_url = href_list[i]
                con_response = requests.get(con_url, headers={'User-Agent':'Mozilla/5.0'})
                time.sleep(1)
                con_html_text=con_response.text

                soup = bs(con_html_text, 'html.parser')

                contents = soup.select('#wrap > div.content.cfixed > div.left_content > section > article > div')

                tem_str = ''
                for con in contents:
                    tem_str = tem_str + con.get_text()

                content_list.append(tem_str)
            elif("비즈니스포스트" in newspaper_list[i]):
                con_url = href_list[i]
                con_response = requests.get(con_url, headers={'User-Agent':'Mozilla/5.0'})
                time.sleep(1)
                con_html_text=con_response.text

                soup = bs(con_html_text, 'html.parser')

                contents = soup.select('#detail_tab_cont')

                tem_str = ''
                for con in contents:
                    tem_str = tem_str + con.get_text()

                content_list.append(tem_str)
            elif("글로벌경제" in newspaper_list[i]):
                con_url = href_list[i]
                con_response = requests.get(con_url, headers={'User-Agent':'Mozilla/5.0'})
                time.sleep(1)
                con_html_text=con_response.text

                soup = bs(con_html_text, 'html.parser')

                contents = soup.select('#article-view-content-div')

                tem_str = ''
                for con in contents:
                    tem_str = tem_str + con.get_text()

                content_list.append(tem_str)
            elif("한국일보" in newspaper_list[i]):
                con_url = href_list[i]
                con_response = requests.get(con_url, headers={'User-Agent':'Mozilla/5.0'})
                time.sleep(1)
                con_html_text=con_response.text

                soup = bs(con_html_text, 'html.parser')

                contents = soup.select('body > div.wrap.imp-end > div.container.end-uni > div.end-body > div > div.col-main')

                tem_str = ''
                for con in contents:
                    tem_str = tem_str + con.get_text()

                content_list.append(tem_str)
            elif("청년일보" in newspaper_list[i]):
                con_url = href_list[i]
                con_response = requests.get(con_url, headers={'User-Agent':'Mozilla/5.0'})
                time.sleep(1)
                con_html_text=con_response.text

                soup = bs(con_html_text, 'html.parser')

                contents = soup.select('#container > div > div:nth-child(1) > div > div.arv_005_01 > div.cnt_view.news_body_area')

                tem_str = ''
                for con in contents:
                    tem_str = tem_str + con.get_text()

                content_list.append(tem_str)
            

            else:
                content_list.append('')
        except:
            content_list.append('')

        print(f"{i} / {href_len} {href_list[i]} 본분내용추가!")
    
    #본문+제목
    df_o = pd.DataFrame({'제목' : title_list, '날짜' : date_time_list, '본문' : content_list})
    df_o['내용'] = df_o['제목'] + df_o['본문']
    
    #같은날 한 행으로 합치기
    base=pd.DataFrame(df_o[["날짜"]])
    base=base.drop_duplicates(["날짜"])
    base=base.reset_index(drop=True)
    
    dic={}
    for x in base["날짜"]:
        dic[x]=""
        
    for tit,dat in zip(df_o["내용"],df_o["날짜"]):
        dic[dat]+=" "+str(tit)

    result=pd.DataFrame([dic])
    result=result.transpose()
    result.columns=["내용"]
    result["날짜"]=result.index
    
    #거시지표 새로운 피처 생성
    modelpath='C:/dev/stock_data/자연어처리 모델.h5'
    naverdatapath="C:/dev/stock_data/NaverNew_labeling105.csv"
    word=result.iloc[:1]
    
    
    omoran = Komoran()

    mecab = Mecab("C:\\mecab\\mecab-ko-dic")

    word['내용'] = word['내용'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","", regex=True)
    word.reset_index(drop=True,inplace=True)

    stopwords = ['도', '는', '다', '의', '가', '이', '은', '한',
                '에', '하', '고', '을', '를', '인', '듯', '과', 
                '와', '네', '들', '듯', '지', '임', '게', '만', 
                '게임', '겜', '되', '음', '면','있','으로','했','로', '할']
    cols=['inflation' , #인플레이션
        'treasury_bonds' ,#국채
        'tightening' , #긴축
        'normality' , #정상
        'powell' , #파월
        'dispute' , #분쟁
        'japan' , #일본
        'volume' , #물량
        'chairman' , #의장
        'remarks' , #발언
        'thought' , #사상
        'effect' , #효과
        'anxiety' , #불안
        'buying' , #매수세
        'volatility' , #유동
        'early_stage' , #초반
        'decline' , #낙폭
        'learning_result'] #학습결과
    df=pd.DataFrame()
    wordlist=['인플레이션', '국채', '긴축', '정상', '파월', '분쟁'
                , '일본', '물량','의장','발언','사상','효과','불안','매수세','유동','초반','낙폭','date']
    list1=[[]for _ in range(17)]
    
    text=result["내용"][0]
    
    text = mecab.nouns(text)
    text = [item for item in text if item not in stopwords]
    text = np.hstack(text)

    word_count = Counter(text)

    for y in range(17):
        list1[y].append(word_count[wordlist[y]])

    
    
    for x in range(17):
        df[cols[x]]=list1[x] 

    df["date"]=word["날짜"]


    
    word["내용"]=pd.Series(map(lambda x:" ".join(mecab.nouns(x)) ,word["내용"]))
    
    #데이터 불러오기
    train=pd.read_csv(naverdatapath)
    train=train.dropna(axis=0)
    train=train.reset_index(drop=True)
    X_m_t=train["내용"]
    Y_m_t=train["label"]
    x_train_m, x_val_m, y_train_m, y_val_m=train_test_split(X_m_t,Y_m_t,test_size=0.2,random_state=42)

    NGRAM_RANGE = (1, 4) # 주변 요소 묶어서 분석 (1,4)->4개까지 묶어서 분석
    TOP_K = 20000 # 최대 토큰 개수
    TOKEN_MODE = 'word' #word 단어단위분석 char 문자단위분석
    MIN_DOCUMENT_FREQUENCY = 4 #뭐지?

    def ngram_vectorize(train_texts, train_labels, val_texts):

        kwargs = {
                'ngram_range': NGRAM_RANGE,  
                'dtype': 'int32',
                'strip_accents': 'unicode',
                'decode_error': 'replace',
                'analyzer': TOKEN_MODE, 
                'min_df': MIN_DOCUMENT_FREQUENCY,
        }
        vectorizer = TfidfVectorizer(**kwargs)
        x_train = vectorizer.fit_transform(train_texts)
        x_val = vectorizer.transform(val_texts)
        selector = SelectKBest(f_classif, k=min(TOP_K, x_train.shape[1]))
        selector.fit(x_train, train_labels)
        x_train = selector.transform(x_train).astype('float32')
        x_val = selector.transform(x_val).astype('float32')
        return x_train, x_val

    X_m_t=word["내용"]
    NGRAM_RANGE = (1, 4)
    TOKEN_MODE = 'word'
    MIN_DOCUMENT_FREQUENCY = 2
    TOP_K = 20000
    
    print("추출중...(밑에 경고 떠도 돌아가는중...)")
    
    x_train_m_ngr,x_test_m_ngr=ngram_vectorize(x_train_m,y_train_m,X_m_t)

    from keras.models import load_model
    model = load_model(modelpath)
    pred=model.predict(x_test_m_ngr)
    df[cols[17]]=pd.Series(pred[0])
    
    stockai_db = pymysql.connect(host='localhost', user='root', password='aivle', db='stockai', charset='utf8')

    try:
        curs = stockai_db.cursor()
        sql = "UPDATE MacroeconomicIndicators SET inflation = %s, treasury_bonds = %s, tightening = %s, normality = %s, powell = %s, dispute = %s, japan = %s, volume = %s, chairman = %s, remarks = %s, thought = %s, effect = %s, anxiety = %s, buying = %s, volatility = %s, early_stage = %s, decline = %s, learning_result = %s WHERE date_time = %s"
        for i in range(0,df.shape[0]):
            curs.execute(sql, (df['inflation'][i], df['treasury_bonds'][i], df['tightening'][i], df['normality'][i], df['powell'][i], df['dispute'][i], df['japan'][i], df['volume'][i], df['chairman'][i], df['remarks'][i], df['thought'][i], df['effect'][i], df['anxiety'][i], df['buying'][i], df['volatility'][i], df['early_stage'][i], df['decline'][i], df['learning_result'][i], df['date'][i]))
        stockai_db.commit()

    finally:
        stockai_db.close()
        print('MacroeconomicIndicators 추가등록 완료!!!')
    
#사용자 주식 가치 최신화
def invest_value_update(now_date):

    now_date = now_date
    print(str(now_date) + " invest_value_update...")


    stockai_db = pymysql.connect(host='localhost', user='root', password='aivle', db='stockai', charset='utf8', cursorclass=pymysql.cursors.DictCursor)

    try:
        curs = stockai_db.cursor()
        
        #유저 id 가져오기(사용함)
        curs.execute("SELECT userid, now_money FROM UserData")
        data = curs.fetchall()
        UserData = pd.DataFrame(data)
        
        #UserStock 가져오기(사용함)
        curs.execute("SELECT userid, stock_code, count FROM UserStock")
        data = curs.fetchall()
        UserStock = pd.DataFrame(data)
        
        
        for i in range(len(UserStock)):
            count = UserStock['count'][i]
            userid = UserStock['userid'][i]
            stock_code = UserStock['stock_code'][i]
            curs.execute("SELECT end_close FROM StockData WHERE (data_time = %s) AND (stock_code = %s)",(str(now_date), stock_code))
            stock_end = pd.DataFrame(curs.fetchall())
            stock_end = stock_end['end_close'][0]
            
            curs.execute("UPDATE UserStock SET stock_value = %s, sum_stock_value = %s WHERE (userid = %s) AND (stock_code = %s)",(stock_end, count * stock_end, userid, stock_code))
        stockai_db.commit()
        
        
        for i in range(len(UserData)):
            userid = UserData['userid'][i]
            now_money = UserData['now_money'][i]
            curs.execute("SELECT sum_stock_value FROM UserStock WHERE userid = %s",(userid))
            user = pd.DataFrame(curs.fetchall())
            
            user_sum_stock_value = 0
            for j in range(len(user)):#UserStock에서 sum_stock_value 다 더하기
                user_sum_stock_value += user['sum_stock_value'][j]
            
            #UserData invest_value, total_money 업데이트
            curs.execute("UPDATE UserData SET invest_value = %s, total_money = %s WHERE userid = %s",(user_sum_stock_value, now_money + user_sum_stock_value, userid))
            stockai_db.commit()
    finally:
        stockai_db.close()


#short_xgb_lstm 모델 생성 및 StockCode테이블에 정확도 업데이트(1주일 마다)
def short_model_create():
    conn = pymysql.connect(host='localhost', user='root', password='aivle', db='stockai', charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    curs = conn.cursor()
    stock_code_sql = "SELECT stock_code FROM StockCode"
    curs.execute(stock_code_sql)
    stock_code = curs.fetchall()
    stock_code_list = pd.DataFrame(stock_code)

    # 총합 정확도 예측을 위한 변수
    count = 0

    #출력하고자 하는 주식 개수 입력, 최대 100개
    stock_n = len(stock_code_list)

    try:
        # for문에 
        for i in range(0,stock_n):

            curs = conn.cursor()
            sql = "SELECT * FROM StockData WHERE stock_code ='{}'".format(str(stock_code_list['stock_code'][i]))
            # 코드 앞에서 A 지우고 주식 이름 불러오기
            name = stock.get_market_ticker_name(str(stock_code_list['stock_code'][i][1:]))
            curs.execute(sql)
            data = curs.fetchall()
            
            df = pd.DataFrame(data)
            
            # 0.00등 Nan 값으로 인식되지 않는 결측치를 Nan으로 바꿈
            df["start_open"] = df["start_open"].apply(lambda x: np.nan if x<0.00001 else x)
            df["high"] = df["high"].apply(lambda x: np.nan if x<0.00001 else x)
            df["low"] = df["low"].apply(lambda x: np.nan if x<0.00001 else x)
            df["trading_volume"] = df["trading_volume"].apply(lambda x: np.nan if x<0.00001 else x)
            df["institutional_total"] = df["institutional_total"].apply(lambda x: np.nan if x<0.00001 else x)
            df["other_corporations"] = df["other_corporations"].apply(lambda x: np.nan if x<0.00001 else x)
            df["individual"] = df["individual"].apply(lambda x: np.nan if x<0.00001 else x)
            df["foreigner_total"] = df["foreigner_total"].apply(lambda x: np.nan if x<0.00001 else x)
            df["transaction_amount"] = df["transaction_amount"].apply(lambda x: np.nan if x<0.00001 else x)
            df["short_selling"] = df["short_selling"].apply(lambda x: np.nan if x<0.01 else x)
            df["short_buying"] = df["short_buying"].apply(lambda x: np.nan if x<0.01 else x)
            
            df = df.fillna(method='bfill')
            df = df.fillna(method='ffill')
        
            df['1yd_end_close'] = df['end_close'].shift(1)
            df['1yd_trading'] = df['trading_volume'].shift(1)
            df['5일 평균 종가'] = df['end_close'].rolling(5).mean()
            df['10일 평균 종가'] = df['end_close'].rolling(10).mean()
            df['20일 평균 종가'] = df['end_close'].rolling(20).mean()
            df['60일 평균 종가'] = df['end_close'].rolling(60).mean()
            df['120일 평균 종가'] = df['end_close'].rolling(120).mean()
        
            df['5일 평균 거래량'] = df['trading_volume'].rolling(5).mean()
            df['10일 평균 거래량'] = df['trading_volume'].rolling(10).mean()
            df['20일 평균 거래량'] = df['trading_volume'].rolling(20).mean()
            df['60일 평균 거래량'] = df['trading_volume'].rolling(60).mean()
            df['120일 평균 거래량'] = df['trading_volume'].rolling(120).mean()
        
            pd.set_option('mode.chained_assignment',  None)
        
            #10일 뒤 5일 평균
            X1 = 10
            X2 = 5
            df['X1일 뒤 종가'] = df['end_close'].shift(-X1)
            df['X1일 뒤 X2일 평균 종가'] = 0
            for i in range(0, df.shape[0]-X2):
                for j in range(0,X2):
                    df['X1일 뒤 X2일 평균 종가'][i] = df['X1일 뒤 X2일 평균 종가'][i] + df['X1일 뒤 종가'][i+j]
                
            df['X1일 뒤 X2일 평균 종가'] = df['X1일 뒤 X2일 평균 종가']/X2
        
            df['X1일 뒤 X2일 평균 종가 변화량'] = df['X1일 뒤 X2일 평균 종가'] - df['end_close']
        
            # 분류 모델 쓸 때 0,1로 라벨링 하기
            df['X1일 뒤 X2일 평균 종가 변화량'] = df['X1일 뒤 X2일 평균 종가 변화량'].apply(lambda x: 1 if x>0 else 0)

            df.dropna(inplace=True)
            sql2 = "SELECT * FROM MacroeconomicIndicators"
            curs.execute(sql2)
            data2 = curs.fetchall()

            df2 = pd.DataFrame(data2)

            df2['코스피 5일 평균 종가'] = df2['kospi'].rolling(5).mean()
            df2['코스피 20일 평균 종가'] = df2['kospi'].rolling(20).mean()
            df2['코스피 60일 평균 종가'] = df2['kospi'].rolling(60).mean()
            df2['코스피 120일 평균 종가'] = df2['kospi'].rolling(120).mean()
        
            df2.dropna(inplace=True)
            
            df_m = pd.merge(df, df2, left_on='data_time',right_on='date_time',how='inner')
            
            #merge하면서 생기는 id 행들 제거
            df_m.drop(columns=['id_x','id_y'],inplace=True)
                                                
            # 컬럼 제작
            df_m['전일종가대비 당일 시가비율'] = df_m['1yd_end_close']/df_m['start_open']
            df_m['당일종가 대비 당일 고가 비율'] = df_m['high']/df_m['end_close']
            df_m['당일종가 대비 당일 저가 비율'] = df_m['low']/df_m['end_close']
            df_m['당일 종가 대비 전일 종가 비율'] = df_m['end_close']/df_m['1yd_end_close']
            df_m['전일 거래량 대비 당일 거래량 비율'] = df_m['trading_volume']/df_m['1yd_trading']
            df_m['5일 평균 종가 대비 당일 종가 비율'] = df_m['end_close']/df_m['5일 평균 종가']
            df_m['10일 평균 종가 대비 당일 종가 비율'] = df_m['end_close']/df_m['10일 평균 종가']
            df_m['20일 평균 종가 대비 당일 종가 비율'] = df_m['end_close']/df_m['20일 평균 종가']
            df_m['60일 평균 종가 대비 당일 종가 비율'] = df_m['end_close']/df_m['60일 평균 종가']
            df_m['120일 평균 종가 대비 당일 종가 비율'] = df_m['end_close']/df_m['120일 평균 종가']

            df_m['5일평균거래량대비당일거래량'] = df_m['trading_volume']/df_m['5일 평균 거래량']
            df_m['10일평균거래량대비당일거래량'] = df_m['trading_volume']/df_m['10일 평균 거래량']
            df_m['20일평균거래량대비당일거래량'] = df_m['trading_volume']/df_m['20일 평균 거래량']
            df_m['60일평균거래량대비당일거래량'] = df_m['trading_volume']/df_m['60일 평균 거래량']
            df_m['120일평균거래량대비당일거래량'] = df_m['trading_volume']/df_m['120일 평균 거래량']

            df_m['코스피지수5일평균종가대비당일종가비율'] = df_m['kospi']/df_m['코스피 5일 평균 종가']
            df_m['코스피지수20일평균종가대비당일종가비율'] = df_m['kospi']/df_m['코스피 20일 평균 종가']
            df_m['코스피지수60일평균종가대비당일종가비율'] = df_m['kospi']/df_m['코스피 60일 평균 종가']
            df_m['코스피지수120일평균종가대비당일종가비율'] = df_m['kospi']/df_m['코스피 120일 평균 종가']
            
            target = ['X1일 뒤 X2일 평균 종가 변화량']
            f_col = ['start_open', 'high', 'low', 'end_close',
                'trading_volume', 'transaction_amount', 'end_rate_change',
                'institutional_total', 'other_corporations', 'individual',
                'foreigner_total', 'short_selling', 'short_buying', 'short_importance',
                '1yd_end_close', '1yd_trading', '5일 평균 종가', '10일 평균 종가', '20일 평균 종가',
                '60일 평균 종가', '120일 평균 종가', '5일 평균 거래량', '10일 평균 거래량', '20일 평균 거래량',
                '60일 평균 거래량', '120일 평균 거래량', 'kospi','inflation', 'treasury_bonds', 
                    'tightening','normality', 'powell', 'dispute', 'japan', 'volume', 'chairman',
                    'remarks', 'thought', 'effect', 'anxiety', 'buying', 
                    'volatility', 'early_stage', 'decline', 'learning_result',
                'america_top_500', 'gold', 'copper', 'k_gov3', 'usd_k', '코스피 5일 평균 종가',
                '코스피 20일 평균 종가', '코스피 60일 평균 종가', '코스피 120일 평균 종가', '전일종가대비 당일 시가비율',
                '당일종가 대비 당일 고가 비율', '당일종가 대비 당일 저가 비율', '당일 종가 대비 전일 종가 비율',
                '전일 거래량 대비 당일 거래량 비율', '5일 평균 종가 대비 당일 종가 비율', '10일 평균 종가 대비 당일 종가 비율',
                '20일 평균 종가 대비 당일 종가 비율', '60일 평균 종가 대비 당일 종가 비율',
                '120일 평균 종가 대비 당일 종가 비율', '5일평균거래량대비당일거래량', '10일평균거래량대비당일거래량',
                '20일평균거래량대비당일거래량', '60일평균거래량대비당일거래량', '120일평균거래량대비당일거래량',
                '코스피지수5일평균종가대비당일종가비율', '코스피지수20일평균종가대비당일종가비율', 
                    '코스피지수60일평균종가대비당일종가비율','코스피지수120일평균종가대비당일종가비율']
            
            train_x, test_x, train_y, test_y = train_test_split(df_m[f_col], df_m[target], test_size=0.15,shuffle=False)
            
            #xgbboost
            xgb = XGBClassifier()
            xgb.fit(train_x, train_y)
            y_pred = xgb.predict(test_x)
            
            
            joblib.dump(xgb,'C:/dev/stock_data/model/xgbboost/short_pred/'+name+'_model.pkl')
            print("[XgbboostsShortPred] AI 예측 정확도 - " + name + ":",accuracy_score(test_y, y_pred))
            curs.execute("UPDATE StockCode SET xgb_short_pred = %s WHERE stock_name = %s",(accuracy_score(test_y, y_pred), name))  

            #lstm
            X=df_m[f_col]
            Y=df_m[target]
            
            scaler = MinMaxScaler()
            X_s = scaler.fit_transform(X)
            X_s = pd.DataFrame(X_s,columns=X.columns)
            TEST_SIZE = 180
            WINDOW_SIZE = 10

            train, test, train_y, test_y = train_test_split(X_s, Y, test_size=0.2,shuffle=False)

            def make_dataset(data, label, window_size=10):
                feature_list = []
                label_list = []
                for i in range(len(data) - window_size):
                    feature_list.append(np.array(data.iloc[i:i+window_size]))
                    label_list.append(np.array(label.iloc[i+window_size]))
                return np.array(feature_list), np.array(label_list)

            train_feature = train
            train_label = train_y

            train_feature, train_label = make_dataset(train_feature, train_label, 10)
            x_train, x_valid, y_train, y_valid = train_test_split(train_feature, train_label, test_size=0.05)
            test_feature = test
            test_label = test_y
            test_feature, test_label = make_dataset(test_feature, test_label, 10)

            clear_session()
            model = Sequential()
            model.add(LSTM(16, 
                           input_shape=(train_feature.shape[1], train_feature.shape[2]), 
                           activation='relu', 
                           return_sequences=False)
                      )

            model.add(Dense(1,activation='sigmoid'))

            model.compile(loss='mean_squared_error', optimizer='adam')
            early_stop = EarlyStopping(monitor='val_loss', patience=2)

            model_path = 'model'
            filename = os.path.join(model_path, 'tmp_checkpoint.h5')
            checkpoint = ModelCheckpoint(filename, monitor='val_loss', verbose=0, save_best_only=True, mode='auto')

            history = model.fit(x_train, y_train, 
                                                epochs=200, 
                                                batch_size=16,
                                                verbose=0,
                                                validation_data=(x_valid, y_valid), 
                                                callbacks=[early_stop, checkpoint])
            model.load_weights(filename)
            pred = model.predict(test_feature)
            pred=list(map(lambda x : 1 if x>0.5 else 0,pred))
            warnings.filterwarnings('ignore')
            count+=1
            
            model.save('C:/dev/stock_data/model/lstm/short_pred/'+name+'_model.h5')
            print("[LSTMShortPred] AI 예측 정확도 - " + name + ":",f1_score(pred, test_label, average='macro'))
            curs.execute("UPDATE StockCode SET ltms_short_pred = %s WHERE stock_name = %s",(f1_score(pred, test_label, average='macro'), name))
            
            print("진행도 : ", count,"/",stock_n)
            print()
        conn.commit()


    finally:
        conn.close()

#long_xgb_lstm 모델 생성 및 StockCode테이블에 정확도 업데이트(1주일 마다)
def long_model_create():
    conn = pymysql.connect(host='localhost', user='root', password='aivle', db='stockai', charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    curs = conn.cursor()
    stock_code_sql = "SELECT stock_code FROM StockCode"
    curs.execute(stock_code_sql)
    stock_code = curs.fetchall()
    stock_code_list = pd.DataFrame(stock_code)

    # 총합 정확도 예측을 위한 변수
    count = 0

    #출력하고자 하는 주식 개수 입력, 최대 100개
    stock_n = len(stock_code_list)

    try:
        # for문에 
        for i in range(0,stock_n):

            curs = conn.cursor()
            sql = "SELECT * FROM StockData WHERE stock_code ='{}'".format(str(stock_code_list['stock_code'][i]))
            # 코드 앞에서 A 지우고 주식 이름 불러오기
            name = stock.get_market_ticker_name(str(stock_code_list['stock_code'][i][1:]))
            curs.execute(sql)
            data = curs.fetchall()
            
            df = pd.DataFrame(data)
            
            # 0.00등 Nan 값으로 인식되지 않는 결측치를 Nan으로 바꿈
            df["start_open"] = df["start_open"].apply(lambda x: np.nan if x<0.00001 else x)
            df["high"] = df["high"].apply(lambda x: np.nan if x<0.00001 else x)
            df["low"] = df["low"].apply(lambda x: np.nan if x<0.00001 else x)
            df["trading_volume"] = df["trading_volume"].apply(lambda x: np.nan if x<0.00001 else x)
            df["institutional_total"] = df["institutional_total"].apply(lambda x: np.nan if x<0.00001 else x)
            df["other_corporations"] = df["other_corporations"].apply(lambda x: np.nan if x<0.00001 else x)
            df["individual"] = df["individual"].apply(lambda x: np.nan if x<0.00001 else x)
            df["foreigner_total"] = df["foreigner_total"].apply(lambda x: np.nan if x<0.00001 else x)
            df["transaction_amount"] = df["transaction_amount"].apply(lambda x: np.nan if x<0.00001 else x)
            df["short_selling"] = df["short_selling"].apply(lambda x: np.nan if x<0.01 else x)
            df["short_buying"] = df["short_buying"].apply(lambda x: np.nan if x<0.01 else x)
            
            df = df.fillna(method='bfill')
            df = df.fillna(method='ffill')
        
            df['1yd_end_close'] = df['end_close'].shift(1)
            df['1yd_trading'] = df['trading_volume'].shift(1)
            df['5일 평균 종가'] = df['end_close'].rolling(5).mean()
            df['10일 평균 종가'] = df['end_close'].rolling(10).mean()
            df['20일 평균 종가'] = df['end_close'].rolling(20).mean()
            df['60일 평균 종가'] = df['end_close'].rolling(60).mean()
            df['120일 평균 종가'] = df['end_close'].rolling(120).mean()
        
            df['5일 평균 거래량'] = df['trading_volume'].rolling(5).mean()
            df['10일 평균 거래량'] = df['trading_volume'].rolling(10).mean()
            df['20일 평균 거래량'] = df['trading_volume'].rolling(20).mean()
            df['60일 평균 거래량'] = df['trading_volume'].rolling(60).mean()
            df['120일 평균 거래량'] = df['trading_volume'].rolling(120).mean()
        
            pd.set_option('mode.chained_assignment',  None)
        
            #30일 뒤 10일 평균
            X1 = 30
            X2 = 10
            df['X1일 뒤 종가'] = df['end_close'].shift(-X1)
            df['X1일 뒤 X2일 평균 종가'] = 0
            for i in range(0, df.shape[0]-X2):
                for j in range(0,X2):
                    df['X1일 뒤 X2일 평균 종가'][i] = df['X1일 뒤 X2일 평균 종가'][i] + df['X1일 뒤 종가'][i+j]
                
            df['X1일 뒤 X2일 평균 종가'] = df['X1일 뒤 X2일 평균 종가']/X2
        
            df['X1일 뒤 X2일 평균 종가 변화량'] = df['X1일 뒤 X2일 평균 종가'] - df['end_close']
        
            # 분류 모델 쓸 때 0,1로 라벨링 하기
            df['X1일 뒤 X2일 평균 종가 변화량'] = df['X1일 뒤 X2일 평균 종가 변화량'].apply(lambda x: 1 if x>0 else 0)

            df.dropna(inplace=True)
            sql2 = "SELECT * FROM MacroeconomicIndicators"
            curs.execute(sql2)
            data2 = curs.fetchall()

            df2 = pd.DataFrame(data2)

            df2['코스피 5일 평균 종가'] = df2['kospi'].rolling(5).mean()
            df2['코스피 20일 평균 종가'] = df2['kospi'].rolling(20).mean()
            df2['코스피 60일 평균 종가'] = df2['kospi'].rolling(60).mean()
            df2['코스피 120일 평균 종가'] = df2['kospi'].rolling(120).mean()
        
            df2.dropna(inplace=True)
            
            df_m = pd.merge(df, df2, left_on='data_time',right_on='date_time',how='inner')
            
            #merge하면서 생기는 id 행들 제거
            df_m.drop(columns=['id_x','id_y'],inplace=True)
                                                
            # 컬럼 제작
            df_m['전일종가대비 당일 시가비율'] = df_m['1yd_end_close']/df_m['start_open']
            df_m['당일종가 대비 당일 고가 비율'] = df_m['high']/df_m['end_close']
            df_m['당일종가 대비 당일 저가 비율'] = df_m['low']/df_m['end_close']
            df_m['당일 종가 대비 전일 종가 비율'] = df_m['end_close']/df_m['1yd_end_close']
            df_m['전일 거래량 대비 당일 거래량 비율'] = df_m['trading_volume']/df_m['1yd_trading']
            df_m['5일 평균 종가 대비 당일 종가 비율'] = df_m['end_close']/df_m['5일 평균 종가']
            df_m['10일 평균 종가 대비 당일 종가 비율'] = df_m['end_close']/df_m['10일 평균 종가']
            df_m['20일 평균 종가 대비 당일 종가 비율'] = df_m['end_close']/df_m['20일 평균 종가']
            df_m['60일 평균 종가 대비 당일 종가 비율'] = df_m['end_close']/df_m['60일 평균 종가']
            df_m['120일 평균 종가 대비 당일 종가 비율'] = df_m['end_close']/df_m['120일 평균 종가']

            df_m['5일평균거래량대비당일거래량'] = df_m['trading_volume']/df_m['5일 평균 거래량']
            df_m['10일평균거래량대비당일거래량'] = df_m['trading_volume']/df_m['10일 평균 거래량']
            df_m['20일평균거래량대비당일거래량'] = df_m['trading_volume']/df_m['20일 평균 거래량']
            df_m['60일평균거래량대비당일거래량'] = df_m['trading_volume']/df_m['60일 평균 거래량']
            df_m['120일평균거래량대비당일거래량'] = df_m['trading_volume']/df_m['120일 평균 거래량']

            df_m['코스피지수5일평균종가대비당일종가비율'] = df_m['kospi']/df_m['코스피 5일 평균 종가']
            df_m['코스피지수20일평균종가대비당일종가비율'] = df_m['kospi']/df_m['코스피 20일 평균 종가']
            df_m['코스피지수60일평균종가대비당일종가비율'] = df_m['kospi']/df_m['코스피 60일 평균 종가']
            df_m['코스피지수120일평균종가대비당일종가비율'] = df_m['kospi']/df_m['코스피 120일 평균 종가']
            
            target = ['X1일 뒤 X2일 평균 종가 변화량']
            f_col = ['start_open', 'high', 'low', 'end_close',
                'trading_volume', 'transaction_amount', 'end_rate_change',
                'institutional_total', 'other_corporations', 'individual',
                'foreigner_total', 'short_selling', 'short_buying', 'short_importance',
                '1yd_end_close', '1yd_trading', '5일 평균 종가', '10일 평균 종가', '20일 평균 종가',
                '60일 평균 종가', '120일 평균 종가', '5일 평균 거래량', '10일 평균 거래량', '20일 평균 거래량',
                '60일 평균 거래량', '120일 평균 거래량', 'kospi','inflation', 'treasury_bonds', 
                    'tightening','normality', 'powell', 'dispute', 'japan', 'volume', 'chairman',
                    'remarks', 'thought', 'effect', 'anxiety', 'buying', 
                    'volatility', 'early_stage', 'decline', 'learning_result',
                'america_top_500', 'gold', 'copper', 'k_gov3', 'usd_k', '코스피 5일 평균 종가',
                '코스피 20일 평균 종가', '코스피 60일 평균 종가', '코스피 120일 평균 종가', '전일종가대비 당일 시가비율',
                '당일종가 대비 당일 고가 비율', '당일종가 대비 당일 저가 비율', '당일 종가 대비 전일 종가 비율',
                '전일 거래량 대비 당일 거래량 비율', '5일 평균 종가 대비 당일 종가 비율', '10일 평균 종가 대비 당일 종가 비율',
                '20일 평균 종가 대비 당일 종가 비율', '60일 평균 종가 대비 당일 종가 비율',
                '120일 평균 종가 대비 당일 종가 비율', '5일평균거래량대비당일거래량', '10일평균거래량대비당일거래량',
                '20일평균거래량대비당일거래량', '60일평균거래량대비당일거래량', '120일평균거래량대비당일거래량',
                '코스피지수5일평균종가대비당일종가비율', '코스피지수20일평균종가대비당일종가비율', 
                    '코스피지수60일평균종가대비당일종가비율','코스피지수120일평균종가대비당일종가비율']
            
            train_x, test_x, train_y, test_y = train_test_split(df_m[f_col], df_m[target], test_size=0.15,shuffle=False)
            
            #xgbboost
            xgb = XGBClassifier()
            xgb.fit(train_x, train_y)
            y_pred = xgb.predict(test_x)
            
            
            joblib.dump(xgb,'C:/dev/stock_data/model/xgbboost/long_pred/'+name+'_model.pkl')
            print("[XgbboostsLongPred] AI 예측 정확도 - " + name + ":",accuracy_score(test_y, y_pred))
            curs.execute("UPDATE StockCode SET xgb_long_pred = %s WHERE stock_name = %s",(accuracy_score(test_y, y_pred), name))  

            #lstm
            X=df_m[f_col]
            Y=df_m[target]
            
            scaler = MinMaxScaler()
            X_s = scaler.fit_transform(X)
            X_s = pd.DataFrame(X_s,columns=X.columns)
            TEST_SIZE = 180
            WINDOW_SIZE = 10

            train, test, train_y, test_y = train_test_split(X_s, Y, test_size=0.2,shuffle=False)

            def make_dataset(data, label, window_size=10):
                feature_list = []
                label_list = []
                for i in range(len(data) - window_size):
                    feature_list.append(np.array(data.iloc[i:i+window_size]))
                    label_list.append(np.array(label.iloc[i+window_size]))
                return np.array(feature_list), np.array(label_list)

            train_feature = train
            train_label = train_y

            train_feature, train_label = make_dataset(train_feature, train_label, 10)
            x_train, x_valid, y_train, y_valid = train_test_split(train_feature, train_label, test_size=0.05)
            test_feature = test
            test_label = test_y
            test_feature, test_label = make_dataset(test_feature, test_label, 10)

            clear_session()
            model = Sequential()
            model.add(LSTM(16, 
                           input_shape=(train_feature.shape[1], train_feature.shape[2]), 
                           activation='relu', 
                           return_sequences=False)
                      )

            model.add(Dense(1,activation='sigmoid'))

            model.compile(loss='mean_squared_error', optimizer='adam')
            early_stop = EarlyStopping(monitor='val_loss', patience=2)

            model_path = 'model'
            filename = os.path.join(model_path, 'tmp_checkpoint.h5')
            checkpoint = ModelCheckpoint(filename, monitor='val_loss', verbose=0, save_best_only=True, mode='auto')

            history = model.fit(x_train, y_train, 
                                                epochs=200, 
                                                batch_size=16,
                                                verbose=0,
                                                validation_data=(x_valid, y_valid), 
                                                callbacks=[early_stop, checkpoint])
            model.load_weights(filename)
            pred = model.predict(test_feature)
            pred=list(map(lambda x : 1 if x>0.5 else 0,pred))
            warnings.filterwarnings('ignore')
            count+=1
            
            model.save('C:/dev/stock_data/model/lstm/long_pred/'+name+'_model.h5')
            print("[LSTMLongPred] AI 예측 정확도 - " + name + ":",f1_score(pred, test_label, average='macro'))
            curs.execute("UPDATE StockCode SET ltms_long_pred = %s WHERE stock_name = %s",(f1_score(pred, test_label, average='macro'), name))
            
            print("진행도 : ", count,"/",stock_n)
            print()
        conn.commit()


    finally:
        conn.close()

#xgb,lstm 모델 예측 결과 ModelResult테이블에 업데이트 *(short_long_model_create()함수 실행뒤 실행)*
def ModelResult_update(start_date):
    conn = pymysql.connect(host='localhost', user='root', password='aivle', db='stockai', charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    curs = conn.cursor()
    stock_code_sql = "SELECT stock_code FROM StockCode"
    curs.execute(stock_code_sql)
    stock_code = curs.fetchall()
    stock_code_list = pd.DataFrame(stock_code) #종목코드 가져오기

    #오늘날짜로부터 200일 뒤까지 가져옴
    start_date = start_date
    end_date = start_date
    start_date -= timedelta(days=200)

    start_date = str(start_date.date())
    end_date = str(end_date.date())

    try:
        for i in range(0,len(stock_code_list)):
            curs = conn.cursor()
            # 코드 앞에서 A 지우고 주식 이름 불러오기
            name = stock.get_market_ticker_name(str(stock_code_list['stock_code'][i][1:]))
            curs.execute("SELECT * FROM StockData WHERE (data_time BETWEEN %s AND %s) AND (stock_code = %s)",(start_date, end_date, stock_code_list['stock_code'][i]))
            data = curs.fetchall()
            
            df = pd.DataFrame(data)
            
            df = df[-130:]
            
            # 0.00등 Nan 값으로 인식되지 않는 결측치를 Nan으로 바꿈
            df["start_open"] = df["start_open"].apply(lambda x: np.nan if x<0.00001 else x)
            df["high"] = df["high"].apply(lambda x: np.nan if x<0.00001 else x)
            df["low"] = df["low"].apply(lambda x: np.nan if x<0.00001 else x)
            df["trading_volume"] = df["trading_volume"].apply(lambda x: np.nan if x<0.00001 else x)
            df["institutional_total"] = df["institutional_total"].apply(lambda x: np.nan if x<0.00001 else x)
            df["other_corporations"] = df["other_corporations"].apply(lambda x: np.nan if x<0.00001 else x)
            df["individual"] = df["individual"].apply(lambda x: np.nan if x<0.00001 else x)
            df["foreigner_total"] = df["foreigner_total"].apply(lambda x: np.nan if x<0.00001 else x)
            df["transaction_amount"] = df["transaction_amount"].apply(lambda x: np.nan if x<0.00001 else x)
            df["short_selling"] = df["short_selling"].apply(lambda x: np.nan if x<0.01 else x)
            df["short_buying"] = df["short_buying"].apply(lambda x: np.nan if x<0.01 else x)
            
            df = df.fillna(method='bfill')
            df = df.fillna(method='ffill')
        
            df['1yd_end_close'] = df['end_close'].shift(1)
            df['1yd_trading'] = df['trading_volume'].shift(1)
            df['5일 평균 종가'] = df['end_close'].rolling(5).mean()
            df['10일 평균 종가'] = df['end_close'].rolling(10).mean()
            df['20일 평균 종가'] = df['end_close'].rolling(20).mean()
            df['60일 평균 종가'] = df['end_close'].rolling(60).mean()
            df['120일 평균 종가'] = df['end_close'].rolling(120).mean()
        
            df['5일 평균 거래량'] = df['trading_volume'].rolling(5).mean()
            df['10일 평균 거래량'] = df['trading_volume'].rolling(10).mean()
            df['20일 평균 거래량'] = df['trading_volume'].rolling(20).mean()
            df['60일 평균 거래량'] = df['trading_volume'].rolling(60).mean()
            df['120일 평균 거래량'] = df['trading_volume'].rolling(120).mean()
        
            pd.set_option('mode.chained_assignment',  None)

            df.dropna(inplace=True)
            
            curs.execute("SELECT * FROM MacroeconomicIndicators WHERE (date_time BETWEEN %s AND %s)",(start_date, end_date))
            data2 = curs.fetchall()

            df2 = pd.DataFrame(data2)
            
            df2 = df2[-130:]

            df2['코스피 5일 평균 종가'] = df2['kospi'].rolling(5).mean()
            df2['코스피 20일 평균 종가'] = df2['kospi'].rolling(20).mean()
            df2['코스피 60일 평균 종가'] = df2['kospi'].rolling(60).mean()
            df2['코스피 120일 평균 종가'] = df2['kospi'].rolling(120).mean()
        
            df2.dropna(inplace=True)
            
            df_m = pd.merge(df, df2, left_on='data_time',right_on='date_time',how='inner')
            
            #merge하면서 생기는 id 행들 제거
            df_m.drop(columns=['id_x','id_y'],inplace=True)
                                                
            # 컬럼 제작
            df_m['전일종가대비 당일 시가비율'] = df_m['1yd_end_close']/df_m['start_open']
            df_m['당일종가 대비 당일 고가 비율'] = df_m['high']/df_m['end_close']
            df_m['당일종가 대비 당일 저가 비율'] = df_m['low']/df_m['end_close']
            df_m['당일 종가 대비 전일 종가 비율'] = df_m['end_close']/df_m['1yd_end_close']
            df_m['전일 거래량 대비 당일 거래량 비율'] = df_m['trading_volume']/df_m['1yd_trading']
            df_m['5일 평균 종가 대비 당일 종가 비율'] = df_m['end_close']/df_m['5일 평균 종가']
            df_m['10일 평균 종가 대비 당일 종가 비율'] = df_m['end_close']/df_m['10일 평균 종가']
            df_m['20일 평균 종가 대비 당일 종가 비율'] = df_m['end_close']/df_m['20일 평균 종가']
            df_m['60일 평균 종가 대비 당일 종가 비율'] = df_m['end_close']/df_m['60일 평균 종가']
            df_m['120일 평균 종가 대비 당일 종가 비율'] = df_m['end_close']/df_m['120일 평균 종가']

            df_m['5일평균거래량대비당일거래량'] = df_m['trading_volume']/df_m['5일 평균 거래량']
            df_m['10일평균거래량대비당일거래량'] = df_m['trading_volume']/df_m['10일 평균 거래량']
            df_m['20일평균거래량대비당일거래량'] = df_m['trading_volume']/df_m['20일 평균 거래량']
            df_m['60일평균거래량대비당일거래량'] = df_m['trading_volume']/df_m['60일 평균 거래량']
            df_m['120일평균거래량대비당일거래량'] = df_m['trading_volume']/df_m['120일 평균 거래량']

            df_m['코스피지수5일평균종가대비당일종가비율'] = df_m['kospi']/df_m['코스피 5일 평균 종가']
            df_m['코스피지수20일평균종가대비당일종가비율'] = df_m['kospi']/df_m['코스피 20일 평균 종가']
            df_m['코스피지수60일평균종가대비당일종가비율'] = df_m['kospi']/df_m['코스피 60일 평균 종가']
            df_m['코스피지수120일평균종가대비당일종가비율'] = df_m['kospi']/df_m['코스피 120일 평균 종가']
            
            f_col = ['start_open', 'high', 'low', 'end_close',
                'trading_volume', 'transaction_amount', 'end_rate_change',
                'institutional_total', 'other_corporations', 'individual',
                'foreigner_total', 'short_selling', 'short_buying', 'short_importance',
                '1yd_end_close', '1yd_trading', '5일 평균 종가', '10일 평균 종가', '20일 평균 종가',
                '60일 평균 종가', '120일 평균 종가', '5일 평균 거래량', '10일 평균 거래량', '20일 평균 거래량',
                '60일 평균 거래량', '120일 평균 거래량', 'kospi', 
                    'inflation', 'treasury_bonds', 'tightening','normality', 
                    'powell', 'dispute', 'japan', 'volume', 'chairman',
                    'remarks', 'thought', 'effect', 'anxiety', 'buying', 
                    'volatility', 'early_stage', 'decline', 'learning_result',
                'america_top_500', 'gold', 'copper', 'k_gov3', 'usd_k', '코스피 5일 평균 종가',
                '코스피 20일 평균 종가', '코스피 60일 평균 종가', '코스피 120일 평균 종가', '전일종가대비 당일 시가비율',
                '당일종가 대비 당일 고가 비율', '당일종가 대비 당일 저가 비율', '당일 종가 대비 전일 종가 비율',
                '전일 거래량 대비 당일 거래량 비율', '5일 평균 종가 대비 당일 종가 비율', '10일 평균 종가 대비 당일 종가 비율',
                '20일 평균 종가 대비 당일 종가 비율', '60일 평균 종가 대비 당일 종가 비율',
                '120일 평균 종가 대비 당일 종가 비율', '5일평균거래량대비당일거래량', '10일평균거래량대비당일거래량',
                '20일평균거래량대비당일거래량', '60일평균거래량대비당일거래량', '120일평균거래량대비당일거래량',
                '코스피지수5일평균종가대비당일종가비율', '코스피지수20일평균종가대비당일종가비율', 
                    '코스피지수60일평균종가대비당일종가비율','코스피지수120일평균종가대비당일종가비율']
            
            #xgbboost
            test_x = df_m[f_col]
            
            xgb_short_pred = joblib.load('C:/dev/stock_data/model/xgbboost/short_pred/'+name+'_model.pkl')
            xgb_short_y_pred = xgb_short_pred.predict(test_x)
            
            xgb_long_pred = joblib.load('C:/dev/stock_data/model/xgbboost/long_pred/'+name+'_model.pkl')
            xgb_long_y_pred = xgb_long_pred.predict(test_x)

            print(name + "의 " + str(df_m['data_time'][10])+" xgb_short_pred예측 결과 = ",xgb_short_y_pred[0]) #10일뒤 5일평균
            print(name + "의 " + str(df_m['data_time'][10])+" xgb_long_pred예측 결과 = ",xgb_long_y_pred[0]) #30일뒤 10일평균
            print()
            
            
            #lstm
            test_x = df_m[f_col]
            
            scaler = MinMaxScaler()
            X_s = scaler.fit_transform(test_x)
            X_s = pd.DataFrame(X_s,columns=test_x.columns)
            TEST_SIZE = 180
            WINDOW_SIZE = 10
            
            def make_dataset(data, window_size=10):
                feature_list = []
                for i in range(len(data) - window_size):
                    feature_list.append(np.array(data.iloc[i:i+window_size]))
                return np.array(feature_list)
            test_feature= make_dataset(X_s, 10)
            
            lstm_short_model = load_model('C:/dev/stock_data/model/lstm/short_pred/'+name+'_model.h5')
            lstm_short_pred = lstm_short_model.predict(test_feature)
            
            lstm_long_model = load_model('C:/dev/stock_data/model/lstm/short_pred/'+name+'_model.h5')
            lstm_long_pred = lstm_long_model.predict(test_feature)
            
            
            print(name + "의 " + str(df_m['data_time'][10])+" lstm_short_pred 예측 결과 = ",round(lstm_short_pred[0][0],5))
            print(name + "의 " + str(df_m['data_time'][10])+" lstm_long_pred 예측 결과 = ",round(lstm_long_pred[0][0],5))
            print()
            
            sql = "INSERT INTO ModelResult(stock_code,date_time,xgb_short_result,xgb_long_result,lstm_short_result,lstm_long_result) VALUES (%s, %s, %s, %s, %s, %s)"
            curs.execute(sql, (stock_code_list['stock_code'][i], df_m['data_time'][10], xgb_short_y_pred[0], xgb_long_y_pred[0], round(lstm_short_pred[0][0],5), round(lstm_long_pred[0][0],5)))
        conn.commit()
        
    finally:
        conn.close()

#AIRate,AIFunds 업데이트 - AI모의투자 결과 저장
def AIRate_AIFunds_update(start_date):
    conn = pymysql.connect(host='localhost', user='root', password='aivle', db='stockai', charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    curs = conn.cursor()
    stock_code_sql = "SELECT stock_code FROM StockCode"
    curs.execute(stock_code_sql)
    stock_code = curs.fetchall()
    stock_code_list = pd.DataFrame(stock_code)


    meansu=[]
    profitdata=pd.DataFrame()
    holding=pd.DataFrame()
    maxsu=0
    minsu=100
    #출력하고자 하는 주식 개수 입력, 최대 100개
    stock_n = 96
    datelist=[]

    end_date = start_date

    end_date = str(end_date.date())
    start_date = "2021-12-17"


    print(f"start_date = {start_date}, end_date = {end_date}")
    try:
        # for문에 
        for i in range(0,stock_n):
            from pykrx import stock
            curs = conn.cursor()
            curs.execute("SELECT * FROM StockData WHERE (data_time BETWEEN %s AND %s) AND (stock_code = %s)",(start_date, end_date, stock_code_list['stock_code'][i]))
            # 코드 앞에서 A 지우고 주식 이름 불러오기
            name = stock.get_market_ticker_name(str(stock_code_list['stock_code'][i][1:]))
            data = curs.fetchall()
            df = pd.DataFrame(data)
            
            curs.execute("SELECT * FROM stockcode WHERE stock_name=%s",name)
            data = curs.fetchall()
            score = pd.DataFrame(data)

            # 0.00등 Nan 값으로 인식되지 않는 결측치를 Nan으로 바꿈
            df["start_open"] = df["start_open"].apply(lambda x: np.nan if x<0.00001 else x)
            df["high"] = df["high"].apply(lambda x: np.nan if x<0.00001 else x)
            df["low"] = df["low"].apply(lambda x: np.nan if x<0.00001 else x)
            df["trading_volume"] = df["trading_volume"].apply(lambda x: np.nan if x<0.00001 else x)
            df["institutional_total"] = df["institutional_total"].apply(lambda x: np.nan if x<0.00001 else x)
            df["other_corporations"] = df["other_corporations"].apply(lambda x: np.nan if x<0.00001 else x)
            df["individual"] = df["individual"].apply(lambda x: np.nan if x<0.00001 else x)
            df["foreigner_total"] = df["foreigner_total"].apply(lambda x: np.nan if x<0.00001 else x)
            df["transaction_amount"] = df["transaction_amount"].apply(lambda x: np.nan if x<0.00001 else x)
            df["short_selling"] = df["short_selling"].apply(lambda x: np.nan if x<0.01 else x)
            df["short_buying"] = df["short_buying"].apply(lambda x: np.nan if x<0.01 else x)
            
            df = df.fillna(method='bfill')
            df = df.fillna(method='ffill')
        
            df['1yd_end_close'] = df['end_close'].shift(1)
            df['1yd_trading'] = df['trading_volume'].shift(1)
            df['5일 평균 종가'] = df['end_close'].rolling(5).mean()
            df['10일 평균 종가'] = df['end_close'].rolling(10).mean()
            df['20일 평균 종가'] = df['end_close'].rolling(20).mean()
            df['60일 평균 종가'] = df['end_close'].rolling(60).mean()
            df['120일 평균 종가'] = df['end_close'].rolling(120).mean()
        
            df['5일 평균 거래량'] = df['trading_volume'].rolling(5).mean()
            df['10일 평균 거래량'] = df['trading_volume'].rolling(10).mean()
            df['20일 평균 거래량'] = df['trading_volume'].rolling(20).mean()
            df['60일 평균 거래량'] = df['trading_volume'].rolling(60).mean()
            df['120일 평균 거래량'] = df['trading_volume'].rolling(120).mean()
        
            pd.set_option('mode.chained_assignment',  None)

            df.dropna(inplace=True)
            
            curs.execute("SELECT * FROM MacroeconomicIndicators WHERE (date_time BETWEEN %s AND %s)",(start_date, end_date))
            data2 = curs.fetchall()

            df2 = pd.DataFrame(data2)
            

            df2['코스피 5일 평균 종가'] = df2['kospi'].rolling(5).mean()
            df2['코스피 20일 평균 종가'] = df2['kospi'].rolling(20).mean()
            df2['코스피 60일 평균 종가'] = df2['kospi'].rolling(60).mean()
            df2['코스피 120일 평균 종가'] = df2['kospi'].rolling(120).mean()
        
            df2.dropna(inplace=True)
            
            df_m = pd.merge(df, df2, left_on='data_time',right_on='date_time',how='inner')
            
            #merge하면서 생기는 id 행들 제거
            df_m.drop(columns=['id_x','id_y'],inplace=True)
                                                
            # 컬럼 제작
            df_m['전일종가대비 당일 시가비율'] = df_m['1yd_end_close']/df_m['start_open']
            df_m['당일종가 대비 당일 고가 비율'] = df_m['high']/df_m['end_close']
            df_m['당일종가 대비 당일 저가 비율'] = df_m['low']/df_m['end_close']
            df_m['당일 종가 대비 전일 종가 비율'] = df_m['end_close']/df_m['1yd_end_close']
            df_m['전일 거래량 대비 당일 거래량 비율'] = df_m['trading_volume']/df_m['1yd_trading']
            df_m['5일 평균 종가 대비 당일 종가 비율'] = df_m['end_close']/df_m['5일 평균 종가']
            df_m['10일 평균 종가 대비 당일 종가 비율'] = df_m['end_close']/df_m['10일 평균 종가']
            df_m['20일 평균 종가 대비 당일 종가 비율'] = df_m['end_close']/df_m['20일 평균 종가']
            df_m['60일 평균 종가 대비 당일 종가 비율'] = df_m['end_close']/df_m['60일 평균 종가']
            df_m['120일 평균 종가 대비 당일 종가 비율'] = df_m['end_close']/df_m['120일 평균 종가']

            df_m['5일평균거래량대비당일거래량'] = df_m['trading_volume']/df_m['5일 평균 거래량']
            df_m['10일평균거래량대비당일거래량'] = df_m['trading_volume']/df_m['10일 평균 거래량']
            df_m['20일평균거래량대비당일거래량'] = df_m['trading_volume']/df_m['20일 평균 거래량']
            df_m['60일평균거래량대비당일거래량'] = df_m['trading_volume']/df_m['60일 평균 거래량']
            df_m['120일평균거래량대비당일거래량'] = df_m['trading_volume']/df_m['120일 평균 거래량']

            df_m['코스피지수5일평균종가대비당일종가비율'] = df_m['kospi']/df_m['코스피 5일 평균 종가']
            df_m['코스피지수20일평균종가대비당일종가비율'] = df_m['kospi']/df_m['코스피 20일 평균 종가']
            df_m['코스피지수60일평균종가대비당일종가비율'] = df_m['kospi']/df_m['코스피 60일 평균 종가']
            df_m['코스피지수120일평균종가대비당일종가비율'] = df_m['kospi']/df_m['코스피 120일 평균 종가']
            
            f_col = ['start_open', 'high', 'low', 'end_close',
                'trading_volume', 'transaction_amount', 'end_rate_change',
                'institutional_total', 'other_corporations', 'individual',
                'foreigner_total', 'short_selling', 'short_buying', 'short_importance',
                '1yd_end_close', '1yd_trading', '5일 평균 종가', '10일 평균 종가', '20일 평균 종가',
                '60일 평균 종가', '120일 평균 종가', '5일 평균 거래량', '10일 평균 거래량', '20일 평균 거래량',
                '60일 평균 거래량', '120일 평균 거래량', 'kospi', 
                    'inflation', 'treasury_bonds', 'tightening','normality', 
                    'powell', 'dispute', 'japan', 'volume', 'chairman',
                    'remarks', 'thought', 'effect', 'anxiety', 'buying', 
                    'volatility', 'early_stage', 'decline', 'learning_result',
                'america_top_500', 'gold', 'copper', 'k_gov3', 'usd_k', '코스피 5일 평균 종가',
                '코스피 20일 평균 종가', '코스피 60일 평균 종가', '코스피 120일 평균 종가', '전일종가대비 당일 시가비율',
                '당일종가 대비 당일 고가 비율', '당일종가 대비 당일 저가 비율', '당일 종가 대비 전일 종가 비율',
                '전일 거래량 대비 당일 거래량 비율', '5일 평균 종가 대비 당일 종가 비율', '10일 평균 종가 대비 당일 종가 비율',
                '20일 평균 종가 대비 당일 종가 비율', '60일 평균 종가 대비 당일 종가 비율',
                '120일 평균 종가 대비 당일 종가 비율', '5일평균거래량대비당일거래량', '10일평균거래량대비당일거래량',
                '20일평균거래량대비당일거래량', '60일평균거래량대비당일거래량', '120일평균거래량대비당일거래량',
                '코스피지수5일평균종가대비당일종가비율', '코스피지수20일평균종가대비당일종가비율', 
                    '코스피지수60일평균종가대비당일종가비율','코스피지수120일평균종가대비당일종가비율']
            
            #XGB 예측
            test_x = df_m[f_col][10:]
            model = joblib.load('C:/dev/stock_data/model/xgbboost/short_pred/'+name+'_model.pkl')
            XGB_pred = model.predict(test_x)
            
            
            #LSTM 전처리
            test_x = df_m[f_col]
            scaler = MinMaxScaler()
            X_s = scaler.fit_transform(test_x)
            X_s = pd.DataFrame(X_s,columns=test_x.columns)
            TEST_SIZE = 180
            WINDOW_SIZE = 10
            def make_dataset(data, window_size=10):
                feature_list = []
                for i in range(len(data) - window_size):
                    feature_list.append(np.array(data.iloc[i:i+window_size]))
                return np.array(feature_list)
            test_feature= make_dataset(X_s, 10)
            
            #LSTM 예측
            model = load_model('C:/dev/stock_data/model/lstm/short_pred/'+name+'_model.h5')
            LSTM_pred = model.predict(test_feature)
            
            res=pd.DataFrame()
            res["date"]=df_m['data_time'][10:]
            res["XGB"]=XGB_pred
            res["LSTM"]=LSTM_pred
            res["end_close"]=df_m["end_close"][10:]
            
            #모의투자 방식
            money=100000000
            stock=0
            size=int(5000000/list(res["end_close"])[0])
            # print("사이즈",size)
            score["xgb_short_pred"]
            profit=[]
            hold=[]
            '''
            XGB가 1일시 2배수 구매
            XGB가 0일시 0배수 구매
            XGB*2 = XGB개도
            int((LSTM-0.5)*10) =LSTM 구매개도
            '''
            targets=""
            tgsc=0
            if score["xgb_short_pred"][0] <= score["ltms_short_pred"][0]:
                targets="LSTM"
                tgsc=score["ltms_short_pred"][0]
            else:
                targets="XGB"
                tgsc=score["xgb_short_pred"][0]
            
            for end,pred in zip(res["end_close"],res[targets]):
                if pred > 0.9:
                    if money>end*size:
                        money-=end*size
                        stock+=1*size
                if pred > 0.6:
                    if money>end*size:
                        money-=end*size
                        stock+=1*size
                if pred <= 0.1:
                    if stock>=size:
                        money+=end*size
                        stock-=1*size
                if pred <= 0.4:
                    if stock>=size:
                        money+=end*size
                        stock-=1*size
                profit.append((money+stock*end)/100000000)
                hold.append(stock*end)
            print(name,targets,"현금",money,"보유주식수",stock,"총자산가치",money+stock*end,"수익률",(money+stock*end)/100000000)
            profitdata['A'+str(stock_code_list['stock_code'][i][1:])]=profit
            holding['A'+str(stock_code_list['stock_code'][i][1:])]=hold
            meansu.append((money+stock*end)/100000000)
                
            
    finally:
        conn.close()
    print("종합수익율",sum(meansu)/96)
    profitdata["날짜"]=list(df_m['data_time'])[10:]
    profitdata["종합누적수익률"]=profitdata.drop(["날짜"],axis=1).sum(axis=1)/96
    holding["날짜"]=list(df_m['data_time'])[10:]

    #마지막 한행(오늘 날짜)
    profitdata = profitdata.tail(1)
    profitdata.reset_index(drop=True, inplace=True)
    holding = holding.tail(1)
    holding.reset_index(drop=True, inplace=True)


    stockai_db = pymysql.connect(host='localhost', user='root', password='aivle', db='stockai', charset='utf8')
    profitdata_columns_list = ['날짜', '종합누적수익률', 'A000060', 'A000100', 'A000270', 'A000660', 'A000720', 'A000810','A003490', 'A003550', 'A003670', 'A004020', 'A004990', 'A005380','A005490', 'A005830', 'A005930', 'A005935', 'A005940', 'A006400','A006800', 'A007070', 'A008560', 'A008770', 'A009150', 'A009540','A009830', 'A010130', 'A010140', 'A010620', 'A010950', 'A011070','A011170', 'A011200', 'A011780', 'A011790', 'A012330', 'A012450','A015760', 'A016360', 'A017670', 'A018260', 'A018880', 'A021240','A024110', 'A028050', 'A028260', 'A028300', 'A029780', 'A030200','A032640', 'A032830', 'A033780', 'A034020', 'A034220', 'A034730','A035250', 'A035420', 'A035720', 'A036460', 'A036570', 'A047810','A051900', 'A051910', 'A055550', 'A066570', 'A066970', 'A068270','A071050', 'A078930', 'A086280', 'A086790', 'A088980', 'A090430','A091990', 'A096770', 'A097950', 'A105560', 'A128940', 'A137310','A138040', 'A161390', 'A207940', 'A241560', 'A247540', 'A251270','A259960', 'A267250', 'A271560', 'A282330', 'A293490', 'A302440','A316140', 'A323410', 'A326030', 'A329180', 'A352820', 'A361610']
    holding_columns_list = ['날짜', 'A000060', 'A000100', 'A000270', 'A000660', 'A000720', 'A000810','A003490', 'A003550', 'A003670', 'A004020', 'A004990', 'A005380','A005490', 'A005830', 'A005930', 'A005935', 'A005940', 'A006400','A006800', 'A007070', 'A008560', 'A008770', 'A009150', 'A009540','A009830', 'A010130', 'A010140', 'A010620', 'A010950', 'A011070','A011170', 'A011200', 'A011780', 'A011790', 'A012330', 'A012450','A015760', 'A016360', 'A017670', 'A018260', 'A018880', 'A021240','A024110', 'A028050', 'A028260', 'A028300', 'A029780', 'A030200','A032640', 'A032830', 'A033780', 'A034020', 'A034220', 'A034730','A035250', 'A035420', 'A035720', 'A036460', 'A036570', 'A047810','A051900', 'A051910', 'A055550', 'A066570', 'A066970', 'A068270','A071050', 'A078930', 'A086280', 'A086790', 'A088980', 'A090430','A091990', 'A096770', 'A097950', 'A105560', 'A128940', 'A137310','A138040', 'A161390', 'A207940', 'A241560', 'A247540', 'A251270','A259960', 'A267250', 'A271560', 'A282330', 'A293490', 'A302440','A316140', 'A323410', 'A326030', 'A329180', 'A352820', 'A361610']


    try:
        curs = stockai_db.cursor()
        #AIRate insert
        sql = "INSERT INTO AIRate(date_time, synthesis_rate, A000060, A000100, A000270, A000660, A000720, A000810, A003490, A003550, A003670, A004020, A004990, A005380, A005490, A005830, A005930, A005935, A005940, A006400, A006800, A007070, A008560, A008770, A009150, A009540, A009830, A010130, A010140, A010620, A010950, A011070, A011170, A011200, A011780, A011790, A012330, A012450, A015760, A016360, A017670, A018260, A018880, A021240, A024110, A028050, A028260, A028300, A029780, A030200,A032640, A032830, A033780, A034020, A034220, A034730, A035250, A035420, A035720, A036460, A036570, A047810, A051900, A051910, A055550, A066570, A066970, A068270, A071050, A078930, A086280, A086790, A088980, A090430,A091990, A096770, A097950, A105560, A128940, A137310, A138040, A161390, A207940, A241560, A247540, A251270,A259960, A267250, A271560, A282330, A293490, A302440,A316140, A323410, A326030, A329180, A352820, A361610) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        for i in range(0,profitdata.shape[0]):
            tem_list =[]
            for x in profitdata_columns_list:
                tem_list.append(profitdata[x][i])
            curs.execute(sql, (tem_list))
        stockai_db.commit()
    
        #AIFunds insert
        sql = "INSERT INTO AIFunds(date_time, A000060, A000100, A000270, A000660, A000720, A000810, A003490, A003550, A003670, A004020, A004990, A005380, A005490, A005830, A005930, A005935, A005940, A006400, A006800, A007070, A008560, A008770, A009150, A009540, A009830, A010130, A010140, A010620, A010950, A011070, A011170, A011200, A011780, A011790, A012330, A012450, A015760, A016360, A017670, A018260, A018880, A021240, A024110, A028050, A028260, A028300, A029780, A030200,A032640, A032830, A033780, A034020, A034220, A034730, A035250, A035420, A035720, A036460, A036570, A047810, A051900, A051910, A055550, A066570, A066970, A068270, A071050, A078930, A086280, A086790, A088980, A090430,A091990, A096770, A097950, A105560, A128940, A137310, A138040, A161390, A207940, A241560, A247540, A251270,A259960, A267250, A271560, A282330, A293490, A302440,A316140, A323410, A326030, A329180, A352820, A361610) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        for i in range(0,holding.shape[0]):
            tem_list =[]
            for x in holding_columns_list:
                tem_list.append(holding[x][i])
            curs.execute(sql, (tem_list))
        stockai_db.commit()
    finally:
        stockai_db.close()
        print("데이터저장 완료!")

MacroeconomicIndicators_day_update(start_date)
StockData_day_update(start_date)
NaverNews_day_update(start_date)
invest_value_update(now_date)

ModelResult_update(start_date)
AIRate_AIFunds_update(start_date)








#실행부분

# def oik():
#     print(str(datetime.now()) + ' 대기중...')


# run_time = "13:13"

# schedule.every(5).seconds.do(oik)

# #월
# schedule.every().monday.at(run_time).do(MacroeconomicIndicators_day_update,start_date)
# schedule.every().monday.at(run_time).do(StockData_day_update,start_date)
# schedule.every().monday.at(run_time).do(NaverNews_day_update,start_date)
# schedule.every().monday.at(run_time).do(invest_value_update,now_date)
# schedule.every().monday.at(run_time).do(short_model_create)
# schedule.every().monday.at(run_time).do(long_model_create)
# schedule.every().monday.at(run_time).do(ModelResult_update,start_date)
# schedule.every().monday.at(run_time).do(AIRate_AIFunds_update,start_date)

# #화
# schedule.every().tuesday.at(run_time).do(MacroeconomicIndicators_day_update,start_date)
# schedule.every().tuesday.at(run_time).do(StockData_day_update,start_date)
# schedule.every().tuesday.at(run_time).do(NaverNews_day_update,start_date)
# schedule.every().tuesday.at(run_time).do(invest_value_update,now_date)
# schedule.every().tuesday.at(run_time).do(ModelResult_update,start_date)
# schedule.every().tuesday.at(run_time).do(AIRate_AIFunds_update,start_date)

# #수
# schedule.every().wednesday.at(run_time).do(MacroeconomicIndicators_day_update,start_date)
# schedule.every().wednesday.at(run_time).do(StockData_day_update,start_date)
# schedule.every().wednesday.at(run_time).do(NaverNews_day_update,start_date)
# schedule.every().wednesday.at(run_time).do(invest_value_update,now_date)
# schedule.every().wednesday.at(run_time).do(ModelResult_update,start_date)
# schedule.every().wednesday.at(run_time).do(AIRate_AIFunds_update,start_date)

# #목
# schedule.every().thursday.at(run_time).do(MacroeconomicIndicators_day_update,start_date)
# schedule.every().thursday.at(run_time).do(StockData_day_update,start_date)
# schedule.every().thursday.at(run_time).do(NaverNews_day_update,start_date)
# schedule.every().thursday.at(run_time).do(invest_value_update,now_date)
# schedule.every().thursday.at(run_time).do(ModelResult_update,start_date)
# schedule.every().thursday.at(run_time).do(AIRate_AIFunds_update,start_date)

# #금
# schedule.every().friday.at(run_time).do(MacroeconomicIndicators_day_update,start_date)
# schedule.every().friday.at(run_time).do(StockData_day_update,start_date)
# schedule.every().friday.at(run_time).do(NaverNews_day_update,start_date)
# schedule.every().friday.at(run_time).do(invest_value_update,now_date)
# schedule.every().friday.at(run_time).do(ModelResult_update,start_date)
# schedule.every().friday.at(run_time).do(AIRate_AIFunds_update,start_date)



########################################테스트
# schedule.every().thursday.at(run_time).do(MacroeconomicIndicators_day_update,start_date)
# schedule.every().thursday.at(run_time).do(StockData_day_update,start_date)
# schedule.every().thursday.at(run_time).do(NaverNews_day_update,start_date)
# schedule.every().thursday.at(run_time).do(invest_value_update,now_date)
# schedule.every().thursday.at(run_time).do(ModelResult_update,start_date)
# schedule.every().thursday.at(run_time).do(AIRate_AIFunds_update,start_date)


# while True:
#     schedule.run_pending()
#     time.sleep(1)

