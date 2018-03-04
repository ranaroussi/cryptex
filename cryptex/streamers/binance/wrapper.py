#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from ..wrapper import Wrapper


class BinanceWrapper(Wrapper):

    ws_url = "wss://stream.binance.com:9443/ws"
    name = "binance"

    def tradesCallback(self, params, raw_data):
        data = self.getBaseData(base=params["base"],
                                quote=params["quote"],
                                format="trade")
        data["timestamp"] = int(raw_data["T"]) / 1000
        data["data"] = {"base": float(raw_data["q"]),
                        "quote": float(raw_data["p"])}

        if params["depth"] == 1:
            self.dataCallback(data)
        else:
            self.dataCallback([data])

    def orderbookCallback(self, params, raw_data):
        asksb = []
        asksq = []
        if "a" in raw_data.keys():
            for ask in raw_data["a"][:params["depth"]]:
                asksb.append(float(ask[1]))
                asksq.append(float(ask[0]))

        bidsb = []
        bidsq = []
        if "b" in raw_data.keys():
            for bid in raw_data["b"][:params["depth"]]:
                bidsb.append(float(bid[1]))
                bidsq.append(float(bid[0]))

        result = self.getBaseData(base=params["base"],
                                  quote=params["quote"],
                                  format="orderbook")
        result["timestamp"] = time.time()
        result["data"] = {"bids": {"base": bidsb, "quote": bidsq},
                          "asks": {"base": asksb, "quote": asksq}}

        self.dataCallback(result)
