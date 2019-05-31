from datetime import date, datetime, timedelta
from bs4 import BeautifulSoup
import urllib.request
import requests
import time
import telegram
import re
import sys
import subprocess
from _telegram import *


def progress(count, total, site=''):
    bar_len = 20
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 2)
    bar = '!' * filled_len + '.' * (bar_len - filled_len)
    sys.stdout.write('  %s%s [%s]  %s/%s | %s...    \r' % (percents, '%', bar, count, total, site[8:30]))
    sys.stdout.flush()


def shell_cmd(cmd):
    result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = result.communicate()
    return output


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
