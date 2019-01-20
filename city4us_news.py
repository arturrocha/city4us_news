#!/usr/bin/python3
from datetime import date, datetime, timedelta
from bs4 import BeautifulSoup
import urllib.request
import requests
import time
import telegram
from _telegram import *


class AppURLopener(urllib.request.FancyURLopener):
    version = 'Mozilla/5.0'

count = 0
bot = telegram.Bot(token=bot_token)


# var in file _telegram
# bot_token = 'some id'
# telegram_chat_id = ['bla', 'bla']

# to do
# transportation, urban design and urban planning


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
    url = ["https://www.citylab.com/posts/",
        "https://www.mobilize.org.br/noticias/",
        "https://urbanidades.arq.br/",
        "https://caosplanejado.com/",
        "https://www.archdaily.com/"]
    opener = AppURLopener()
    news_list = []
    for site in url:
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
                            print(sub_url)
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
                                print(e)
                        if 'www' in sub_url and 'blogs' in sub_url and '?p=' in sub_url:
                            print(sub_url)
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
                                print(e)
            elif site is 'https://caosplanejado.com/':
                result_search = str(soup.find_all('h1'))
                a = result_search.split(' ')
                for thing in a:
                    if 'http' in thing:
                        sub_url = thing.split('"')[1]
                        print(sub_url)
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
                            print(e)
            elif site is 'https://www.archdaily.com/':
                result_search = str(soup.find_all('h3')).split(' ')
                for sub_url in result_search:
                    if 'href="' in sub_url:
                        sub_url = site+sub_url.replace('href="', '').replace('"', '').split('>')[0]
                        print(sub_url)
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
                            print(e)
            elif site is "https://www.citylab.com/posts/":
                result_search = str(soup.find_all('section')).split(" ")
                empty_list = []
                for sub_url in result_search:
                    if 'href="' in sub_url and 'authors' not in sub_url and '/newsletters/' not in sub_url:
                        if sub_url not in empty_list:
                            empty_list.append(sub_url.split('"')[1])
                for sub_url in list(set(empty_list)):
                    print(sub_url)
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
                        print(e)

            else:
                pass
        except Exception as e:
            print(e)
    for news in news_list:
        count += 1
        for user in telegram_chat_id:
            bot.send_message(chat_id=user, text="{}".format(news[1]))


run = True
if run:
    t1 = time.time()
    _main()
    for user in telegram_chat_id:
        bot.send_message(chat_id=user, text="runtime={}, news={}".format(round((time.time() - t1), 2), count))
    exit()

