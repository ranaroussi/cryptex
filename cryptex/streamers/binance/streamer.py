#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import signal
import multitasking
from .binance import BinanceChannel
from .wrapper import BinanceWrapper

multitasking.set_engine("process")
signal.signal(signal.SIGINT, multitasking.killall)


class BinanceStreamer(BinanceWrapper):

    @multitasking.task
    def streamTrades(self, base, quote, depth=1, sleep=1):
        symbol = self.getPair(base, quote)
        ws_url = self.ws_url + "/" + symbol + "@trade"

        channel = BinanceChannel(ws_url)
        channel.init(channel="@trade",
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
        ws_url = self.ws_url + "/" + symbol + "@depth"

        channel = BinanceChannel(ws_url)
        channel.init(channel="@depth",
                     symbol=symbol,
                     depth=depth,
                     base=base,
                     quote=quote)
        channel.wsCallback = self.orderbookCallback
        self.dataCallback = self.streamCallback

        channel.connect()
        channel.run_forever()
