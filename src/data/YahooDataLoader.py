"""
Class definition for Yahoo data loader.
"""
from bs4 import BeautifulSoup
import datetime as dt
import pandas as pd
import re
import requests


class YahooDataLoader:
    """Data loader for finance.yahoo.com"""
    __base_url = 'https://finance.yahoo.com/'
    __url_data = 'https://finance.yahoo.com/quote/{ticker}/history'
    __url_data_download = 'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?' \
        'period1={start}&period2={end}&interval={freq}&events=history&crumb={crumb}'

    __ticker_class = 'D(ib) Fz(18px)'

    __SEPARATOR = ','

    def __get_cookies_and_crumbs(self, ticker):
        url = self.__url_data.format(ticker=ticker)

        with requests.session():
            header = {
                'Connection': 'keep-alive',
                'Expires': '-1',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
                    'AppleWebKit/537.36 (KHTML, like Gecko) ' \
                    'Chrome/80.0.3987.132 Safari/537.36'
            }
            website = requests.get(url, headers=header)
            soup = BeautifulSoup(website.text, 'html.parser')
            crumb = re.findall('"CrumbStore":{"crumb":"(.+?)"}', str(soup))
            self.cookies = website.cookies  # ToDo: delete
            return header, website.cookies, crumb[0]

    def fetch(self, ticker, start, end, freq):
        def _date_to_seconds(date):
            return int((date-dt.datetime(1970, 1, 1)).total_seconds())

        header, cookies, crumb = self.__get_cookies_and_crumbs(ticker)

        with requests.session():
            url = self.__url_data_download.format(
                ticker=ticker,
                start=str(_date_to_seconds(start)),
                end=str(_date_to_seconds(end)),
                freq=freq,
                crumb=crumb
            )
            website = requests.get(url, headers=header, cookies=cookies)

            data = website.text.split('\n')

        names = data.pop(0).split(self.__SEPARATOR)

        return pd.DataFrame([row.split(self.__SEPARATOR) for row in data], columns=names)
