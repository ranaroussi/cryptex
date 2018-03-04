#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .bitfinex import BitfinexChannel
from .wrapper import BitfinexWrapper

import multitasking
multitasking.set_engine("process")

import signal
signal.signal(signal.SIGINT, multitasking.killall)


class BitfinexStreamer(BitfinexWrapper):

    def streamCallback(self, data, **kwargs):
        """ this method will be overridden from outside """
        pass

    @multitasking.task
    def streamTrades(self, base, quote, depth=1, sleep=1):
        symbol = self.getPair(base, quote)
        channel = BitfinexChannel(self.ws_url)
        channel.init(channel="trades",
                     symbol=symbol,
                     depth=depth,
                     base=base,
                     quote=quote)
        channel.wsCallback = self.tradesCallback
        self.dataCallback = self.streamCallback

        channel.connect()
        channel.run_forever()

    @multitasking.task
    def streamOrderbook(self, base, quote, depth=10, sleep=1):
        symbol = self.getPair(base, quote)
        channel = BitfinexChannel(self.ws_url)
        channel.init(channel="book",
                     symbol=symbol,
                     depth=depth,
                     base=base,
                     quote=quote)
        channel.wsCallback = self.orderbookCallback
        self.dataCallback = self.streamCallback

        channel.connect()
        channel.run_forever()
