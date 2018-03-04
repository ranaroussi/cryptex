#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ..wrapper import Wrapper


class BitfinexWrapper(Wrapper):

    ws_url = "wss://api.bitfinex.com/ws/2"
    name = "bitfinex"

    def tradesCallback(self, params, raw_data):
        if not isinstance(raw_data, list):

            if raw_data["event"] == "disconnect":
                empty = self.getBaseData(base=params["base"],
                                         quote=params["quote"],
                                         format="trade")
                if params["depth"] == 1:
                    self.dataCallback(empty)
                    return
                self.dataCallback([empty])
                return

            if raw_data["event"] == "info" or raw_data["event"] == "subscribed":
                return

        if raw_data[1] == "hb":
            # heartbeat
            return

        if isinstance(raw_data[1], list):
            # snapshot
            result = []
            for raw in raw_data[1][:params["depth"]]:
                data = self.getBaseData(base=params["base"],
                                        quote=params["quote"],
                                        format="trade")
                data["timestamp"] = int(raw[1]) / 1000
                data["data"] = {"base": abs(float(raw_data[2])),
                                "quote": float(raw_data[3])}
                result.append(data)

            if params["depth"] == 1:
                self.dataCallback(result[0])
            else:
                self.dataCallback(result)

            return

        if raw_data[1] == "te" or raw_data[1] == "tu":

            # tu = update, te = ?
            data = self.getBaseData(base=params["base"],
                                    quote=params["quote"],
                                    format="trade")
            data["timestamp"] = int(raw_data[2][1]) / 1000
            data["data"] = {"base": abs(float(raw_data[2][2])),
                            "quote": float(raw_data[2][3]),
                            }

            if params["depth"] == 1:
                self.dataCallback(data)
            else:
                self.dataCallback([data])

            return

    def orderbookCallback(self, params, raw_data):
        if not isinstance(raw_data, list):

            if raw_data["event"] == "disconnect":
                empty = self.getBaseData(
                    base=params["base"], quote=params["quote"], format="trade")
                if params["depth"] == 1:
                    self.dataCallback(empty)
                    return
                self.dataCallback([empty])
                return

            if raw_data["event"] == "info" or raw_data["event"] == "subscribed":
                return

        if raw_data[1] == "hb":
            # heartbeat
            return

        result = self.getBaseData(
            base=params["base"], quote=params["quote"], format="orderbook")

        if isinstance(raw_data[1], list) and not isinstance(raw_data[1][0], list):
            # update
            data = {"base": float(raw_data[1][2]),
                    "quote": abs(float(raw_data[1][0]))}

            if raw_data[1][2] < 0:
                result["data"] = {"asks": data, "bids": {}}
            else:
                result["data"] = {"asks": {}, "bids": data}

        else:

            # snapshot
            asksb = []
            asksq = []
            bidsb = []
            bidsq = []

            for data in raw_data[1][:params["depth"]]:
                if data[2] < 0:
                    asksb.append(abs(float(data[2])))
                    asksq.append(float(data[0]))
                else:
                    bidsb.append(abs(float(data[2])))
                    bidsq.append(float(data[0]))

            result["data"] = {"bids": {"base": bidsb, "quote": bidsq},
                              "asks": {"base": asksb, "quote": asksq}}

        self.dataCallback(result)
