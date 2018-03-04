import requests


class ItbitBase:

    public_url = "https://api.itbit.com/v1/markets"
    name = "itbit"

    def returnOrderBook(self, ticker_symbol):
        url = self.public_url + "/" + ticker_symbol + "/order_book"
        r = requests.get(url, data={}, headers={}, params={})
        return r.json()

    def returnTrades(self, ticker_symbol):
        url = self.public_url + "/" + ticker_symbol + "/trades"
        r = requests.get(url, data={}, headers={}, params={})
        return r.json()
