import requests
from bs4 import BeautifulSoup
import re
import json
import time
import logging
import datetime
from database import DB


r = requests.get("https://lab.isaaclin.cn/nCoV/")

info = {'user-agent': 'Chrome'}

class Spider:

    def __init__(self):
        self.session = requests.session()
        self.session.headers.update(info)
        self.db = DB()
        self.timestamp = int()

    def spider(self):
        url = "https://3g.dxy.cn/newh5/view/pneumonia"

        while True:
            self.timestamp = int(datetime.datetime.timestamp(datetime.datetime.now()) * 1000)

            try:
                r = self.session.get(url=url)
            except requests.exceptions.ChunkedEncodingError:
                continue
            soup = BeautifulSoup(r.content, 'lxml')

            sum_info = re.search(r'\{("id".*?)\]\}', str(soup.find('script', attrs={'id': 'getStatisticsService'})))
            province_info = re.search(r'\[(.*?)\]', str(soup.find('script', attrs={'id': 'getListByCountryTypeService1'})))
            area_info = re.search(r'\[(.*)\]', str(soup.find('script', attrs={'id': 'getAreaStat'})))

            if not any([sum_info, province_info, area_info]):
                continue
            self.sum_info_parser(sum_info)

            break


    def sum_info_parser(self, sum_info):
        sum_info = json.loads(sum_info.group(0))
        sum_info.pop('id')
        sum_info.pop('createTime')
        sum_info.pop('modifyTime')
        sum_info.pop('imgUrl')
        sum_info.pop('deleted')
        sum_info.pop('')
        sum_info['countRemark'] = sum_info['countRemark']
        if not self.db.find_one(collection='Sum_info', data=sum_info):
            sum_info['updateTime'] = self.timestamp
            self.db.insert(collection="Sum_info", data=sum_info)

    def province_info_parser(self, province_info):
        province = json.loads(province_info.group(0))
        for p in province:
            p.pop('id')
            p.pop('tags')
            p.pop('sort')
            if self.db.find_one(collection='Province', data=p):
                continue
            p['crawlTime'] = self.timestamp
            p['country'] = 'China'

    def area_info_parser(self, area_info):
        area = json.loads(area_info.group(0))
        for a in area:
            if self.db.find_one(collection='Area', data=a):
                continue
            area['country'] = 'China'
            area['updateTime'] = self.timestamp


# if __name__ == "__main__":
#     s = Spider()
#     s.spider()