import matplotlib.pyplot as plt
import requests
import json
import time
import pandas as pd
from lxml import etree
from data import dead
from data import suspected
from data import cured
from data import confirmed

def graph():
    plt.rcParams['font.family'] = ['WenQuanYi Zen Hei']
    plt.rcParams['savefig.format'] = 'png'
    plt.rcParams['figure.figsize'] = (12.0, 7.0)
    plt.rcParams['savefig.dpi'] = 200
    plt.rcParams['figure.dpi'] = 200
    url = "https://3g.dxy.cn/newh5/view/pneumonia_peopleapp?from=timeline&isappinstalled=0"
    request_headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}

    # Send request
    response = requests.get(url, headers=request_headers)
    response.encoding = 'utf-8'
    html = etree.HTML(response.text)

    # Pick data
    area_stat = html.xpath('//*[@id="getAreaStat"]')
    statistics = html.xpath('//*[@id="getStatisticsService"]')
    _time = time.strftime('20%y-%m-%d', time.localtime())

    # Save data into files
    data_list = []
    with open('./data/statistics (' + _time + ').json', 'w') as f:
        f.write(statistics[0].text[36:-11])
        f.close()
    data_1 = json.loads(statistics[0].text[36:-11])
    data_list.append(data_1['confirmedCount'])
    data_list.append(data_1['suspectedCount'])
    data_list.append(data_1['curedCount'])
    data_list.append(data_1['deadCount'])

    # Draw graph
    f1 = plt.subplot(2, 1, 1)
    f2 = plt.subplot(2, 1, 2)
    plt.sca(f1)
    plt.plot(list(confirmed.keys()), list(confirmed.values()),
            marker='o', label='确诊', color=confirmed_color, linewidth=3)
    plt.plot(list(suspected.keys()), list(suspected.values()),
            marker='v', label='疑似', color=suspected_color, linewidth=3)
    plt.title('2019-nCov 全国疫情新增趋势图 2019-01-11 至 ' + _time)
    plt.legend()
    plt.sca(f2)
    plt.plot(list(cured.keys()), list(cured.values()), marker='s',
            label='治愈', color=cured_color, linewidth=3)
    plt.plot(list(dead.keys()), list(dead.values()), marker='x',
            label='死亡', color=dead_color, linewidth=3)
    title1 = '2019-nCov 全国趋势图 ' + _time
    plt.title('2019-nCov 全国疫情死亡/治愈累计趋势图 2019-01-11 至 ' + _time)
    plt.legend()
    plt.savefig('./view/{0}.png'.format(title1))

    # Save data into files
    with open('./data/area_stat (' + _time + ').json', 'w') as f:
        f.write(area_stat[0].text[27:-11])
        f.close()
    data_2 = json.loads(area_stat[0].text[27:-11])

    # Draw graph
    provinceShortName = []
    confirmedCount = []
    curedCount = []
    deadCount = []
    for i in data_2:
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
    df.plot.barh(stacked=True, color=[confirmed_color, cured_color, dead_color])
    title2 = '2019-nCov 省际统计图 ' + _time
    plt.title(title2)
    plt.savefig('./view/{0}.png'.format(title2))
    #plt.show()

    return title1, title2
