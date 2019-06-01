#!/usr/bin/python3
import time
import threading
from lib.telegram_token import *
from lib.helper import ProcessSiteThread


def main():
    url_list = ["https://www.mobilize.org.br/noticias/",
                "https://archi.ru/en",
                "https://www.citylab.com/posts/",
                "https://urbanidades.arq.br/",
                "https://caosplanejado.com/",
                "https://www.archdaily.com/search/projects/categories/transportation?ad_name=flyout&ad_medium=categories",
                "https://www.archdaily.com/search/projects/categories/urban-design?ad_name=flyout&ad_medium=categories",
                "https://www.archdaily.com/search/projects/categories/urban-planning?ad_name=flyout&ad_medium=categories"]

    # total = len(url_list)
    loop_count = 0
    for site in url_list:
        try:
            thread = ProcessSiteThread(site, telegram_chat_id)
            thread.start()
            time.sleep(1)
        except TypeError:
            pass
        except Exception as e:
            print(e, 'process_site error')

        loop_count += 1
        # progress(loop_count, total, site)


run = True
if run:
    t1 = time.time()
    main()
    while threading.activeCount() > 1:
        time.sleep(1)
    td = time.time() - t1
    print('duration = ', round(td/60, 2))
    exit()
