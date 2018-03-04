#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests


class BithumbBase():

    public_url = "https://api.bithumb.com/public"
    name = 'bithumb'

    def returnOrderBook(self, order_currency):
        url = self.public_url + "/orderbook/" + order_currency
        r = requests.get(url, data={}, headers={}, params={})
        return r.json()

    def returnRecentTransactions(self, order_currency):
        url = self.public_url + "/recent_transactions/" + order_currency
        r = requests.get(url, data={}, headers={}, params={})
        return r.json()
