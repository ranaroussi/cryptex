#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import pusherclient
from ..wrapper import Wrapper


class BitstampChannel():

    channel = None
    symbol = None
    depth = 1
    base = None
    quote = None
    pusher = None
    key = None
    pusher = None
    event = None

    def init(self, key, event, channel, symbol, depth, base, quote):
        self.event = event
        self.symbol = symbol
        self.depth = depth
        self.base = base
        self.quote = quote
        self.key = key

        if base == "btc" and quote == "usd":
            self.channel = channel
        else:
            self.channel = channel + "_" + self.symbol

        self.pusher = pusherclient.Pusher(self.key)
        self.pusher.connection.bind(
            'pusher:connection_established', self.opened)
        self.pusher.connect()

    def getParams(self):
        return {"channel": self.channel,
                "event": self.event,
                "symbol": self.symbol,
                "depth": self.depth,
                "base": self.base,
                "quote": self.quote}

    def opened(self, data=None):
        channel = self.pusher.subscribe(self.channel)
        channel.bind(self.event, self.received_message)

    def closed(self, code, reason=None):
        print("Closed down", code, reason)
        self.wsCallback(self.getParams(), {"event": "disconnect"})

    def received_message(self, message):
        parsedMessage = json.loads(message)
        self.wsCallback(self.getParams(), parsedMessage)
