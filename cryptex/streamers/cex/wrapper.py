#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from ..wrapper import Wrapper


class CexWrapper(Wrapper):

    ws_url = "wss://ws.cex.io/ws/"
    name = "cex"

    def tradesCallback(self, params, raw_data):
        if raw_data["e"] == "disconnect":
            empty = self.getBaseData(base=params["base"],
                                     quote=params["quote"],
                                     format="trade")
            if params["depth"] == 1:
                self.dataCallback(empty)
                return
            self.dataCallback([empty])
            return

        elif raw_data["e"] == "history":

            result = []
            for raw in raw_data["data"]:
                data = self.getBaseData(base=params["base"],
                                        quote=params["quote"],
                                        format="trade")
                raw_split = raw.split(':')

                data["timestamp"] = int(raw_split[1]) / 1000
                data["data"] = {"base": float(raw_split[2]) / 10000000,
                                "quote": float(raw_split[3])}
                result.append(data)

            if params["depth"] == 1:
                self.dataCallback(result[0])
            else:
                self.dataCallback(result)

        elif raw_data["e"] == "history-update":

            result = []
            for raw in raw_data["data"]:
                data = self.getBaseData(base=params["base"],
                                        quote=params["quote"],
                                        format="trade")

                data["timestamp"] = int(raw[1]) / 1000
                data["data"] = {"base": float(raw[2]) / 10000000,
                                "quote": float(raw[3])}
                result.append(data)

            if params["depth"] == 1:
                self.dataCallback(result[0])
            else:
                self.dataCallback(result)

    def orderbookCallback(self, params, raw_data):
        if raw_data["e"] == "disconnect":
            empty = self.getBaseData(base=params["base"],
                                     quote=params["quote"],
                                     format="orderbook")
            if params["depth"] == 1:
                self.dataCallback(empty)
                return
            self.dataCallback([empty])
            return

        elif raw_data["e"] == "md":

            asksb = []
            asksq = []
            for ask in raw_data["data"]["sell"][:params["depth"]]:
                asksb.append(float(ask[0]))
                asksq.append(float(ask[1]))

            bidsb = []
            bidsq = []
            for bid in raw_data["data"]["buy"][:params["depth"]]:
                bidsb.append(float(bid[0]))
                bidsq.append(float(bid[1]))

            result = self.getBaseData(base=params["base"],
                                      quote=params["quote"],
                                      format="trade")
            result["timestamp"] = time.time()
            result["data"] = {"bids": {"base": bidsb, "quote": bidsq},
                              "asks": {"base": asksb, "quote": asksq}}

            self.dataCallback(result)

        elif raw_data["e"] == "md_groupped":

            asksb = []
            asksq = []
            count = 0
            for ask in raw_data["data"]["sell"]:
                count += 1
                asksb.append(float(raw_data["data"]["sell"][ask] / 1000000))
                asksq.append(float(ask))
                if count == params["depth"]:
                    break

            bidsb = []
            bidsq = []
            count = 0
            for bid in raw_data["data"]["buy"]:
                count += 1
                bidsb.append(float(raw_data["data"]["buy"][bid] / 10000000))
                bidsq.append(float(bid))
                if count == params["depth"]:
                    break

            result = self.getBaseData(base=params["base"],
                                      quote=params["quote"],
                                      format="trade")
            result["timestamp"] = time.time()
            result["data"] = {"bids": {"base": bidsb, "quote": bidsq},
                              "asks": {"base": asksb, "quote": asksq}}

            self.dataCallback(result)
