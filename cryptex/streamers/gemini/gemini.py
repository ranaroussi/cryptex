#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests


class GeminiBase:

    public_url = "https://api.gemini.com/v1"
    name = 'gemini'

    def returnOrderbook(self, order_currency):
        url = self.public_url + "/book/" + order_currency
        r = requests.get(url, params={})
        return r.json()

    def returnTrades(self, order_currency, depth=1):
        url = self.public_url + "/trades/" + order_currency
        r = requests.get(url, params={"limit_trades": depth})
        return r.json()
