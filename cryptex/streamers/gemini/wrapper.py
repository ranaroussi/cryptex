#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .gemini import GeminiBase
from ..wrapper import Wrapper


class GeminiWrapper(GeminiBase, Wrapper):

    def getTrades(self, base, quote, depth):
        if depth < 0:
            return self.getBaseData(base=base,
                                    quote=quote,
                                    format="trade")

        raw_result = self.returnTrades(
            self.getPair(base=base, quote=quote), depth)

        if "price" not in raw_result[0]:
            # print(raw_result)
            return

        result = []
        for raw in raw_result[:depth]:
            data = self.getBaseData(base=base,
                                    quote=quote,
                                    format="trade")
            data["timestamp"] = raw["timestamp"]
            data["data"] = {"base": float(raw["amount"]),
                            "quote": float(raw["price"])}
            result.append(data)

        if depth == 1:
            return result[0]

        return result

    def getOrderbook(self, base, quote, depth):
        if depth < 0:
            return self.getBaseData(base=base,
                                    quote=quote,
                                    format="orderbook")

        raw_result = self.returnOrderbook(
            self.getPair(base=base, quote=quote))

        if "bids" not in raw_result.keys():
            # print(raw_result)
            return

        asksb = []
        asksq = []
        for ask in raw_result["asks"][:depth]:
            asksb.append(ask["amount"])
            asksq.append(ask["price"])

        bidsb = []
        bidsq = []
        for bid in raw_result["bids"][:depth]:
            bidsb.append(bid["amount"])
            bidsq.append(bid["price"])

        result = self.getBaseData(base=base,
                                  quote=quote,
                                  format="orderbook")
        result["data"] = {"bids": {"base": bidsb, "quote": bidsq},
                          "asks": {"base": asksb, "quote": asksq}}

        return result
