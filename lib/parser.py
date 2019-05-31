import urllib.request
import re
import time
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from .helper import today_article, shell_cmd


class AppURLopener(urllib.request.FancyURLopener):
    version = 'Mozilla/5.0'


def parse_archirussia(site):
    try:
        news_list = []
        opener = AppURLopener()
        response = opener.open(site)
        soup = BeautifulSoup(response, "html.parser")
    except Exception as e:
        print(e, 'archi.ru opener error')
        return
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
                    print(e, 'arch.ru > thing in blob')
                if is_news:
                    try:
                        response = opener.open(sub_url)
                        soup = BeautifulSoup(response, "html.parser")
                        _date = str(soup.find_all('div', {'class': 'date'})).split(',')[0]
                        _date = _date.replace('</div>', '').replace('[<div class="date">', '')
                        if today_article(_date, 5):
                            news_list.append(sub_url)
                    except Exception as e:
                        print(e)
    return news_list


def parse_caosplanejado(site):
    try:
        news_list = []
        opener = AppURLopener()
        response = opener.open(site)
        soup = BeautifulSoup(response, "html.parser")
    except Exception as e:
        print(e, 'caosplanejado opener error')
        return
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
                print(e, 'caos planejado error')
    return news_list


def parse_mobilize(site):
    try:
        news_list = []
        opener = AppURLopener()
        response = opener.open(site)
        soup = BeautifulSoup(response, "html.parser")
    except Exception as e:
        print(e, 'mobilize opener error')
        return
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
                    print(e, 'error for mobilize www and noticias in if')

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
                    print(e, 'error for mobilize www and blogs and ?p in if')
    return news_list


def parse_archdaily(site):
    try:
        news_list = []
        opener = AppURLopener()
        response = opener.open(site)
        soup = BeautifulSoup(response, "html.parser")
    except Exception as e:
        print(e, 'mobilize opener error')
        return
    result_search = str(soup.find_all(re.compile('^a'))).split(" ")
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
                                print(e)
                        except Exception as e:
                            time.sleep(0.4)
                            e = str(e) + ' # result_search2 url | archdaily categories/all'
                            print(e)
                except Exception as e:
                    e = str(e) + ' # archdaily split /'
                    print(e)
        except Exception as e:
            time.sleep(0.4)
            e = str(e) + ' # sub url | archdaily***'
            print(e)
    return news_list


def parse_citylab(site):
    try:
        news_list = []
        opener = AppURLopener()
        response = opener.open(site)
        soup = BeautifulSoup(response, "html.parser")
    except Exception as e:
        print(e, 'citylab opener error')
        return
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
            print(e, 'citylab error sub_url')
    return news_list


def parse_urbanidades(site):
    try:
        news_list = []
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
                        del (article[6])
                    except Exception as e:
                        e = str(e) + ' # urbanidades article_blob'
                        print(e)
                    if str(article[3]) == str(yesterday[0]) and str(article[4]) == str(yesterday[1]):
                        urbanidades_news_list.append('/'.join(article))
        for news in list(set(urbanidades_news_list)):
            try:
                cmd = 'wget {0} -O news.txt'.format(news)
                shell_cmd(cmd)
                with open('news.txt', 'r') as news_txt:
                    data = str(news_txt.read()).split('time')
                    for blob in data:
                        blob2 = blob.split('"')
                        for thing in blob2:
                            if str_yesterday in thing:
                                news_list.append(news)
                cmd = 'rm news.txt'
                shell_cmd(cmd)
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
        return
    return news_list
