#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import signal
import multitasking
from .hitbtc import HitbtcChannel
from .wrapper import HitbtcWrapper

multitasking.set_engine("process")
signal.signal(signal.SIGINT, multitasking.killall)


class HitbtcStreamer(HitbtcWrapper):

    @multitasking.task
    def streamTrades(self, base, quote, depth=1, sleep=1):
        symbol = self.getPair(base, quote)

        channel = HitbtcChannel(self.ws_url)
        channel.init(method="subscribeTrades",
                     symbol=symbol,
                     depth=depth,
                     base=base,
                     quote=quote)
        channel.wsCallback = self.tradesCallback
        self.dataCallback = self.streamCallback

        # while True:
        channel.connect()
        channel.run_forever()

    @multitasking.task
    def streamOrderbook(self, base, quote, depth=10, sleep=1):
        symbol = self.getPair(base, quote)

        channel = HitbtcChannel(self.ws_url)
        channel.init(method="subscribeOrderbook",
                     symbol=symbol,
                     depth=depth,
                     base=base,
                     quote=quote)
        channel.wsCallback = self.orderbookCallback
        self.dataCallback = self.streamCallback

        # while True:
        channel.connect()
        channel.run_forever()
