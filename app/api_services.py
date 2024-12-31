import requests
from .api_config import *

class MarketDataService:
    @staticmethod
    def get_stock_data(symbol):
        """Get real-time stock data from Marketstack"""
        endpoint = f"{MARKETSTACK_ENDPOINT}/intraday"
        params = {
            'access_key': MARKETSTACK_API_KEY,
            'symbols': symbol,
            'interval': '1min'
        }
        response = requests.get(endpoint, params=params)
        return response.json()

    @staticmethod
    def get_crypto_data(symbol):
        """Get cryptocurrency data from Coinlayer"""
        endpoint = f"{COINLAYER_ENDPOINT}/live"
        params = {
            'access_key': COINLAYER_API_KEY,
            'symbols': symbol
        }
        response = requests.get(endpoint, params=params)
        return response.json()

    @staticmethod
    def get_forex_data(symbol):
        """Get forex data from Alpha Vantage"""
        endpoint = ALPHA_VANTAGE_ENDPOINT
        params = {
            'function': 'CURRENCY_EXCHANGE_RATE',
            'from_currency': symbol.split('/')[0],
            'to_currency': symbol.split('/')[1],
            'apikey': ALPHA_VANTAGE_API_KEY
        }
        response = requests.get(endpoint, params=params)
        return response.json() 