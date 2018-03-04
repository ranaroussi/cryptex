#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from ..wrapper import Wrapper


class BitstampWrapper(Wrapper):

    app_key = "de504dc5763aeef9ff52"
    name = "bitstamp"

    def tradesCallback(self, params, raw_data):
        data = self.getBaseData(base=params["base"],
                                quote=params["quote"],
                                format="trade")
        data["timestamp"] = raw_data["timestamp"]
        data["data"] = {"base": float(raw_data["amount"]),
                        "quote": float(raw_data["price"])}

        if params["depth"] == 1:
            self.dataCallback(data)
        else:
            self.dataCallback([data])

    def orderbookCallback(self, params, raw_data):
        asksb = []
        asksq = []
        for ask in raw_data["asks"][:params["depth"]]:
            asksb.append(float(ask[1]))
            asksq.append(float(ask[0]))

        bidsb = []
        bidsq = []
        for bid in raw_data["bids"][:params["depth"]]:
            bidsb.append(float(bid[1]))
            bidsq.append(float(bid[0]))

        result = self.getBaseData(base=params["base"],
                                  quote=params["quote"],
                                  format="trade")

        result["timestamp"] = time.time()
        result["data"] = {"bids": {"base": bidsb, "quote": bidsq},
                          "asks": {"base": asksb, "quote": asksq}}

        self.dataCallback(result)
