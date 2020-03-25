"""
Class definition for ING data scraper.
"""
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd


class IngDataScraper:
    """Data loader for wertpapiere.ing.de"""
    __index_components_url = 'https://wertpapiere.ing.de/Investieren/Index/EnthalteneWerte/'
    __stock_profile_url = 'https://wertpapiere.ing.de/Investieren/Aktie/Firmenprofil/'
    __contained_shares_class = 'sh-index-contained-shares-list'
    __pnl_class = 'sh-share-income-statement'
    __balance_sheet_class = 'sh-balance-sheet'
    __pnl_fields = ['turnover', 'resultOfOperations', 'incomeAfterTax']

    __MILLION = 10**6

    def __init__(self, max_delay=3):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=chrome_options)
        self.max_delay = max_delay

    def get_components(self, isin):
        self.driver.get(self.__index_components_url + isin)

        try:
            target = EC.presence_of_element_located((By.CLASS_NAME, 'last'))
            WebDriverWait(self.driver, self.max_delay).until(target)
        except TimeoutException:
            return None

        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        table = soup.find_all('div', {'class': self.__contained_shares_class})
        table_soup = BeautifulSoup(str(table), 'html.parser')
        anchors = list(set(table_soup.find_all('a')))

        components = dict((a.attrs['href'][-12:], (a.text, a.attrs['href'])) for a in anchors)

        return components

    def get_financials_for_stock(self, isin):
        def to_float(string):
            return float(string.replace('.', '').replace(',', '.'))

        def floatable(string):
            try:
                to_float(string)
            except ValueError:
                return False
            return True

        self.driver.get(self.__stock_profile_url + isin)

        try:
            target = EC.presence_of_element_located((By.CLASS_NAME, 'row-change'))
            WebDriverWait(self.driver, self.max_delay).until(target)
        except TimeoutException:
            return None

        soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        pnl_table = soup.find_all('div', {'class': self.__pnl_class})
        pnl_soup = BeautifulSoup(str(pnl_table), 'html.parser')

        pnl_fields = self.__pnl_fields
        pnl = pd.DataFrame(columns=['year'] + pnl_fields)

        pnl_dates = [int(tag.text) for tag in pnl_soup.select('thead')[0].select('td[data-position]')]
        pnl['year'] = pnl_dates
        for field in pnl_fields:
            pnl[field] = [to_float(tag.text) * self.__MILLION for tag in pnl_soup.find_all('tr', {'data-row': field})[0]
                          if floatable(tag.text)]

        # ToDo: balance sheet
        balance = None

        return pnl, balance

    def get_financials_for_index(self, isin):
        pass

