"""
Class definition for ING data scraper.
"""
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import pandas as pd


class IngDataScraper:
    """Data loader for wertpapiere.ing.de"""
    index_components_url = 'https://wertpapiere.ing.de/Investieren/Index/EnthalteneWerte/'
    table_div_class = 'sh-index-contained-shares-list'
    max_delay = 3

    def get_components(self, isin):
        chrome_options = Options()
        chrome_options.add_argument('--headless')

        driver = webdriver.Chrome(options=chrome_options)
        driver.get(self.index_components_url + isin)

        try:
            target = EC.presence_of_element_located((By.CLASS_NAME, 'last'))
            WebDriverWait(driver, self.max_delay).until(target)
        except TimeoutException:
            return None

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        table = soup.find_all('div', {'class': self.table_div_class})
        table_soup = BeautifulSoup(str(table), 'html.parser')
        anchors = list(set(table_soup.find_all('a')))

        components = dict((a.attrs['href'][-12:], (a.text, a.attrs['href'])) for a in anchors)

        return components
