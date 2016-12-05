#!/usr/bin/env python3
# -*- coding:euc-kr -*-

import requests, time
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import SQL_util, init, class_article

# 연도별 통계 계산용 함수
# def count_year(press, years):
#     chk_data = 'count(*)'
#     option = " press = '" + press + "' and years = " + str(years)
#
#     chk = SQL_util.select(chk_data, 'year_count', option)
#     if(chk.fetchone()[0] == 0):
#         input_data = " '" + press + "', 1, " + str(years) + " "
#         SQL_util.insert_count(input_data, ' year_count ')
#     else:
#         input_data = ' cnt = cnt+1 '
#         SQL_util.update_count(input_data, 'year_count', option)
#
# # 월별 통계 계산용 함수
# def count_month(press, months):
#     chk_data = 'count(*)'
#     option = " press = '" + press + "' and months = " + str(months)
#
#     chk = SQL_util.select(chk_data, 'month_count', option)
#     if(chk.fetchone()[0] == 0):
#         input_data = " '" + press + "', 1, " + str(months) + " "
#         SQL_util.insert_count(input_data, ' month_count ')
#     else:
#         input_data = ' cnt = cnt+1 '
#         SQL_util.update_count(input_data, 'month_count', option)
#
# # 일자별 통계 계산용 함수
# def count_date(press, dates):
#     chk_data = 'count(*)'
#     option = " press = '" + press + "' and dates = " + str(dates)
#
#     chk = SQL_util.select(chk_data, 'date_count', option)
#     if(chk.fetchone()[0] == 0):
#         input_data = " '" + press + "', 1, " + str(dates) + " "
#         SQL_util.insert_count(input_data, ' date_count ')
#     else:
#         input_data = ' cnt = cnt+1 '
#         SQL_util.update_count(input_data, 'date_count', option)

# 단독 기사 조건 필터링
def isDandok(title):
    for dandock_item in init.dandok:
        if title.find(dandock_item) > -1:
            return True
    return False


# def politician(title, summ, part):
#     for poli in politicians:
#         code = poli[0]
#         name = poli[1]
#
#         if title.find(name) > -1 or summ.find(name) > -1:
#             option = 'part = ' + str(part) + ', politician_code = ' + str(code)
#             SQL_util.update('politician_part ', ' cnt = cnt + 1 ', option)
#             SQL_util.update('politician ', ' total_count = total_count + 1 ', ' politician_code = ' + str(code))


def isUpdating(url):
    flg_cur = SQL_util.select('count(*)', 'articles', "article_url ='"+url+"'")
    flg = flg_cur.fetchone()[0]
    if flg > 0:
        return True
    else:
        return False

def sleeping():
    time.sleep(1)

