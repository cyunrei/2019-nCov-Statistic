import matplotlib.pyplot as plt
import requests
import json
import time
import sys
import pandas as pd
from lxml import etree
from data import dead
from data import suspected
from data import cured
from data import confirmed

def graph():
    plt.rcParams['font.family'] = ['Source Han Sans CN']
    plt.rcParams['savefig.format'] = 'png'
    plt.rcParams['figure.figsize'] = (16.0, 8.0)
    plt.rcParams['savefig.dpi'] = 100
    plt.rcParams['figure.dpi'] = 100
    url = "https://3g.dxy.cn/newh5/view/pneumonia_peopleapp?from=timeline&isappinstalled=0"
    request_headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
    response = requests.get(url, headers=request_headers)
    response.encoding = 'utf-8'
    html = etree.HTML(response.text)

    area_stat = html.xpath('//*[@id="getAreaStat"]')
    _time = html.xpath('//*[@id="root"]/div/div[3]/div[1]/p[1]/span/text()')
    _time = str(_time)
    _time = _time[5:-9]
    data_list = []

    for i in range(1, 5):
        data_list.append(''.join(html.xpath(
            '//*[@id="root"]/div/div[3]/div[1]/p[2]/span/span['+str(i)+']/span/text()')))
    label_list = ['确诊（'+str(data_list[0])+'）', '疑似（'+str(
        data_list[1])+'）', '死亡（'+str(data_list[2])+'）', '治愈（'+str(data_list[3])+'）']
    confirmed[time.strftime('%m-%d', time.localtime())] = int(data_list[0])
    suspected[time.strftime('%m-%d', time.localtime())] = int(data_list[1])
    dead[time.strftime('%m-%d', time.localtime())] = int(data_list[2])
    cured[time.strftime('%m-%d', time.localtime())] = int(data_list[3])

    f1 = plt.subplot(2, 1, 1)
    f2 = plt.subplot(2, 1, 2)
    plt.sca(f1)
    color = ['red', 'orange', 'gray', 'green']
    explode = [0, 0, 0, 0.1]
    patches, l_text, p_text = plt.pie(data_list, explode=explode, colors=color, labels=label_list,
                                    labeldistance=1.1, autopct='%1.1f%%', shadow=True, startangle=90, pctdistance=0.6)
    plt.axis("equal")
    plt.title('2019-nCov 统计图 '+_time+'（北京时间）')
    plt.legend()
    plt.sca(f2)
    plt.plot(list(confirmed.keys()), list(confirmed.values()),
            marker='o', label='确诊', color='red', linewidth=3)
    plt.plot(list(suspected.keys()), list(suspected.values()),
            marker='v', label='疑似', color='orange', linewidth=3)
    plt.plot(list(cured.keys()), list(cured.values()), marker='s',
            label='治愈', color='green', linewidth=3)
    plt.plot(list(dead.keys()), list(dead.values()), marker='x',
            label='死亡', color='gray', linewidth=3)
    plt.title('2019-nCov 统计图 2019-01-11 至 ' + _time[:-6])
    title1 = '2019-nCov 统计图 '+_time+'（北京时间）'
    plt.savefig('{0}.png'.format(title1))
    plt.legend()

    with open('./data/area_stat ('+_time+').json', 'w') as f:
        f.write((area_stat[0].text)[27:-11])
        f.close()
    with open('./data/area_stat ('+_time+').json', 'r') as f:
        data = json.load(f)
    provinceShortName = []
    confirmedCount = []
    curedCount = []
    deadCount = []
    for i in data:
        provinceShortName.append(i['provinceShortName'])
        confirmedCount.append(i['confirmedCount'])
        curedCount.append(i['curedCount'])
        deadCount.append(i['deadCount'])

    provinceShortName.reverse()
    confirmedCount.reverse()
    curedCount.reverse()
    deadCount.reverse()
    df = pd.DataFrame({
        '确诊': pd.Series(confirmedCount, index=provinceShortName),
        '治愈': pd.Series(curedCount, index=provinceShortName),
        '死亡': pd.Series(deadCount, index=provinceShortName)
    })
    df.plot.barh(stacked=True, color=['red', 'green', 'black'])
    title2 = '2019-nCov 省际统计图 '+_time+'（北京时间）'
    plt.title(title2)
    plt.savefig('{0}.png'.format(title2))
    #plt.show()

    return title1, title2