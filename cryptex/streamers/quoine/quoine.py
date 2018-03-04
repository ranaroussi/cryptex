#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests


class QuoineBase:

    public_url = "https://api.quoine.com"
    name = "quoine"

    def returnProducts(self, base, quote):
        url = self.public_url + "/products"
        r = requests.get(url, data={}, headers={}, params={})
        return r.json()

    def returnPriceLevels(self, product_id):
        url = self.public_url + "/products/" + product_id + "/price_levels"
        options = {"id": product_id, "full": 1}
        r = requests.get(url, data={}, headers={}, params=options)
        return r.json()

    def returnExecutions(self, product_id, limit):
        url = self.public_url + "/executions"
        options = {"product_id": product_id, "limit": limit}
        r = requests.get(url, data={}, headers={}, params=options)
        return r.json()
