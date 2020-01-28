import matplotlib.pyplot as plt
import matplotlib
import requests
import json
import time
import pandas as pd
from lxml import etree
from config import request_headers
from config import request_url
from config import pattern
from data import dead
from data import suspected
from data import cured
from data import confirmed
response = requests.get(
    request_url, headers=request_headers).text.encode('ISO-8859-1')
html = etree.HTML(response)
area_stat = html.xpath('//*[@id="getAreaStat"]')
_time = html.xpath('//*[@id="root"]/div/div[3]/div[1]/p[1]/span/text()')
_time = str(_time)
_time = _time[5:-9]
data_list = []
for i in range(1, 5):
    data_list.append(''.join(html.xpath(
        '//*[@id="root"]/div/div[3]/div[1]/p[2]/span/span['+str(i)+']/span/text()')))
label_list = ['Confirmed ('+str(data_list[0])+')', 'Suspected ('+str(
    data_list[1])+')', 'Dead ('+str(data_list[2])+')', 'Cured ('+str(data_list[3])+')']
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
plt.title('Statistics of 2019-nCov as of '+_time+' (Beijing Time)')
plt.legend()
plt.sca(f2)
plt.plot(list(confirmed.keys()), list(confirmed.values()),
         marker='o', label='confirmed', color='red', linewidth=3)
plt.plot(list(suspected.keys()), list(suspected.values()),
         marker='v', label='suspected', color='orange', linewidth=3)
plt.plot(list(cured.keys()), list(cured.values()), marker='s',
         label='cured', color='green', linewidth=3)
plt.plot(list(dead.keys()), list(dead.values()), marker='x',
         label='dead', color='gray', linewidth=3)
plt.title('Statistics of 2019-nCov from 2019-10-11 to ' + _time[:-6])
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
for i in range(len(data)):
    try:
        provinceShortName.append(data[i]['provinceShortName'])
        confirmedCount.append(data[i]['confirmedCount'])
        curedCount.append(data[i]['curedCount'])
        deadCount.append(data[i]['deadCount'])
    except:
        pass
provinceShortName = [pattern[x]
                     if x in pattern else x for x in provinceShortName]
provinceShortName.reverse()
confirmedCount.reverse()
curedCount.reverse()
deadCount.reverse()
df = pd.DataFrame({
    'Confrimed': pd.Series(confirmedCount, index=provinceShortName),
    'Cured': pd.Series(curedCount, index=provinceShortName),
    'Dead': pd.Series(deadCount, index=provinceShortName)
})
df.plot.barh(stacked=True, color=['red', 'green', 'black'])
plt.title('Statistics of 2019-nCov by province as of '+_time+' (Beijing Time)')
plt.show()
