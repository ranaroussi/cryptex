#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .getbtc import GetbtcBase
from ..wrapper import Wrapper


class GetbtcWrapper(GetbtcBase, Wrapper):

    def getTrades(self, base, quote, depth=1):

        if depth < 0:
            return self.getBaseData(base=base,
                                    quote=quote,
                                    format="trade")

        raw_result = self.returnTransactions(quote.upper(),
                                             limit=depth)

        if "errors" in raw_result:
            # print(raw_result)
            return

        result = []
        for value in raw_result["transactions"]:
            if value != "request_currency" and raw_result[
                    "transactions"][value]["currency"] == quote.upper():

                data = self.getBaseData(base=base, quote=quote, format="trade")
                data["timestamp"] = raw_result["transactions"][value]["timestamp"]
                data["data"] = {"base": float(raw_result["transactions"][value]["btc"]),
                                "quote": float(raw_result["transactions"][value]["price"])}

                result.append(data)

        if depth == 1:
            return result[0]

        return result

    def getOrderbook(self, base, quote, depth):

        if depth < 0:
            return self.getBaseData(base=base,
                                    quote=quote,
                                    format="trade")

        raw_result = self.returnOrderBook(quote.upper(),
                                          limit=depth)

        if "errors" in raw_result:
            # print(raw_result)
            return

        asksb = []
        asksq = []
        for ask in raw_result["order-book"]["ask"]:
            if ask["converted_from"] is None:
                asksb.append(float(ask["order_amount"]))
                asksq.append(float(ask["price"]))

        bidsb = []
        bidsq = []
        for bid in raw_result["order-book"]["bid"]:
            if bid["converted_from"] is None:
                bidsb.append(float(bid["order_amount"]))
                bidsq.append(float(bid["price"]))

        result = self.getBaseData(base=base,
                                  quote=quote,
                                  format="orderbook")
        result["data"] = {"bids": {"base": bidsb, "quote": bidsq},
                          "asks": {"base": asksb, "quote": asksq}}

        return result
