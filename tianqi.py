# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 11:48:58 2020

@author: ZAN
"""
import os

import requests
import pandas as pd
from bs4 import BeautifulSoup
from collections import defaultdict
from dateutil.relativedelta import relativedelta
from datetime import datetime
import numpy as np


class weather_data:
    def __init__(self, city, start_year, end_year, start_month=1, end_month=12, FilePath='./test.csv'):
        """

        :param city: 需爬取的城市全拼
        :param start_year: 爬取开始年份
        :param end_year: 爬取结束年份
        :param start_month: 爬取开始月份
        :param end_month: 爬取结束月份
        """
        self.city = city
        self.start_time = datetime.strptime(f"{start_year}-{start_month}", '%Y-%m')
        self.end_time = datetime.strptime(f"{end_year}-{end_month}", '%Y-%m')
        self.FilePath = FilePath

    def _get_parse_html(self):
        """
            网页爬取并解析
        """

        url = f"https://tianqi.911cha.com/{self.city}/{self.start_time.year}-{self.start_time.month}.html"
        print(url)
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"}  # 填写自己浏览器内容
        response = requests.get(url, headers=header)
        # return response.content.decode("utf-8")
        # 一次解析一个月
        soup = BeautifulSoup(response.content.decode("utf-8"), "html.parser")
        df = pd.DataFrame(columns=['日期', '时间', '图片', '天气', '温度℃', '湿度', '风力', '风级', '降水量mm', '体感温度℃', '云量'])
        date = ''
        for n, tr in enumerate(soup.find_all("tr")):
            # 首行为字段行，无数据
            if n == 0:
                continue
                # 奇数行，白天
            if n % 2 != 0:
                date = tr.find("a").get_text()
                data = {key: con.get_text() for key, con in zip(
                    ['时间', '图片', '天气', '温度℃', '湿度', '风力', '风级',
                     '降水量mm', '体感温度℃', '云量'], tr.find_all("td"))}
                data['日期'] = date
                df2 = pd.DataFrame([data])
                df2['日期'] = pd.to_datetime(str(self.start_time.year) + '年' + df2['日期'], format='%Y年%m月%d日')
                df2['温度℃'] = df2['温度℃'].str.strip('℃')
                df2['体感温度℃'] = df2['体感温度℃'].str.strip('℃')
                df2['风级'] = df2['风级'].str.strip('级')
                try:
                    df2['降水量mm'] = df2['降水量mm'].str.strip('mm')
                except:
                    print('当天无降水')
                df2['降水量mm'].replace('-', 0, inplace=True)
                df = df.append(df2, ignore_index=True)

            else:
                # 偶数行，夜间
                data = {key: con.get_text() for key, con in zip(
                    ['时间', '图片', '天气', '温度℃', '湿度', '风力', '风级',
                     '降水量mm', '体感温度℃', '云量'], tr.find_all("td"))}
                data['日期'] = date
                df2 = pd.DataFrame([data])
                df2 = pd.DataFrame([data])
                df2['日期'] = pd.to_datetime(str(self.start_time.year) + '年' + df2['日期'], format='%Y年%m月%d日')
                df2['温度℃'] = df2['温度℃'].str.strip('℃')
                df2['体感温度℃'] = df2['体感温度℃'].str.strip('℃')
                df2['风级'] = df2['风级'].str.strip('级')
                try:
                    df2['降水量mm'] = df2['降水量mm'].str.strip('mm')
                except:
                    print('当天无降水')
                df2['降水量mm'].replace('-', 0, inplace=True)
                df = df.append(df2, ignore_index=True)
            # print(df)
        flag = os.path.isfile(self.FilePath)
        if not flag:
            # 文件不存在
            df.to_csv(self.FilePath, mode='a', header=True, encoding='utf_8_sig')
        else:
            # 文件存在
            df.to_csv(self.FilePath, mode='a', header=False, encoding='utf_8_sig')
        print('写入数据完成')

    def main(self):

        while self.start_time <= self.end_time:
            self._get_parse_html()
            self.start_time += relativedelta(months=1)


if __name__ == "__main__":
    city = "hexi"
    start_year = 2019
    start_month = 1
    end_year = 2020
    end_month = 7
    File_Path = './天津市{}区天气{}-{}至{}-{}.csv'.format(city,start_year,start_month,end_year,end_month)
    T = weather_data(city=city, start_year=start_year, end_year=end_year, start_month=start_month, end_month=end_month,FilePath=File_Path)
    T.main()
