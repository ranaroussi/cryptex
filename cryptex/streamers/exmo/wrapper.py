#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .exmo import ExmoBase
from ..wrapper import Wrapper


class ExmoWrapper(ExmoBase, Wrapper):

    def getTrades(self, base, quote, depth=1):
        if depth < 0:
            return self.getBaseData(base=base,
                                    quote=quote,
                                    format="trade")

        pair = self.getPair(base, quote, "upper", "_")

        raw_result = self.returnTrades(pair, depth)

        if raw_result == {}:
            # heartbit
            return

        result = []
        for raw in raw_result[pair]:
            data = self.getBaseData(base=base,
                                    quote=quote,
                                    format="trade")
            data["timestamp"] = raw["date"]
            data["data"] = {"base": float(
                raw["quantity"]), "quote": float(raw["price"])}

            result.append(data)

        if depth == 1:
            return result[0]

        return result

    def getOrderbook(self, base, quote, depth=10):
        if depth < 0:
            return self.getBaseData(base=base,
                                    quote=quote,
                                    format="orderbook")

        pair = self.getPair(base, quote, "upper", "_")

        raw_result = self.returnOrderbook(pair, depth)

        asksb = []
        asksq = []
        for ask in raw_result[pair]["ask"][:depth]:
            asksb.append(float(ask[1]))
            asksq.append(float(ask[0]))

        bidsb = []
        bidsq = []
        for bid in raw_result[pair]["bid"][:depth]:
            bidsb.append(float(bid[1]))
            bidsq.append(float(bid[0]))

        result = self.getBaseData(base=base,
                                  quote=quote,
                                  format="orderbook")
        result["data"] = {"bids": {"base": bidsb, "quote": bidsq},
                          "asks": {"base": asksb, "quote": asksq}}

        return result
