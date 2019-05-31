#!/usr/bin/python3
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import urllib.request
import time
import telegram
import re
import subprocess
from _telegram import *
from lib.helper import progress, today_article


class AppURLopener(urllib.request.FancyURLopener):
    version = 'Mozilla/5.0'


count = 0
news_counter = 0

bot = telegram.Bot(token=bot_token)
bot_admin = telegram.Bot(token=bot_admin)


def debug(message, user):
    time.sleep(1)
    bot_admin.send_message(chat_id=user, text="{}".format(message))


def shell_cmd(cmd):
    result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = result.communicate()
    return output
   

def _main():
    global count
    global telegram_chat_id_admin
    global news_counter
    url = ["https://archi.ru/en",
        "https://www.citylab.com/posts/",
        "https://www.mobilize.org.br/noticias/",
        "https://urbanidades.arq.br/",
        "https://caosplanejado.com/",
        "https://www.archdaily.com/search/projects/categories/transportation?ad_name=flyout&ad_medium=categories",
        "https://www.archdaily.com/search/projects/categories/urban-design?ad_name=flyout&ad_medium=categories",
        "https://www.archdaily.com/search/projects/categories/urban-planning?ad_name=flyout&ad_medium=categories"]

    arch_trasportation = \
        "https://www.archdaily.com/search/projects/categories/transportation?ad_name=flyout&ad_medium=categories"
    arch_urbandesign = \
        "https://www.archdaily.com/search/projects/categories/urban-design?ad_name=flyout&ad_medium=categories"
    arch_urbanplanning = \
        "https://www.archdaily.com/search/projects/categories/urban-planning?ad_name=flyout&ad_medium=categories"
    try:
        opener = AppURLopener()
    except Exception as e:
        debug(e, telegram_chat_id_admin)
    news_list = []
    total = len(url)
    loop_count = 0
    for site in url:
        loop_count += 1
        progress(loop_count, total, site)
        try:
            response = opener.open(site)
            soup = BeautifulSoup(response, "html.parser")
            if site is "https://www.mobilize.org.br/noticias/":
                result_search = str(soup.find_all('p'))
                b = result_search.split('</p>,')
                for thing in b:
                    thing = thing.split('"')
                    for sub_url in thing:
                        if 'www' in sub_url and 'noticias' in sub_url:
                            try:
                                response = opener.open(sub_url)
                                soup = BeautifulSoup(response, "html.parser")
                                result_search = str(soup.find_all('p'))
                                c = result_search.split('<span id="ctl00_ContentPlaceHolder1_lblData">')
                                _date = c[1].split('</span>')[0]
                                news_counter += 1
                                description = str(soup.find_all('title'))
                                description = description.replace('<title>', '').replace('</title>', '')
                                if today_article(_date):
                                    var = description, sub_url
                                    news_list.append(var)
                            except Exception as e:
                                debug(e, telegram_chat_id_admin)                                
                        if 'www' in sub_url and 'blogs' in sub_url and '?p=' in sub_url:
                            try:
                                response = opener.open(sub_url)
                                soup = BeautifulSoup(response, "html.parser")
                                result_search = str(soup.find_all('p'))
                                d = result_search.split('</a> no dia ')
                                _date = d[1].split('</div>')[0]
                                news_counter += 1
                                description = str(soup.find_all('title'))
                                description = description.replace('<title>', '').replace('</title>', '')
                                if today_article(_date):
                                    var = description, sub_url
                                    news_list.append(var)
                            except Exception as e:
                                debug(e, telegram_chat_id_admin)
            elif site is "https://archi.ru/en":
                result_search = str(soup.find_all('header'))
                a = result_search.split(' ')
                for url in a:
                    if 'http' in url:
                        sub_url = url.split('"')[1]
                        blob = sub_url.split('/')
                        for thing in blob:
                            try:
                                int(thing)
                                is_news = True
                            except Exception as e:
                                is_news = False
                            if is_news:
                                try:
                                    response = opener.open(sub_url)
                                    soup = BeautifulSoup(response, "html.parser")
                                    _date = str(soup.find_all('div', {'class': 'date'})).split(',')[0].replace('</div>', '').replace('[<div class="date">', '')
                                    news_counter += 1
                                    if today_article(_date, 5):
                                        news_list.append(sub_url)
                                except Exception as e:
                                    print(e)                        
            elif site is 'https://caosplanejado.com/':
                result_search = str(soup.find_all('h1'))
                a = result_search.split(' ')
                for thing in a:
                    if 'http' in thing:
                        sub_url = thing.split('"')[1]
                        try:
                            response = opener.open(sub_url)
                            soup = BeautifulSoup(response, "html.parser")
                            result_search = str(soup.find_all('time'))
                            _date = result_search.split('"')[3].split('T')[0]
                            news_counter += 1
                            description = str(soup.find_all('h1'))
                            description = description.split('">')[1].replace('</h1>]', '')
                            if today_article(_date, 2):
                                var = description, sub_url
                                news_list.append(var)
                        except Exception as e:
                            debug(e, telegram_chat_id_admin)
            elif site is 'https://www.archdaily.com/':
                result_search = str(soup.find_all('h3')).split(' ')
                for sub_url in result_search:
                    if 'href="' in sub_url:
                        sub_url = site+sub_url.replace('href="', '').replace('"', '').split('>')[0]
                        try:
                            response = opener.open(sub_url)
                            soup = BeautifulSoup(response, "html.parser")
                            result_search = str(soup.find_all('header'))
                            result_search = result_search.split('ul')
                            description = str(soup.find_all('h1'))
                            description = description.split('afd-relativeposition">')[1].split('</h1>]')[0]
                            for thing in result_search:
                                if 'theDate' in thing:
                                    _date = thing.split('</li>')[0].split('<li class="theDate">')[1].split('-')[1]
                                    news_counter += 1
                                    if today_article(_date, 3):
                                        var = description, sub_url
                                        news_list.append(var)
                        except Exception as e:
                            debug(e, telegram_chat_id_admin)
            elif site is "https://www.citylab.com/posts/":
                result_search = str(soup.find_all('section')).split(" ")
                empty_list = []
                for sub_url in result_search:
                    if 'href="' in sub_url and 'authors' not in sub_url and '/newsletters/' not in sub_url:
                        if sub_url not in empty_list:
                            empty_list.append(sub_url.split('"')[1])
                for sub_url in list(set(empty_list)):
                    try:
                        response = opener.open(sub_url)
                        soup = BeautifulSoup(response, "html.parser")
                        result_search = str(soup.find_all('article'))
                        _date = result_search.split('<meta content="')[1].split('T')[0]
                        news_counter += 1
                        description = str(soup.find_all('h1'))
                        description = description.split('headline">')[1].replace('</h1>]', '')
                        if today_article(_date, 2):
                            var = description, sub_url
                            news_list.append(var)
                    except Exception as e:
                        debug(e, telegram_chat_id_admin)
            elif site is arch_trasportation or site is arch_urbandesign or site is arch_urbanplanning:
                result_search = str(soup.find_all(re.compile('^a'))).split(" ")
                empty_list = []
                for sub_url in result_search:
                    try:
                        if 'href' in sub_url:
                            try:    
                                if len(str(sub_url.split('/')[1])) == 6:
                                    sub_url = 'https://www.archdaily.com' + sub_url.replace('href="', '')
                                    try:
                                        response = opener.open(sub_url)
                                        soup = BeautifulSoup(response, "html.parser")
                                        result_search2 = str(soup.find_all('header'))
                                        result_search2 = result_search2.split('ul')
                                        description = str(soup.find_all('h1'))
                                        description = description.split('afd-relativeposition">')[1].split('</h1>]')[0]
                                        try:
                                            for thing in result_search2:
                                                if 'theDate' in thing:
                                                    _date = thing.split('</li>')[0].split('<li class="theDate">')[1].split('-')[1]
                                                    news_counter += 1
                                                    if today_article(_date, 4):
                                                        var = description, sub_url
                                                        news_list.append(var)
                                        except Exception as e:
                                            time.sleep(0.4)
                                            e = str(e) + ' # sub url | archdaily categories/all'
                                            debug(e, telegram_chat_id_admin)
                                    except Exception as e:
                                        time.sleep(0.4)
                                        e = str(e) + ' # result_search2 url | archdaily categories/all'
                                        debug(e, telegram_chat_id_admin)
                            except Exception as e:
                                e = str(e) + ' # archdaily split /'
                                debug(e, telegram_chat_id_admin)
                    except Exception as e:
                        time.sleep(0.4)
                        e = str(e) + ' # sub url | archdaily***'
                        debug(e, telegram_chat_id_admin)
        except Exception as e:
            e = str(e) + ' #####'
            debug(e, telegram_chat_id_admin)
            print(e)
        if site is "https://urbanidades.arq.br/":
            try:
                cmd = 'curl {0}'.format(site)
                result = str(shell_cmd(cmd)).split('<article id="')
                yesterday = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
                yesterday = yesterday.split('-')
                str_yesterday = '-'.join(yesterday)
                urbanidades_news_list = []
                for blob in result:
                    blob = blob.split(' ')
                    for article_blob in blob:
                        if 'href="https://urbanidades.arq.br/' in article_blob:
                            article = article_blob.split('"')[1].split('/')
                            try:
                                del(article[6])
                            except Exception as e:
                                pass
                            if str(article[3]) == str(yesterday[0]) and str(article[4]) == str(yesterday[1]):
                                urbanidades_news_list.append('/'.join(article))
                for news in list(set(urbanidades_news_list)):
                    news_counter += 1
                    urbanidades_yesterday_news = []
                    try:
                        cmd = 'wget {0} -O news.txt'.format(news)
                        shell_cmd(cmd)
                        with open('news.txt', 'r') as news_txt:
                            data = str(news_txt.read()).split('time')
                            for blob in data:
                                blob2 = blob.split('"')
                                for thing in blob2:
                                    if str_yesterday in thing:
                                        urbanidades_yesterday_news.append(news)
                        cmd = 'rm news.txt'
                        shell_cmd(cmd)
                    except Exception as e:
                        print(e)
            except Exception as e:
                print(e)
    try:
        for news in urbanidades_yesterday_news:
            news_list.append(news)
    except Exception as e:
        print(e)
    news_list = set(list(news_list))
    for news in news_list:
        count += 1
        for user in telegram_chat_id:
            time.sleep(0.1)
            bot.send_message(chat_id=user, text="{}".format(news[1]))


run = True
if run:
    t1 = time.time()
    _main()
    for user in telegram_chat_id:
        bot.send_message(chat_id=user, text="runtime={}, news={}, total_news={}"
                         .format(round((time.time() - t1), 2), count, news_counter))
        print("runtime={}m, news={}, total_news={}".format(round((time.time() - t1)/60, 2), count, news_counter))
    exit()

