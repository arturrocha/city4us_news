#!/usr/bin/python3
import time
import threading
import logging
import yaml
from lib.telegram_token import *
from lib.helper import ProcessSiteThread


def main():
    logging.basicConfig(format='%(asctime)s %(message)s', filename='city4us.log', level=logging.INFO)
    logging.info('**************** Start')
    t1 = time.time()

    with open("sites.yaml", 'r') as stream:
        url_list = yaml.safe_load(stream)

    for url in url_list['url']:
        thread = ProcessSiteThread(url, telegram_chat_id)
        thread.start()
        time.sleep(1)

    while threading.activeCount() > 1:
        time.sleep(1)

    time_list = str(round((time.time() - t1) / 60, 2)).split('.')
    sec = round((60 * int(time_list[1])) / 100, 1)
    logging.info('End, duration = {}m {}s'.format(time_list[0], sec))


if __name__ == '__main__':
    main()

