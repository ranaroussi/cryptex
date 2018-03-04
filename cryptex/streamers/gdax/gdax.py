#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from ws4py.client.threadedclient import WebSocketClient


class GdaxChannel(WebSocketClient):

    method = None
    symbol = None
    channel = None
    depth = 1
    base = None
    quote = None

    def init(self, channel, symbol, depth, base, quote):
        self.channel = channel
        self.symbol = symbol
        self.depth = depth
        self.base = base
        self.quote = quote

    def getParams(self):
        return {"channel": self.channel,
                "symbol": self.symbol,
                "depth": self.depth,
                "base": self.base,
                "quote": self.quote}

    def opened(self):
        self.send(json.dumps({
            "type": "subscribe",
            "product_ids": [self.symbol],
            "channels": [self.channel],
        }))

    def closed(self, code, reason=None):
        print("Closed down", code, reason)
        self.wsCallback(self.getParams(), {"method": "disconnect"})

    def received_message(self, message):
        parsedMessage = json.loads(message.data.decode("utf-8"))
        self.wsCallback(self.getParams(), parsedMessage)
