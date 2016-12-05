#-*-coding:utf-8-*-
from datetime import datetime, timedelta

class Article:

    def __init__(self, title, press, summ, report_time, url, part):
        self.title = title
        self.press = press
        self.summ = summ
        self.report_time = report_time
        self.url = url
        self.part = part
        self.years = int(self.report_time[0:4])
        self.months = int(self.report_time[5:7])
        self.dates = int(self.report_time[8:10])

    def to_dbdata(self):
        data = "'"
        data += self.title + "', '"
        data += self.press + "', '"
        data += self.summ + "', '"
        data += self.report_time + "', '"
        data += self.url + "', "
        data += str(self.part) + " "
        return data

    def forCounting(self):

        return self.years, self.months, self.dates
