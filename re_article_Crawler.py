#!/usr/bin/env python3
# -*- coding:euc-kr -*-

import requests, time
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import SQL_util, init, class_article


def pressStat(report_time, press, part):
    yrs = int(report_time.split(' ')[0].split('-')[0])
    mth = int(report_time.split(' ')[0].split('-')[1])
    dts = int(report_time.split(' ')[0].split('-')[2])

    table = ' press_stat(press, yrs, mth, dts, p' +str(part) + ' ) '
    data = "'"+press+"', "+str(yrs)+", "+str(mth)+", "+str(dts)+",1"
    if SQL_util.insert(data, table) == False:
        setting = 'total = total + 1'
        table = 'press_stat'
        option = "press = '"+press+"' and yrs = "+str(yrs) + " and mth =" + str(mth) + ' and dts = '+str(dts)
        SQL_util.update(set=setting, table=table, option=option)


def politicianStat(title, part):
    for poli in politicians:
        code = poli[0]
        name = poli[1]
        if title.find(name) > -1:

            option = 'part = ' + str(part) + ' and politician_code = ' + str(code)
            SQL_util.update(' cnt = cnt + 1 ', 'politician_part ', option)
            SQL_util.update(' total_count = total_count + 1 ', 'politician ', ' politician_code = ' + str(code))


def orgStat(title, part):
    if part > 3:
        return False
    for org_item in orgs:
        code = org_item[0]
        if code == 1:
            names = []
            names.append(org_item[1])
            names.append(org_item[1].replace('당', ''))


        elif code == 2:
            names = []
            names.append(org_item[1])
            names.append(org_item[1].replace('당', ''))
            names.append('더민주')
            names.append('더민주당')

        else:
            names = []
            names.append(org_item[1])

        for name in names:
            if title.find(name) > -1:
                option = 'org_code = ' + str(code) + ' and part = ' + str(part)
                setting = 'cnt = cnt+1'
                table = 'org_part'
                SQL_util.update(setting, table, option)
                option = 'org_code = ' + str(code)
                setting = 'total_count = total_count + 1'
                table = 'org'
                SQL_util.update(setting, table, option)
                break


# 단독 기사 조건 필터링
def isDandok(title):
    for dandock_item in init.dandok:
        if title.find(dandock_item) > -1:
            return True
    return False

def isNew(url):
    flg_cur = SQL_util.select('count(*)', 'articles', "article_url ='" + url + "'")
    flg = flg_cur.fetchone()[0]
    if flg > 0:
        return False
    else:
        return True

def isUpdating(url, title):
    flg_cur = SQL_util.select('count(*)', 'articles', "article_url ='"+url+"' and title <> '"+title+"'")
    flg = flg_cur.fetchone()[0]
    if flg > 0:
        return True
    else:
        return False


# 크롤링 함수
def spider(url, part):

    page_tag = '&page='+str(1)

    nowtime = datetime.now()
    nowtime_str = nowtime.strftime('%Y-%m-%d')
    #standtime_str = '2016-10-09'

    t_url = url.replace('&page=1', page_tag)
    t_url = t_url.replace('stDt', nowtime_str)
    t_url = t_url.replace('enDt=', nowtime_str)
    #t_url = t_url.replace('stDt', standtime_str)
    #t_url = t_url.replace('enDt=', standtime_str)

    source_code = requests.get(t_url)
    t_file = source_code.text
    soup = BeautifulSoup(t_file, 'html.parser')
    last_page = 1

    for page_item in soup.find_all('span', 'result_num'):
        num = page_item.text.replace('	', '').replace('\n','').replace('건', '').replace('(', '').replace(')', '').replace(' ', '').split('/')[-1]
        last_page = int(int(num) / 10) + 1

    for page_flag in range(1, last_page+1):

        nowtime = datetime.now()
        nowtime_str = nowtime.strftime('%Y-%m-%d')

        print(part, " // ", nowtime_str, ' // ', page_flag)
        page_tag = '&page='+str(page_flag)
        t_url = url.replace('&page=1', page_tag)
        t_url = t_url.replace('stDt', nowtime_str)
        t_url = t_url.replace('enDt=', nowtime_str)
        #t_url = t_url.replace('stDt', standtime_str)
        #t_url = t_url.replace('enDt=', standtime_str)


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
                    time_d = timedelta(hours=24*0)

                reported_time = nowtime - time_d

                R_time = reported_time.strftime('%Y-%m-%d %H:%M')
                time_list.append(R_time)


            for i in range(0, title_list.__len__()):
                this_article = class_article.Article(title_list[i], press_list[i],
                                sum_list[i], time_list[i], title_href_list[i], part)
                if (isDandok(this_article.title)):
                    print(this_article.title, this_article.press, this_article.part)
                    if (isNew(this_article.url)):
                        tables = 'articles(title, press, summary, report_time, article_url, part)'
                        SQL_util.insert(this_article.to_dbdata(), tables)
                        politicianStat(this_article.title, this_article.part)
                        pressStat(this_article.report_time, this_article.press, this_article.part)
                        orgStat(this_article.title, this_article.part)
                    else:
                        if(isUpdating(this_article.url, this_article.title)):
                            set_sentence = " title = '"+this_article.title+"' "
                            option = " url = '"+this_article.url+"' "
                            SQL_util.update(set_sentence, 'articles', option)




        except:
            print('\t', page_flag, 'exception')
            continue

pol_cur = SQL_util.select('politician_code, name', 'politician')
politicians = [[code, name] for code, name in pol_cur.fetchall()]

org_cur = SQL_util.select('org_code, org_name', 'org')
orgs = [[code, org_name] for code, org_name in org_cur.fetchall()]

a = 1

while(True):

    print(a, '-----------------------------------------------')
    url_cursor = SQL_util.select('*', 'target_site', 'part > 0 order by part')
    for url in url_cursor:
        spider(url[1], url[0])
        time.sleep(2)
    print(a, 'th is finished---------------------------------')
    a += 1
    time.sleep(860)

