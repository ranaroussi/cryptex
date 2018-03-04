#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from ws4py.client.threadedclient import WebSocketClient


class CexChannel(WebSocketClient):

    symbol = None
    depth = 1
    base = None
    quote = None

    def init(self, symbol, depth, base, quote):
        self.symbol = symbol
        self.depth = depth
        self.base = base
        self.quote = quote

    def getParams(self):
        return {"symbol": self.symbol,
                "depth": self.depth,
                "base": self.base,
                "quote": self.quote}

    def opened(self):
        self.send(json.dumps({
            "e": "subscribe",
            "rooms": ["pair-" + self.symbol]
        }))

    def closed(self, code, reason=None):
        print("Closed down", code, reason)
        self.wsCallback(self.getParams(), {"e": "disconnect"})

    def received_message(self, message):
        parsedMessage = json.loads(message.data.decode("utf-8"))
        self.wsCallback(self.getParams(), parsedMessage)
