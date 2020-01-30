#!/usr/bin/python3
#-*- coding: utf-8 -*-

import requests
import time
import os
import sys
import json
from lxml import etree

def area():
    ans = ''
    
    overall_url = "https://lab.isaaclin.cn/nCoV/api/overall"
    html = requests.get(overall_url)
    html.encoding = 'utf-8'
    data = json.loads(html.text)
    nation_confirmedCount = data['results'][0]['confirmedCount']
    nation_suspectedCount = data['results'][0]['suspectedCount']
    nation_deadCount = data['results'][0]['deadCount']
    nation_curedCount = data['results'][0]['curedCount']
    _time = time.strftime('%Y-%m-%d %H:%M', time.localtime())

    area_url = "https://lab.isaaclin.cn/nCoV/api/area"
    html = requests.get(area_url)
    html.encoding = 'utf-8'
    data = json.loads(html.text)

    ans += '{0:^6}\t确诊:{1:^6}\t疑似:{2:^6}\t治愈:{3:^6}\t死亡:{4:^6}'.format('全国', nation_confirmedCount, nation_suspectedCount, nation_curedCount, nation_deadCount)

    provinceShortName = []
    confirmedCount = []
    suspectedCount = []
    curedCount = []
    deadCount = []

    for i in data['results']:
        if i['country'] == '中国':
            provinceShortName.append(i['provinceShortName'])
            confirmedCount.append(i['confirmedCount'])
            suspectedCount.append(i['suspectedCount'])
            curedCount.append(i['curedCount'])
            deadCount.append(i['deadCount'])

    for i in range(0, len(confirmedCount) - 1):
        for j in range(i + 1, len(confirmedCount)):
            if confirmedCount[i] < confirmedCount[j]:
                confirmedCount[i], confirmedCount[j] = confirmedCount[j], confirmedCount[i]
                provinceShortName[i], provinceShortName[j] = provinceShortName[j], provinceShortName[i]
                suspectedCount[i], suspectedCount[j] = suspectedCount[j], suspectedCount[i]
                curedCount[i], curedCount[j] = curedCount[j], curedCount[i]
                deadCount[i], deadCount[j] = deadCount[j], deadCount[i]

    for i in range(0, len(confirmedCount)):
        ans += '{0:^6}\t确诊:{1:^6}\t疑似:{2:^6}\t治愈:{3:^6}\t死亡:{4:^6}'.format(provinceShortName[i], confirmedCount[i], suspectedCount[i], curedCount[i], deadCount[i])

    provinceShortName = []
    confirmedCount = []
    suspectedCount = []
    curedCount = []
    deadCount = []

    ans += ('===全球===')

    for i in data['results']:
        if i['country'] != '中国':
            provinceShortName.append(i['provinceShortName'])
            confirmedCount.append(i['confirmedCount'])
            suspectedCount.append(i['suspectedCount'])
            curedCount.append(i['curedCount'])
            deadCount.append(i['deadCount'])

    for i in range(0, len(confirmedCount) - 1):
        for j in range(i + 1, len(confirmedCount)):
            if confirmedCount[i] < confirmedCount[j]:
                confirmedCount[i], confirmedCount[j] = confirmedCount[j], confirmedCount[i]
                provinceShortName[i], provinceShortName[j] = provinceShortName[j], provinceShortName[i]
                suspectedCount[i], suspectedCount[j] = suspectedCount[j], suspectedCount[i]
                curedCount[i], curedCount[j] = curedCount[j], curedCount[i]
                deadCount[i], deadCount[j] = deadCount[j], deadCount[i]

    for i in range(0, len(confirmedCount)):
        ans += '{0:^6}\t确诊:{1:^6}\t疑似:{2:^6}\t治愈:{3:^6}\t死亡:{4:^6}'.format(provinceShortName[i], confirmedCount[i], suspectedCount[i], curedCount[i], deadCount[i])

    return ans