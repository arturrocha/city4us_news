#!/usr/bin/python3
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import urllib.request
import time
import telegram
import re
# import subprocess
from lib.telegram_token import *
from lib.helper import progress, today_article, shell_cmd
from lib.parser import parse_archirussia, parse_caosplanejado, \
    parse_mobilize, parse_archdaily, parse_citylab, parse_urbanidades


class AppURLopener(urllib.request.FancyURLopener):
    version = 'Mozilla/5.0'


count = 0
news_counter = 0

bot = telegram.Bot(token=bot_token)
bot_admin = telegram.Bot(token=bot_admin)


def debug(message, user):
    time.sleep(1)
    bot_admin.send_message(chat_id=user, text="{}".format(message))


def process_site(site):
    arch_trasportation = \
        "https://www.archdaily.com/search/projects/categories/transportation?ad_name=flyout&ad_medium=categories"
    arch_urbandesign = \
        "https://www.archdaily.com/search/projects/categories/urban-design?ad_name=flyout&ad_medium=categories"
    arch_urbanplanning = \
        "https://www.archdaily.com/search/projects/categories/urban-planning?ad_name=flyout&ad_medium=categories"

    if site == 'https://www.mobilize.org.br/noticias/':
        result = parse_mobilize(site)
    elif site == 'https://archi.ru/en':
        result = parse_archirussia(site)
    elif site == 'https://caosplanejado.com/':
        result = parse_caosplanejado(site)
    elif site == arch_trasportation or site == arch_urbandesign or site == arch_urbanplanning:
        result = parse_archdaily(site)
    elif site == 'https://urbanidades.arq.br/':
        result = parse_urbanidades(site)
    elif site == 'https://www.citylab.com/posts/':
        result = parse_citylab(site)
    else:
        return
    return result


def main():
    global count
    global telegram_chat_id_admin
    global news_counter
    url_list = ["https://archi.ru/en",
        "https://www.citylab.com/posts/",
        "https://www.mobilize.org.br/noticias/",
        "https://urbanidades.arq.br/",
        "https://caosplanejado.com/",
        "https://www.archdaily.com/search/projects/categories/transportation?ad_name=flyout&ad_medium=categories",
        "https://www.archdaily.com/search/projects/categories/urban-design?ad_name=flyout&ad_medium=categories",
        "https://www.archdaily.com/search/projects/categories/urban-planning?ad_name=flyout&ad_medium=categories"]

    # fix after parse complete
    try:
        opener = AppURLopener()
    except Exception as e:
        print(e, 'main opener error')

    news_list = []
    total = len(url_list)
    loop_count = 0
    for site in url_list:
        try:
            results = process_site(site)
            for news in results:
                news_list.append(news)
        except TypeError:
            pass
        except Exception as e:
            print(e, 'process_site error')

        loop_count += 1
        progress(loop_count, total, site)

    news_list = set(list(news_list))
    for news in news_list:
        count += 1
        for user in telegram_chat_id:
            time.sleep(0.1)
            bot.send_message(chat_id=user, text="{}".format(news[1]))


run = True
if run:
    t1 = time.time()
    main()
    for user in telegram_chat_id:
        bot.send_message(chat_id=user, text="runtime={}, news={}, total_news={}"
                         .format(round((time.time() - t1), 2), count, news_counter))
        print("runtime={}m, news={}, total_news={}".format(round((time.time() - t1)/60, 2), count, news_counter))
    exit()
