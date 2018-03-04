#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from ..wrapper import Wrapper


class GdaxWrapper(Wrapper):
    ws_url = "wss://ws-feed.gdax.com"
    name = "gdax"

    def tradesCallback(self, params, raw_data):
        if "method" in raw_data and raw_data["method"] == "disconnect":
            empty = self.getBaseData(base=params["base"],
                                     quote=params["quote"],
                                     format="trade")
            if params["depth"] == 1:
                self.dataCallback(empty)
                return
            self.dataCallback([empty])
            return

        result = self.getBaseData(base=params["base"],
                                  quote=params["quote"],
                                  format="trade")

        if not "time" in raw_data:
            # the first record returns without time and last_size
            return

        result["timestamp"] = time.mktime(time.strptime(
            raw_data["time"], '%Y-%m-%dT%H:%M:%S.%fZ'))
        result["data"] = {"base": float(raw_data["last_size"]),
                          "quote": float(raw_data["price"])}

        if params["depth"] == 1:
            self.dataCallback(result)
        else:
            self.dataCallback([result])

    def orderbookCallback(self, params, raw_data):
        if raw_data["type"] == "received":

            asksb = []
            asksq = []
            bidsb = []
            bidsq = []

            if raw_data["side"] == "buy":
                asksb.append(float(raw_data["size"]))
                asksq.append(float(raw_data["price"]))
            elif raw_data["side"] == "sell":
                bidsb.append(float(raw_data["size"]))
                bidsq.append(float(raw_data["price"]))

            result = self.getBaseData(
                base=params["base"], quote=params["quote"], format="trade")
            result["timestamp"] = time.time()
            result["data"] = {"bids": {"base": bidsb, "quote": bidsq},
                              "asks": {"base": asksb, "quote": asksq}}

            self.dataCallback(result)
