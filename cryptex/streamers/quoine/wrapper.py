#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .quoine import QuoineBase
from ..wrapper import Wrapper


class QuoineWrapper(QuoineBase, Wrapper):

    def getProductID(self, base, quote):
        products = self.returnProducts(base=base, quote=quote)
        for product in products:
            if product["quoted_currency"] == quote.upper() and \
                    product["base_currency"] == base.upper():
                return product["id"]

        return None

    def getTrades(self, base, quote, depth=1):
        if depth < 0:
            return self.getBaseData(base=base,
                                    quote=quote,
                                    format="trade")

        product_id = self.getProductID(base, quote)
        if product_id is None:
            return {"success": False, "message": "Product ID not found"}

        raw_result = self.returnExecutions(product_id=product_id, limit=depth)

        result = []
        for raw in raw_result["models"]:

            data = self.getBaseData(base=base,
                                    quote=quote,
                                    format="trade")
            data["timestamp"] = raw["created_at"]
            data["data"] = {"base": float(
                raw["quantity"]), "quote": float(raw["price"])}

            result.append(data)

        return result

    def getOrderbook(self, base, quote, depth=10):

        if depth < 0:
            return self.getBaseData(base=base, quote=quote, format="orderbook")

        product_id = self.getProductID(base, quote)
        if (product_id == None):
            return {"success": False, "message": "Product ID not found"}

        raw_result = self.returnPriceLevels(product_id=product_id)

        asksb = []
        asksq = []
        for ask in raw_result["buy_price_levels"][:depth]:
            asksb.append(ask[1])
            asksq.append(ask[0])

        bidsb = []
        bidsq = []
        for bid in raw_result["sell_price_levels"][:depth]:
            bidsb.append(bid[1])
            bidsq.append(bid[0])

        result = self.getBaseData(base=base, quote=quote, format="orderbook")
        result["data"] = {"bids": {"base": bidsb, "quote": bidsq},
                          "asks": {"base": asksb, "quote": asksq}}

        return result
