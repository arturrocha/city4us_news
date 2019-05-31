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