#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import random
from ws4py.client.threadedclient import WebSocketClient


class HitbtcChannel(WebSocketClient):

    method = None
    symbol = None
    depth = 1
    base = None
    quote = None

    def init(self, method, symbol, depth, base, quote):
        self.method = method
        self.symbol = symbol
        self.depth = depth
        self.base = base
        self.quote = quote

    def getParams(self):
        return {"method": self.method,
                "symbol": self.symbol,
                "depth": self.depth,
                "base": self.base,
                "quote": self.quote}

    def opened(self):
        self.send(json.dumps({
            "method": self.method,
            "params": {
                "symbol": self.symbol
            },
            "id": str(random.random())
        }))

    def closed(self, code, reason=None):
        print("Closed down", code, reason)
        self.wsCallback(self.getParams(), {"method": "disconnect"})

    def received_message(self, message):
        parsedMessage = json.loads(message.data.decode("utf-8"))
        self.wsCallback(self.getParams(), parsedMessage)
