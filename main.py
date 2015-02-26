#!/usr/bin/env python
#-*- coding: utf-8-*-
import time

import requests

from lxml.html import fromstring
from pync import Notifier
import re

ENDPOINT = 'http://atlant-m.kiev.ua/ru/models/new_golf/facts-figures/prices/11-highline/'
TIMEOUT = 5
XPATH = '/html/body/div[1]/div[2]/div[3]/div/div[2]/table/tbody/tr[6]/td[7]'
TITLE = 'Golf GTI VII'


def main():
    last_currency = None

    while True:
        try:
            html = requests.get(ENDPOINT).text
            tree = fromstring(html)
            el = tree.xpath(XPATH)[0]
            value =int(''.join(re.findall(r'\d', el.text)))
        except Exception as e:
	    print(e)
            time.sleep(TIMEOUT)
            continue

        if last_currency != value:
            last_currency = value

            try:
                Notifier.notify(
                    TITLE,
                    open=ENDPOINT,
                    title=unicode(value) + u' uah'
                )
            except Exception as e:
		print(e)
                pass

        time.sleep(TIMEOUT)


if __name__ == '__main__':
    main()
