#!/usr/bin/env python3
# -*- coding:euc-kr -*-

import requests, time
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import SQL_util, init, class_article

# 연도별 통계 계산용 함수
def count_year(press, years):
    chk_data = 'count(*)'
    option = " press = '" + press + "' and years = " + str(years)

    chk = SQL_util.select(chk_data, 'year_count', option)
    if(chk.fetchone()[0] == 0):
        input_data = " '" + press + "', 1, " + str(years) + " "
        SQL_util.insert_count(input_data, ' year_count ')
    else:
        input_data = ' cnt = cnt+1 '
        SQL_util.update_count(input_data, 'year_count', option)

# 월별 통계 계산용 함수
def count_month(press, months):
    chk_data = 'count(*)'
    option = " press = '" + press + "' and months = " + str(months)

    chk = SQL_util.select(chk_data, 'month_count', option)
    if(chk.fetchone()[0] == 0):
        input_data = " '" + press + "', 1, " + str(months) + " "
        SQL_util.insert_count(input_data, ' month_count ')
    else:
        input_data = ' cnt = cnt+1 '
        SQL_util.update_count(input_data, 'month_count', option)

# 일자별 통계 계산용 함수
def count_date(press, dates):
    chk_data = 'count(*)'
    option = " press = '" + press + "' and dates = " + str(dates)

    chk = SQL_util.select(chk_data, 'date_count', option)
    if(chk.fetchone()[0] == 0):
        input_data = " '" + press + "', 1, " + str(dates) + " "
        SQL_util.insert_count(input_data, ' date_count ')
    else:
        input_data = ' cnt = cnt+1 '
        SQL_util.update_count(input_data, 'date_count', option)

# 단독 기사 조건 필터링
def isDandok(title):
    if((title.find(init.dandok1) > -1) or (title.find(init.dandok2) > -1 or (title.find(init.dandok6) > -1))
        or (title.find(init.dandok3) > -1) or (title.find(init.dandok4) > -1) or (title.find(init.dandok5) > -1)):

        return True

    else:
        return False


def politician(title, summ, part):
    for poli in politicians:
        code = poli[0]
        name = poli[1]

        if title.find(name) > -1 or summ.find(name) > -1:
            option = 'part = ' + str(part) + ', politician_code = ' + str(code)
            SQL_util.update('politician_part ', ' cnt = cnt + 1 ', option)
            SQL_util.update('politician ', ' total_count = total_count + 1 ', ' politician_code = ' + str(code))



# 크롤링 함수
def spider(url, part):

    page_flag = True
    page_no = 1
    page_tag = '&page='+str(page_no)

    while(page_flag):
        nowtime = datetime.now()
        nowtime_str = nowtime.strftime('%Y-%m-%d')
        #nowtime_str = '2016-10-01'
        print(part, " // ", nowtime_str, ' // ', page_no)

        t_url = url.replace('&page=1', page_tag)
        t_url = t_url.replace('stDt', nowtime_str)
        t_url = t_url.replace('enDt=', nowtime_str)
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

                option = " title ='" + title + "' and part = " + str(part)
                page_check = SQL_util.select("count(*)", 'articles', option)
                pc = page_check.fetchone()[0]
                if pc > 0:
                    page_flag = False
                    break

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
                time = tm.text

                if time.find(init.sigan) > 0:
                    d_point = time.find(init.sigan)
                    time_d = int(time[0:d_point])
                    time_d = timedelta(hours=time_d)

                elif time.find(init.bun) > 0:
                    d_point = time.find(init.bun)
                    time_d = int(time[0:d_point])
                    time_d = timedelta(minutes=time_d)

                elif time.find(init.il) > 0:
                    d_point = time.find(init.il)
                    time_d = int(time[0:d_point])
                    # time_d = int(time[0])
                    time_d = timedelta(hours=24*time_d)

                else:
                    continue

                reported_time = nowtime - time_d

                R_time = reported_time.strftime('%Y-%m-%d %H:%M')
                time_list.append(R_time)


            for i in range(0, title_list.__len__()):
                this_article = class_article.Article(title_list[i], press_list[i],
                                sum_list[i], time_list[i], '', title_href_list[i], part)
                # print('\n', i+1, this_article.title, ' ', this_article.url, ' ', this_article.press, ' ', )
                # print(this_article.summ)
                if (isDandok(this_article.title)):
                    # print('\n', i+1, this_article.title, ' ', this_article.url, ' ', this_article.press, ' ', )
                    # print(this_article.summ)

                    # option = " title ='" + this_article.title + "' and part = " + str(part)
                    # page_check = SQL_util.select("count(*)", 'articles', option)
                    # pc = page_check.fetchone()[0]
                    # print('\t', pc, ' ', option)
                    # if pc == 0:
                    #     SQL_util.insert(this_article.to_dbdata(), 'articles')
                    #     count_year(this_article.press, this_article.years)
                    #     count_month(this_article.press, this_article.months)
                    #     count_date(this_article.press, this_article.dates)
                    SQL_util.insert(this_article.to_dbdata(), 'articles')
                    politician(this_article.title, this_article.summ, this_article.part)
                    count_year(this_article.press, this_article.years)
                    count_month(this_article.press, this_article.months)
                    count_date(this_article.press, this_article.dates)


            page_no += 1
            page_tag = '&page='+(str(page_no))
            if page_no > 10:
                page_flag = False

        except:
            print('\t', page_no, 'exception')
            continue

name_cur = SQL_util.select('politician_code, name', 'politician')
politicians = [[code, name] for code, name in name_cur.fetchall()]

a = 1
while(True):

    print(a, '-----------------------------------------------')
    url_cursor = SQL_util.select('*', 'target_site')
    for url in url_cursor:
        spider(url[1], url[0])
        time.sleep(2)
    print(a, 'th is finished---------------------------------')
    a += 1
    time.sleep(860)

