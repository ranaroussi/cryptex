#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests


class BittrexBase:

    public_url = "https://bittrex.com/api/v1.1/public"
    name = 'bittrex'

    def returnOrderbook(self, order_currency):
        url = self.public_url + "/getorderbook"
        r = requests.get(url, params={
            "market": order_currency,
            "type": "both"
        })
        return r.json()

    def returnTrades(self, order_currency):
        url = self.public_url + "/getmarkethistory"
        r = requests.get(url, params={
            "market": order_currency
        })
        return r.json()
