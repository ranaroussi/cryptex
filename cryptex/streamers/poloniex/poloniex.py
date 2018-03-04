#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests


class PoloniexBase:

    public_url = "https://poloniex.com/public"
    name = "poloniex"

    def returnOrderBook(self, pair, depth):
        options = {
            "command": "returnOrderBook",
            "currencyPair": pair,
            "depth": depth
        }
        r = requests.get(self.public_url, data={}, headers={}, params=options)
        return r.json()

    def returnTrades(self, pair):
        options = {
            "command": "returnTradeHistory",
            "currencyPair": pair
        }
        r = requests.get(self.public_url, data={}, headers={}, params=options)
        return r.json()
