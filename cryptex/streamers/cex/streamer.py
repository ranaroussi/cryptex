#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import signal
import multitasking
from .cex import CexChannel
from .wrapper import CexWrapper

multitasking.set_engine("process")
signal.signal(signal.SIGINT, multitasking.killall)


class CexStreamer(CexWrapper):

    def streamCallback(self, data, **kwargs):
        """ this method will be overridden from outside """
        pass

    @multitasking.task
    def streamTrades(self, base, quote, depth=1, sleep=1):
        symbol = self.getPair(base, quote, "upper", "-")
        channel = CexChannel(self.ws_url)
        channel.init(symbol=symbol,
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
        symbol = self.getPair(base, quote, "upper", "-")
        channel = CexChannel(self.ws_url)
        channel.init(symbol=symbol,
                     depth=depth,
                     base=base,
                     quote=quote)
        channel.wsCallback = self.orderbookCallback
        self.dataCallback = self.streamCallback

        # while True:
        channel.connect()
        channel.run_forever()
