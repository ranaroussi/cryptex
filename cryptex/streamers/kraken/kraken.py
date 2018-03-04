#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests


class KrakenBase:

    public_url = "https://api.kraken.com/0/public"
    name = "kraken"

    def returnOrderBook(self, pair, count):
        url = self.public_url + "/Depth"
        options = {"pair": pair, "count": count}
        r = requests.get(url, data={}, headers={}, params=options)
        return r.json()

    def returnTrades(self, pair):
        url = self.public_url + "/Trades"
        options = {"pair": pair}
        r = requests.get(url, data={}, headers={}, params=options)
        return r.json()
