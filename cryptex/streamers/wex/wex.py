#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests


class WexBase:

    public_url = "https://wex.nz/api/3"
    name = "wex"

    def returnOrderBook(self, pair, limit):
        url = self.public_url + "/depth/" + pair
        options = {"limit": limit}
        r = requests.get(url, data={}, headers={}, params=options)
        return r.json()

    def returnExecutions(self, pair, limit):
        url = self.public_url + "/trades/" + pair
        options = {"limit": limit}
        r = requests.get(url, data={}, headers={}, params=options)
        return r.json()
