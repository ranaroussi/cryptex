#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from ..wrapper import Wrapper


class HitbtcWrapper(Wrapper):
    ws_url = "wss://api.hitbtc.com/api/2/ws"
    name = "hitbtc"

    def tradesCallback(self, params, raw_data):
        if not "method" in raw_data:
            print("raw: ")
            print(raw_data)
            return

        if raw_data["method"] == "disconnect":
            empty = self.getBaseData(base=params["base"],
                                     quote=params["quote"],
                                     format="trade")
            if params["depth"] == 1:
                self.dataCallback(empty)
                return
            self.dataCallback([empty])
            return

        result = []
        for raw in raw_data["params"]["data"][:params["depth"]]:

            data = self.getBaseData(base=params["base"],
                                    quote=params["quote"],
                                    format="trade")
            data["timestamp"] = time.mktime(time.strptime(
                raw_data["timestamp"], '%Y-%m-%dT%H:%M:%S.%fZ'))

            data["data"] = {"base": float(raw["quantity"]),
                            "quote": float(raw["price"])}
            result.append(data)

        if params["depth"] == 1:
            self.dataCallback(result[0])
        else:
            self.dataCallback(result)

    def orderbookCallback(self, params, raw_data):
        if not "method" in raw_data:
            print("raw: ")
            print(raw_data)
            return

        if raw_data["method"] == "disconnect":
            self.dataCallback(self.getBaseData(
                base=params["base"],
                quote=params["quote"],
                format="orderbook"))
            return

        asksb = []
        asksq = []
        for ask in raw_data["params"]["ask"][:params["depth"]]:
            asksb.append(float(ask["size"]))
            asksq.append(float(ask["price"]))

        bidsb = []
        bidsq = []
        for bid in raw_data["params"]["bid"][:params["depth"]]:
            bidsb.append(float(bid["size"]))
            bidsq.append(float(bid["price"]))

        result = self.getBaseData(base=params["base"],
                                  quote=params["quote"],
                                  format="orderbook")
        result["timestamp"] = int(time.time())
        result["data"] = {
            "bids": {
                "base": bidsb,
                "quote": bidsq,
            },
            "asks": {
                "base": asksb,
                "quote": asksq,
            }
        }

        self.dataCallback(result)
