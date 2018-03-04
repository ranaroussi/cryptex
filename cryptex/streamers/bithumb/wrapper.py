#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from .bithumb import BithumbBase
from ..wrapper import Wrapper


class BithumbWrapper(BithumbBase, Wrapper):

    def getTrades(self, base, quote, depth=1):
        if depth < 0:
            return self.getBaseData(base=base,
                                    quote=quote,
                                    format="trade")

        raw_result = self.returnRecentTransactions(
            order_currency=base.upper())

        result = []
        for raw in raw_result["data"][:depth]:
            data = self.getBaseData(base=base,
                                    quote=quote,
                                    format="trade")

            data["timestamp"] = time.mktime(time.strptime(
                raw["transaction_date"], '%Y-%m-%d %H:%M:%S'))

            data["data"] = {"base": float(raw["total"]),
                            "quote": float(raw["price"])}
            result.append(data)

        if depth == 1:
            return result[0]

        return result

    def getOrderbook(self, base, quote, depth=10):
        base_data = {
            "format": "orderbook",
            "exchange": self.name,
            "base": base.lower(),
            "quote": quote.lower(),
            "timestamp": time.time(),
            "data": {
                "base": [],
                "quote": [],
            }
        }
        if depth < 0:
            return base_data

        raw_result = self.returnOrderBook(order_currency=base.upper())

        asksb = []
        asksq = []
        for ask in raw_result["data"]["asks"][:depth]:
            asksb.append(float(ask["quantity"]))
            asksq.append(float(ask["price"]))

        bidsb = []
        bidsq = []
        for bid in raw_result["data"]["bids"][:depth]:
            bidsb.append(float(bid["quantity"]))
            bidsq.append(float(bid["price"]))

        result = dict(base_data)
        result["timestamp"] = time.time()
        result["data"] = {
            "bids": {
                "base": bidsb,
                "quote": bidsq,
            },
            "asks": {
                "base": asksb,
                "quote": asksq,
            }
        }

        return result