# 크롤링 함수
def spider(url, part):
    # nowtime = datetime.now()
    # nowtime_str = nowtime.strftime('%Y-%m-%d')
    standard_time = '2016-10-06'

    t_url = url.replace('stDt', standard_time)
    t_url = t_url.replace('enDt=', standard_time)


    source_code = requests.get(t_url)
    t_file = source_code.text
    soup = BeautifulSoup(t_file, 'html.parser')
    last_page = 1

    for page_item in soup.find_all('span', 'result_num'):
        num = page_item.text.replace('	','').replace('건','').replace('(','').replace(')','').replace(' ','').split('/')[-1]
        last_page = int(int(num) / 10) + 1

    for page_flag in range(1, last_page):

        nowtime = datetime.now()
        nowtime_str = nowtime.strftime('%Y-%m-%d')
        #nowtime_str = '2016-10-01'
        # print(part, " // ", standard_time, ' // ', page_flag)
        page_tag = '&page='+str(page_flag)
        t_url = url.replace('&page=1', page_tag)
        t_url = t_url.replace('stDt', standard_time)
        t_url = t_url.replace('enDt=', standard_time)
        # t_url = t_url.replace('20160609', nowtime_str)
        # t_url = t_url.replace('20160609', nowtime_str)


        title_list = []; title_href_list = []; press_list = []
        time_list = []; sum_list = []; image_src_list = []
        try:
            source_code = requests.get(t_url)
            t_file = source_code.text
            soup = BeautifulSoup(t_file, 'html.parser')

            # Crawling title
            for tt in (soup.find_all('a', 'tit')):
                href = tt.get('href')
                title = tt.text
                title = title.replace("'", '')
                title = title.replace('"', '')

                title_href_list.append(href)
                title_list.append(title)
                image_src_list.append('None')
                #print(title_list)

            # Crawling press
            for pr in (soup.find_all('span', 'press')):
                press = pr.text
                press_list.append(press)

            # Crawling summary
            for sum in (soup.find_all('p', 'dsc')):
                summ = '' + sum.text[6:]
                summ = summ.replace("'", '')
                summ = summ.replace('"', '')

                sum_list.append(summ)

            # Crawling time
            for tm in (soup.find_all('span', 'time')):
                time_t = tm.text

                if time_t.find(init.sigan) > 0:
                    d_point = time_t.find(init.sigan)
                    time_d = int(time_t[0:d_point])
                    time_d = timedelta(hours=time_d)
                    reported_time = nowtime - time_d
                    R_time = reported_time.strftime('%Y-%m-%d %H:%M')

                elif time_t.find(init.bun) > 0:
                    d_point = time_t.find(init.bun)
                    time_d = int(time_t[0:d_point])
                    time_d = timedelta(minutes=time_d)
                    reported_time = nowtime - time_d
                    R_time = reported_time.strftime('%Y-%m-%d %H:%M')

                elif time_t.find(init.il) > 0:
                    d_point = time_t.find(init.il)
                    time_d = int(time_t[0:d_point])
                    time_d = timedelta(hours=24*time_d)
                    reported_time = nowtime - time_d
                    R_time = reported_time.strftime('%Y-%m-%d %H:%M')

                elif time_t.find(init.cho) > 0:
                    d_point = time_t.find(init.cho)
                    time_d = int(time_t[0:d_point])
                    time_d = timedelta(seconds=time_d)
                    reported_time = nowtime - time_d
                    R_time = reported_time.strftime('%Y-%m-%d %H:%M')

                else:
                    R_time = standard_time

                time_list.append(R_time)
                # reported_time = nowtime - time_d
                #
                # R_time = reported_time.strftime('%Y-%m-%d %H:%M')
                # time_list.append(R_time)


            for i in range(0, title_list.__len__()):
                this_article = class_article.Article(title_list[i], press_list[i],
                                sum_list[i], time_list[i], '', title_href_list[i], part)
                if (isDandok(this_article.title)):
                    # print('\t', this_article.title)
                    # print('\t', this_article.report_time, this_article.press)
                    if(isUpdating(this_article.url)):
                        set_sentence = " title = '"+this_article.title+"' "
                        option = " article_url = '"+this_article.url+"' "
                        SQL_util.update(set_sentence, 'articles', option)
                    else:
                        SQL_util.insert(this_article.to_dbdata(), 'articles')
                        # politician(this_article.title, this_article.summ, this_article.part)
                        # count_year(this_article.press, this_article.years)
                        # count_month(this_article.press, this_article.months)
                        # count_date(this_article.press, this_article.dates)

            page_tag = '&page='+(str(page_flag))

        except:
            print('\t', page_flag, 'exception')
            continue

# name_cur = SQL_util.select('politician_code, name', 'politician')
# politicians = [[code, name] for code, name in name_cur.fetchall()]

a = 1

while(True):

    print(a, '-----------------------------------------------')
    url_cursor = SQL_util.select('*', 'target_site', 'part > 0 order by part')
    for url in url_cursor:
        spider(url[1], url[0])
        time.sleep(2)
    print(a, 'th is finished---------------------------------')
    a += 1


