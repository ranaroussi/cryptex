#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests


class BitbayBase:

    public_url = "https://bitbay.net/API/Public"
    name = "bitbay"

    def returnOrderbook(self, pair):
        url = self.public_url + "/" + pair + "/orderbook.json"
        r = requests.get(url, data={}, headers={}, params={})
        return r.json()

    def returnTrades(self, pair):
        url = self.public_url + "/" + pair + "/trades.json"
        options = {"sort": "desc"}
        r = requests.get(url, data={}, headers={}, params=options)
        return r.json()
