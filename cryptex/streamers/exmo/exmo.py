import requests


class ExmoBase:
    public_url = "https://api.exmo.com/v1"
    name = "exmo"

    def returnTrades(self, pair, limit):
        url = self.public_url + "/trades"
        options = {"pair": pair, "limit": limit}
        r = requests.get(url, data={}, headers={}, params=options)
        return r.json()

    def returnOrderbook(self, pair, limit):
        url = self.public_url + "/order_book"
        options = {"pair": pair, "limit": limit}
        r = requests.get(url, data={}, headers={}, params=options)
        return r.json()
