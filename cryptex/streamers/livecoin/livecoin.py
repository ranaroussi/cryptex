#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests


class LivecoinBase:
    public_url = "https://api.livecoin.net"
    name = "livecoin"

    def returnOrderBook(self, pair, depth):

        url = self.public_url + "/exchange/order_book"
        options = {"currencyPair": pair, "depth": depth}
        r = requests.get(url, data={}, headers={}, params=options)
        return r.json()

    def returnLastTrades(self, pair):
        url = self.public_url + "/exchange/last_trades"
        options = {"currencyPair": pair}
        r = requests.get(url, data={}, headers={}, params=options)
        return r.json()
