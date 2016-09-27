# -*- coding: UTF-8 -*-

import mechanize
import os
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


# 昨天日期
yesterday = datetime.now() - timedelta(days=1)
#ROOT_URL = 'http://cctv.cntv.cn/lm/xinwenlianbo/' + yesterday.strftime('20%y%m%d') + '.shtml'
ROOT_URL = 'http://tv.cctv.com/lm/xwlb/index.shtml'
print "新闻目录URL：", ROOT_URL

# 浏览器伪装
br = mechanize.Browser()
br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.addheaders = [('User-agent',
                  'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

# 新闻联播中各条具体新闻链接
response = br.open(ROOT_URL)
soup = BeautifulSoup(response)
soup = soup.find('div', 'md')
news_urls = []
count = 0

print '正在获取昨日新闻列表...'
# 抓取各条具体新闻链接
for tag_li in soup.find_all('li'):
    # 避开新闻联播全文
    if count == 0:
        count += 1
        continue
    news_urls.append(tag_li.a.get('href'))
    count += 1
print u"昨日共%d条新闻。" % len(news_urls)

print '正在获取新闻联播内容...'
news_count = 1
# 主要内容
content = ''
for url in news_urls[0:-5]:
    print "[%d/%d]获取中..." % (news_count, len(news_urls)),
    response = br.open(url)
    soup = BeautifulSoup(response)
    soup = soup.find('div', 'cnt_bd')
    content += soup.get_text()
    print "ok!"
    news_count += 1
# print content


#file_name = r'~\Documents\DataBase\log.txt'
file_name =yesterday.strftime('20%y%m%d')+".txt"
path_name = os.path.join("C:\Users\dawei\DataBase\\", file_name)
with open(path_name, 'w') as x_file:
    x_file.write(format(content).encode('utf-8'))