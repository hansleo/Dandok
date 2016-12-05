#-*- coding:utf8 -*-
import pymysql
import sys
#
# reload(sys)
# sys.setdefaultencoding('utf-8')


conn = pymysql.connect(host='localhost', port=, user=, passwd=, db=, charset='utf8')


def select(data, table, option=''):
    curs = conn.cursor()
    command = "SELECT " + str(data) + " FROM " + table + ' '
    if str(option) != '':
        command += ' WHERE '
        command += str(option)
    command += ';'
    #print(command)
    curs.execute(command)

    return curs


def insert(data, table):
    curs = conn.cursor()
    command = "INSERT INTO " + table + " VALUES( " + data + " ) ;"
    try:
        curs.execute(command)
        #print('command', command)
        conn.commit()
        return True
    except:
        #print('error')
        #print('command', command)
        conn.rollback()
        return False

def insert_count(data, table):
    curs = conn.cursor()
    command = "INSERT INTO " + table + " VALUES( " + data + " ) ;"
    try:
        curs.execute(command)
        # print('command', command)
        conn.commit()
    except:
        print('error')
        print('command', command)
        conn.rollback()

def update(set, table, option):
    curs = conn.cursor()
    command = "UPDATE " + table + " SET " + set + " WHERE " + option + ' ;'
    try:
        curs.execute(command)
        #print('command', command)
        conn.commit()
    except:
        print('error')
        print('command', command)
        conn.rollback()
