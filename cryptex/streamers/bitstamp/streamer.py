#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import signal
import multitasking
from .bitstamp import BitstampChannel
from .wrapper import BitstampWrapper

multitasking.set_engine("process")
signal.signal(signal.SIGINT, multitasking.killall)


class BitstampStreamer(BitstampWrapper):

    @multitasking.task
    def streamTrades(self, base, quote, depth=1, sleep=.1):
        symbol = self.getPair(base, quote)

        channel = BitstampChannel()
        channel.init(event="trade",
                     channel="live_trades",
                     key=self.app_key,
                     symbol=symbol,
                     depth=depth,
                     base=base,
                     quote=quote)
        channel.wsCallback = self.tradesCallback
        self.dataCallback = self.streamCallback

        while True:
            time.sleep(sleep)

    @multitasking.task
    def streamOrderbook(self, base, quote, depth=10, sleep=.1):
        symbol = self.getPair(base, quote)

        channel = BitstampChannel()
        channel.init(event="data",
                     channel="order_book",
                     key=self.app_key,
                     symbol=symbol,
                     depth=depth,
                     base=base,
                     quote=quote)
        channel.wsCallback = self.orderbookCallback
        self.dataCallback = self.streamCallback

        while True:
            time.sleep(sleep)
