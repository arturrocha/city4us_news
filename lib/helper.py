import threading
import time
import telegram
import sys
from .telegram_token import *
from .parser import parse_archirussia, parse_caosplanejado, \
    parse_mobilize, parse_archdaily, parse_citylab, parse_urbanidades


class ProcessSiteThread(threading.Thread):
    def __init__(self, site, telegram_chat_id):
        threading.Thread.__init__(self)
        self.site = site
        self.telegram_chat_id = telegram_chat_id

    def run(self):
        results = process_site(self.site)
        news_list = set(list(results))
        bot = telegram.Bot(token=bot_token)
        print('***** total news for {} = {}'.format(self.site, len(news_list)))
        for news in news_list:
            for user in self.telegram_chat_id:
                time.sleep(1)
                bot.send_message(chat_id=user, text="{}".format(news[1]))


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


def progress(count, total, site=''):
    bar_len = 20
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 2)
    bar = '!' * filled_len + '.' * (bar_len - filled_len)
    sys.stdout.write('  %s%s [%s]  %s/%s | %s...    \r' % (percents, '%', bar, count, total, site[8:30]))
    sys.stdout.flush()

