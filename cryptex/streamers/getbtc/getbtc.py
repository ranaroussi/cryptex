#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests


class GetbtcBase:

    public_url = "https://getbtc.org/api"
    name = "getbtc"

    def returnOrderBook(self, currency, limit):
        url = self.public_url + "/order-book"
        options = {"currency": currency,
                   "limit": limit}

        r = requests.get(url, data={}, headers={}, params=options)
        return r.json()

    def returnTransactions(self, currency, limit):
        url = self.public_url + "/transactions"
        options = {"currency": currency,
                   "limit": limit}

        r = requests.get(url, data={}, headers={}, params=options)
        return r.json()
