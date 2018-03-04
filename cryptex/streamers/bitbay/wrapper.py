#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .bitbay import BitbayBase
from ..wrapper import Wrapper


class BitbayWrapper(BitbayBase, Wrapper):

    def getTrades(self, base, quote, depth):
        if depth < 0:
            return self.getBaseData(base=base,
                                    quote=quote,
                                    format="trade")

        raw_result = self.returnTrades(
            self.getPair(base=base, quote=quote))

        if "code" in raw_result:
            # print(raw_result)
            return

        result = []
        for raw in raw_result[:depth]:
            data = self.getBaseData(base=base,
                                    quote=quote,
                                    format="trade")

            data["timestamp"] = raw["date"]
            data["data"] = {"base": float(raw["amount"]),
                            "quote": float(raw["price"])}
            result.append(data)

        return result

    def getOrderbook(self, base, quote, depth):
        if depth < 0:
            return self.getBaseData(base=base,
                                    quote=quote,
                                    format="orderbook")

        raw_result = self.returnOrderbook(
            self.getPair(base=base, quote=quote))

        if "code" in raw_result:
            # print(raw_result)
            return

        asksb = []
        asksq = []
        for ask in raw_result["asks"][:depth]:
            asksb.append(ask[1])
            asksq.append(ask[0])

        bidsb = []
        bidsq = []
        for bid in raw_result["bids"][:depth]:
            bidsb.append(bid[1])
            bidsq.append(bid[0])

        result = self.getBaseData(base=base,
                                  quote=quote,
                                  format="orderbook")
        result["data"] = {"bids": {"base": bidsb, "quote": bidsq},
                          "asks": {"base": asksb, "quote": asksq}}

        return result
