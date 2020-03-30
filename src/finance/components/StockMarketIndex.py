"""
Class definition for stock market index.
"""
from src.data.YahooDataLoader import YahooDataLoader
from src.data.IngDataScraper import IngDataScraper


class StockMarketIndex:
    """Stock market index implementation"""

    def __init__(self, isin, yahoo_ticker):
        self.isin = isin
        self.yahoo_ticker = yahoo_ticker
        self.components = {}

        self.ing_scraper = IngDataScraper()
        self.yahoo_loader = YahooDataLoader()

    def data(self, start, end, freq):
        return self.yahoo_loader.fetch(
            ticker=self.yahoo_ticker,
            start=start,
            end=end,
            freq=freq
        )

    def components(self):
        if not self.components:
            components = self.ing_scraper.get_components(self.isin)
            self.components = {isin: details[0] for isin, details in components.items()}

        return self.components

    def book_value(self):
        components = self.components()
        balances = dict()

        for cisin in components.keys():
            _, cbalance = self.ing_scraper.get_financials_for_stock(cisin)
            balances[cisin] = cbalance

        # ToDo: determine weights
