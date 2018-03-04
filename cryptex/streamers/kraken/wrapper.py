#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .kraken import KrakenBase
from ..wrapper import Wrapper


class KrakenWrapper (KrakenBase, Wrapper):

    @staticmethod
    def pairData(data, base, quote):
        """ data pair key can differ from pair key """
        base = base.upper()
        quote = quote.upper()

        for key in data.keys():
            if base in key and quote in key:
                return data[key]

    def getTrades(self, base, quote, depth=1):

        if depth < 0:
            return self.getBaseData(base=base,
                                    quote=quote,
                                    format="trade")

        pair = self.getPair(base, quote)
        raw_result = self.returnTrades(pair)

        if "error" in raw_result and raw_result["error"] != []:
            # print(raw_result)
            return

        result = []
        for raw in self.pairData(raw_result['result'],
                                 base, quote)[:depth]:

            data = self.getBaseData(base=base,
                                    quote=quote,
                                    format="trade")
            data["timestamp"] = float(raw[2])
            data["data"] = {
                "base": float(raw[1]),
                "quote": float(raw[0]),
            }
            result.append(data)

        if depth == 1:
            return result[0]

        return result

    def getOrderbook(self, base, quote, depth=10):

        if depth < 0:
            return self.getBaseData(base=base,
                                    quote=quote,
                                    format="trade")

        pair = self.getPair(base, quote)
        raw_result = self.returnOrderBook(pair, depth)

        if "error" in raw_result and raw_result["error"] != []:
            # print(raw_result)
            return

        asksb = []
        asksq = []
        for ask in self.pairData(raw_result['result'],
                                 base, quote)["asks"][:depth]:
            asksb.append(ask[1])
            asksq.append(ask[0])

        bidsb = []
        bidsq = []
        for bid in self.pairData(raw_result['result'],
                                 base, quote)["bids"][:depth]:
            bidsb.append(bid[1])
            bidsq.append(bid[0])

        result = self.getBaseData(base=base,
                                  quote=quote,
                                  format="orderbook")
        result["data"] = {"bids": {"base": bidsb, "quote": bidsq},
                          "asks": {"base": asksb, "quote": asksq}}

        return result
