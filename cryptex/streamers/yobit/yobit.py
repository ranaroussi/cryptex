#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests


class YobitBase:

    public_url = "https://yobit.net/api/2"
    name = "yobit"

    def returnOrderBook(self, pair, limit):

        url = self.public_url + "/" + pair + "/depth"
        options = {"limit": limit}

        r = requests.get(url, data={}, headers={}, params=options)
        return r.json()

    def returnTrades(self, pair, limit):

        url = self.public_url + "/" + pair + "/trades"
        options = {"limit": limit}

        r = requests.get(url, data={}, headers={}, params=options)
        return r.json()
