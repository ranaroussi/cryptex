#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .livecoin import LivecoinBase
from ..wrapper import Wrapper


class LivecoinWrapper(LivecoinBase, Wrapper):

    def getTrades(self, base, quote, depth):
        if depth < 0:
            return self.getBaseData(base=base,
                                    quote=quote,
                                    format="trade")

        raw_result = self.returnLastTrades(
            self.getPair(base, quote, "upper", "/"))

        if isinstance(raw_result, dict) and not raw_result["success"]:
            # print(raw_result)
            return

        result = []
        for raw in raw_result[:depth]:
            data = self.getBaseData(base=base,
                                    quote=quote,
                                    format="trade")

            data["timestamp"] = raw["time"]
            data["data"] = {"base": float(raw["quantity"]),
                            "quote": float(raw["price"])}

            result.append(data)

        if depth == 1:
            return result[0]

        return result

    def getOrderbook(self, base, quote, depth):

        if depth < 0:
            return self.getBaseData(base=base,
                                    quote=quote,
                                    format="trade")

        raw_result = self.returnOrderBook(
            self.getPair(base, quote, "upper", "/"), depth)

        if isinstance(raw_result, dict) and "success" in raw_result and not raw_result["success"]:
            # print(raw_result)
            return

        asksb = []
        asksq = []
        for ask in raw_result["asks"]:
            asksb.append(float(ask[1]))
            asksq.append(float(ask[0]))

        bidsb = []
        bidsq = []
        for bid in raw_result["bids"]:
            bidsb.append(float(bid[1]))
            bidsq.append(float(bid[0]))

        result = self.getBaseData(base=base,
                                  quote=quote,
                                  format="orderbook")
        result["data"] = {"bids": {"base": bidsb, "quote": bidsq},
                          "asks": {"base": asksb, "quote": asksq}}

        return result
