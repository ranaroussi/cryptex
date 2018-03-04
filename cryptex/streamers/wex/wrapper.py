#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .wex import WexBase
from ..wrapper import Wrapper


class WexWrapper(WexBase, Wrapper):

    def getTrades(self, base, quote, depth):

        if depth < 0:
            return self.getBaseData(base=base,
                                    quote=quote,
                                    format="trade")

        pair = self.getPair(base, quote, "upper", "_")

        raw_result = self.returnExecutions(pair=pair,
                                           limit=depth)

        if "success" in raw_result and raw_result["success"] == 0:
            # print(raw_result)
            return

        result = []
        for raw in raw_result[pair]:

            data = self.getBaseData(base=base,
                                    quote=quote,
                                    format="trade")
            data["timestamp"] = raw["timestamp"]
            data["data"] = {"base": float(
                raw["amount"]), "quote": float(raw["price"])}
            result.append(data)

        if depth == 1:
            return result[0]

        return result

    def getOrderbook(self, base, quote, depth=10):

        if depth < 0:
            return self.getBaseData(base=base,
                                    quote=quote,
                                    format="trade")

        pair = self.getPair(base, quote, "upper", "_")

        raw_result = self.returnOrderBook(pair=pair, limit=depth)

        if "success" in raw_result and raw_result["success"] == 0:
            # print(raw_result)
            return

        asksb = []
        asksq = []
        for ask in raw_result[pair]["asks"]:
            asksb.append(ask[1])
            asksq.append(ask[0])

        bidsb = []
        bidsq = []
        for bid in raw_result[pair]["bids"]:
            bidsb.append(bid[1])
            bidsq.append(bid[0])

        result = self.getBaseData(base=base,
                                  quote=quote,
                                  format="orderbook")
        result["data"] = {"bids": {"base": bidsb, "quote": bidsq},
                          "asks": {"base": asksb, "quote": asksq}}

        return result
