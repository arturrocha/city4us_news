#!/usr/bin/python3
from datetime import date, datetime, timedelta
from bs4 import BeautifulSoup
import urllib.request
import requests
import time
import telegram
import re
import sys
from _telegram import *


class AppURLopener(urllib.request.FancyURLopener):
    version = 'Mozilla/5.0'


count = 0
bot = telegram.Bot(token=bot_token)
bot_admin = telegram.Bot(token=bot_admin)


def progress(count, total, site=''):
    bar_len = 20
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 2)
    bar = '!' * filled_len + '.' * (bar_len - filled_len)
    sys.stdout.write('  %s%s [%s]  %s/%s | %s...    \r' % (percents, '%', bar, count, total, site[8:30]))
    sys.stdout.flush()


def debug(message, user):
    time.sleep(1)
    bot_admin.send_message(chat_id=user, text="{}".format(message))


def today_article(_date, mode=1):
    yesterday = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
    yesterday = yesterday.split('-')
    if mode == 1:
        _article = _date.split(' de ')
        article = _date.split(' de ')

        # year
        article[0] = _article[2]

        # month
        month = _article[1].lower().replace(' ', '')
        if month == 'janeiro' or month == 'january':
            article[1] = '01'
        elif month == 'fevereiro' or month == 'february':
            article[1] = '02'
        elif 'mar' in month:
            article[1] = '03'
        elif month == 'abril' or month == 'april':
            article[1] = '04'
        elif month == 'maio' or month == 'may':
            article[1] = '05'
        elif month == 'junho' or month == 'june':
            article[1] = '06'
        elif month == 'julho' or month == 'july':
            article[1] = '07'
        elif month == 'agosto' or month == 'august':
            article[1] = '08'
        elif month == 'setembro' or month == 'september':
            article[1] = '09'
        elif month == 'outubro' or month == 'october':
            article[1] = '10'
        elif month == 'novembro' or month == 'november':
            article[1] = '11'
        elif month == 'dezembro' or month == 'december':
            article[1] = '12'
        else:
            print('month out of scope')
            print(article)
            exit()

        # day
        article[2] = _article[0]

    elif mode == 2:
        article = _date.split('-')

    elif mode == 3:
        _article = _date.replace(',', '')
        _article = _article.split(' ')
        day = _article[1]
        article = _article

        # year
        article[0] = _article[3]
        # month
        month = _article[2].lower().replace(' ', '')
        if month == 'janeiro' or month == 'january':
            article[1] = '01'
        elif month == 'fevereiro' or month == 'february':
            article[1] = '02'
        elif 'mar' in month:
            article[1] = '03'
        elif month == 'abril' or month == 'april':
            article[1] = '04'
        elif month == 'maio' or month == 'may':
            article[1] = '05'
        elif month == 'junho' or month == 'june':
            article[1] = '06'
        elif month == 'julho' or month == 'july':
            article[1] = '07'
        elif month == 'agosto' or month == 'august':
            article[1] = '08'
        elif month == 'setembro' or month == 'september':
            article[1] = '09'
        elif month == 'outubro' or month == 'october':
            article[1] = '10'
        elif month == 'novembro' or month == 'november':
            article[1] = '11'
        elif month == 'dezembro' or month == 'december':
            article[1] = '12'
        else:
            print('month out of scope')
            print(article)
            exit()
        # day
        article[2] = day

        del article[3]

    elif mode == 4:
        _article = _date.replace(',', '')
        _article = _article.split(' ')
        article = _article
        
        if len(_article) == 4:
            # day
            day = str(_article[1])
            if len(day) == 1:
                day = '0' + day
            # year
            article[0] = _article[3]
            # month
            month = _article[2].lower().replace(' ', '')
        elif len(_article) == 3:
            # day
            day = _article[0]
            # year
            article[0] = _article[2]
            # month
            month = _article[1].lower().replace(' ', '')
        else:
            # fix
            print('something broke on the date')
            print(_article)
            print('exiting')
            exit()
            
        article = _article
                
        # month
        if month == 'janeiro' or month == 'january':
            article[1] = '01'
        elif month == 'fevereiro' or month == 'february':
            article[1] = '02'
        elif 'mar' in month:
            article[1] = '03'
        elif month == 'abril' or month == 'april':
            article[1] = '04'
        elif month == 'maio' or month == 'may':
            article[1] = '05'
        elif month == 'junho' or month == 'june':
            article[1] = '06'
        elif month == 'julho' or month == 'july':
            article[1] = '07'
        elif month == 'agosto' or month == 'august':
            article[1] = '08'
        elif month == 'setembro' or month == 'september':
            article[1] = '09'
        elif month == 'outubro' or month == 'october':
            article[1] = '10'
        elif month == 'novembro' or month == 'november':
            article[1] = '11'
        elif month == 'dezembro' or month == 'december':
            article[1] = '12'
        else:
            print('month out of scope')
            print(article)
            return False
        # day
        article[2] = day
        
        try:
            del article[3]
        except exception as e:
            print(e)
            print('article[#3] nothing here to delete')

    elif mode == 5:
        article = []
        article.append(_date.split('.')[2])
        article.append(_date.split('.')[1])
        article.append(_date.split('.')[0])

    debug = False

    if not debug:
        if yesterday == article:
            return True
        else:
            return False
    else:
        print(yesterday, article)
        return True


def _main():
    global count
    global telegram_chat_id_admin
    url = ["https://archi.ru/en",
        "https://www.citylab.com/posts/",
        "https://www.mobilize.org.br/noticias/",
        "https://urbanidades.arq.br/",
        "https://caosplanejado.com/",
        "https://www.archdaily.com/search/projects/categories/transportation?ad_name=flyout&ad_medium=categories",
        "https://www.archdaily.com/search/projects/categories/urban-design?ad_name=flyout&ad_medium=categories",
        "https://www.archdaily.com/search/projects/categories/urban-planning?ad_name=flyout&ad_medium=categories"]

    arch_trasportation = "https://www.archdaily.com/search/projects/categories/transportation?ad_name=flyout&ad_medium=categories"
    arch_urbandesign = "https://www.archdaily.com/search/projects/categories/urban-design?ad_name=flyout&ad_medium=categories"
    arch_urbanplanning = "https://www.archdaily.com/search/projects/categories/urban-planning?ad_name=flyout&ad_medium=categories"
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
                                    _date = str(soup.find_all('div', {'class':'date'})).split(',')[0].replace('</div>', '').replace('[<div class="date">', '')
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

    news_list = set(list(news_list))
    for news in news_list:
        count += 1
        for user in telegram_chat_id:
            time.sleep(0.4)
            bot.send_message(chat_id=user, text="{}".format(news[1]))


run = True
if run:
    t1 = time.time()
    _main()
    for user in telegram_chat_id:
        bot.send_message(chat_id=user, text="runtime={}, news={}".format(round((time.time() - t1), 2), count))
        print("runtime={}m, news={}".format(round((time.time() - t1)/60, 2), count))
    exit()

