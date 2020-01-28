#!/usr/bin/python
#-*- coding: utf-8 -*-

import requests
import time
import os
import sys
import json
from lxml import etree

def area():
    ans = ''
    url = "https://3g.dxy.cn/newh5/view/pneumonia_peopleapp?from=timeline&isappinstalled=0"
    request_headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
    html = requests.get(url, headers=request_headers)
    html.encoding = 'utf-8'
    content = etree.HTML(html.text)
    number = content.xpath('//*[@id="getAreaStat"]')
    data_time = content.xpath('//*[@id="root"]/div/div[3]/div[1]/p[1]/span')
    nation_confirmedCount = content.xpath('//*[@id="root"]/div/div[3]/div[1]/p[2]/span/span[1]/span')
    nation_suspectedCount = content.xpath('//*[@id="root"]/div/div[3]/div[1]/p[2]/span/span[2]/span')
    nation_deadCount = content.xpath('//*[@id="root"]/div/div[3]/div[1]/p[2]/span/span[3]/span')
    nation_curedCount = content.xpath('//*[@id="root"]/div/div[3]/div[1]/p[2]/span/span[4]/span')
    data = number[0].text[27:-11]

    with open('content.html', 'w') as f:
        f.write(html.text)
        f.close()
    with open('number.json', 'w') as f:
        f.write(data)
        f.close()

    data = json.loads(data)

    print(data_time[0].text)
    #print('{0:^6}\t确诊:{1:^6}\t疑似:{2:^6}\t治愈:{3:^6}\t死亡:{4:^6}'.format('全国', nation_confirmedCount[0].text, nation_suspectedCount[0].text, nation_curedCount[0].text, nation_deadCount[0].text))
    ans += '{0:^6}\t确诊:{1:^6}\t疑似:{2:^6}\t治愈:{3:^6}\t死亡:{4:^6}'.format('全国', nation_confirmedCount[0].text, nation_suspectedCount[0].text, nation_curedCount[0].text, nation_deadCount[0].text)
    for i in data:
        provinceShortName = i['provinceShortName']
        confirmedCount = i['confirmedCount']
        suspectedCount = i['suspectedCount']
        curedCount = i['curedCount']
        deadCount = i['deadCount']
        #print('省份:{0:^6}\t确诊:{1:^6}\t疑似:{2:^6}\t治愈:{3:^6}\t死亡:{4:^6}'.format(provinceShortName, confirmedCount, suspectedCount, curedCount, deadCount))
        ans += '省份:{0:^6}\t确诊:{1:^6}\t疑似:{2:^6}\t治愈:{3:^6}\t死亡:{4:^6}'.format(provinceShortName, confirmedCount, suspectedCount, curedCount, deadCount)

    return ans