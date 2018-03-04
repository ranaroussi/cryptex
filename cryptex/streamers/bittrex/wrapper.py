#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from .bittrex import BittrexBase
from ..wrapper import Wrapper


class BittrexWrapper(BittrexBase, Wrapper):

    def getTrades(self, base, quote, depth=1):
        if depth < 0:
            return self.getBaseData(base=base,
                                    quote=quote,
                                    format="trade")

        raw_result = self.returnTrades(
            self.getPair(base, quote, "upper", "-"))

        if (not raw_result["success"]):
            # print(raw_result)
            return

        result = []
        for raw in raw_result["result"][:depth]:
            data = self.getBaseData(base=base,
                                    quote=quote,
                                    format="trade")

            data["timestamp"] = time.mktime(time.strptime(
                raw["TimeStamp"], '%Y-%m-%dT%H:%M:%S.%f'))

            data["data"] = {"base": float(raw["Quantity"]),
                            "quote": float(raw["Price"])}
            result.append(data)

        if depth == 1:
            return result[0]

        return result

    def getOrderbook(self, base, quote, depth=10):
        if depth < 0:
            return self.getBaseData(base=base,
                                    quote=quote,
                                    format="orderbook")

        raw_result = self.returnOrderbook(
            self.getPair(base, quote, "upper", "-"))

        if "result" not in raw_result:
            return

        asksb = []
        asksq = []
        for ask in raw_result["result"]["buy"][:depth]:
            asksb.append(float(ask["Quantity"]))
            asksq.append(float(ask["Rate"]))

        bidsb = []
        bidsq = []
        for bid in raw_result["result"]["sell"][:depth]:
            bidsb.append(float(bid["Quantity"]))
            bidsq.append(float(bid["Rate"]))

        result = self.getBaseData(base=base,
                                  quote=quote,
                                  format="orderbook")
        result["data"] = {"bids": {"base": bidsb, "quote": bidsq},
                          "asks": {"base": asksb, "quote": asksq}}

        return result
