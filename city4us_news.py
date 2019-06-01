#!/usr/bin/python3
import time
import threading
from lib.telegram_token import *
from lib.helper import ProcessSiteThread
import logging


def main():
    logging.basicConfig(format='%(asctime)s %(message)s', filename='city4us.log', level=logging.DEBUG)
    t1 = time.time()
    url_list = ["https://www.mobilize.org.br/noticias/",
                "https://archi.ru/en",
                "https://www.citylab.com/posts/",
                "https://urbanidades.arq.br/",
                "https://caosplanejado.com/",
                "https://www.archdaily.com/search/projects/categories/transportation?ad_name=flyout&ad_medium=categories",
                "https://www.archdaily.com/search/projects/categories/urban-design?ad_name=flyout&ad_medium=categories",
                "https://www.archdaily.com/search/projects/categories/urban-planning?ad_name=flyout&ad_medium=categories"]

    for site in url_list:
        try:
            thread = ProcessSiteThread(site, telegram_chat_id)
            thread.start()
            time.sleep(1)
        except TypeError:
            pass
        except Exception as e:
            print(e, 'process_site error')

    while threading.activeCount() > 1:
        time.sleep(1)
    td = time.time() - t1
    logging.info('duration = {}'.format(round(td / 60, 2)))


if __name__ == '__main__':
    main()

