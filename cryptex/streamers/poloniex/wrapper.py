#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .poloniex import PoloniexBase
import datetime
from ..wrapper import Wrapper


class PoloniexWrapper(PoloniexBase, Wrapper):

    def getTrades(self, base, quote, depth=1):

        if depth < 0:
            return self.getBaseData(base=base,
                                    quote=quote,
                                    format="trade")

        raw_result = self.returnTrades(
            pair=self.getPair(base, quote, "upper", "_"))

        if "error" in raw_result:
            # print(raw_result)
            return

        result = []
        for raw in raw_result[:depth]:

            data = self.getBaseData(base=base,
                                    quote=quote,
                                    format="trade")
            data["timestamp"] = datetime.datetime.strptime(
                raw["date"], '%Y-%m-%d %H:%M:%S').timestamp()
            data["data"] = {"base": float(
                raw["amount"]), "quote": float(raw["rate"])}

            result.append(data)

        return result

    def getOrderbook(self, base, quote, depth=10):
        if depth < 0:
            return self.getBaseData(base=base,
                                    quote=quote,
                                    format="orderbook")

        raw_result = self.returnOrderBook(
            pair=self.getPair(base, quote, "upper", "_"), depth=depth)

        if "error" in raw_result:
            # print(raw_result)
            return

        asksb = []
        asksq = []
        for ask in raw_result["asks"]:
            asksb.append(ask[1])
            asksq.append(ask[0])

        bidsb = []
        bidsq = []
        for bid in raw_result["bids"]:
            bidsb.append(bid[1])
            bidsq.append(bid[0])

        result = self.getBaseData(base=base,
                                  quote=quote,
                                  format="orderbook")
        result["data"] = {"bids": {"base": bidsb, "quote": bidsq},
                          "asks": {"base": asksb, "quote": asksq}}

        return result
