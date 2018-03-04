#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import signal
import multitasking
from .wrapper import BithumbWrapper

multitasking.set_engine("process")
signal.signal(signal.SIGINT, multitasking.killall)


class BithumbStreamer(BithumbWrapper):

    last_trade = None
    last_orderbook = None

    def streamCallback(self, data, **kwargs):
        """ this method will be overridden from outside """
        pass

    @multitasking.task
    def streamTrades(self, base, quote, depth=1, sleep=1):
        while True:
            trade = self.getTrades(base, quote, depth)
            if trade != self.last_trade:
                self.last_trade = trade
                self.streamCallback(trade)
            time.sleep(sleep)

    @multitasking.task
    def streamOrderbook(self, base, quote, depth=10, sleep=1):
        while True:
            orderbook = self.getOrderbook(base, quote, depth)
            if orderbook != self.last_orderbook:
                self.last_orderbook = orderbook
                self.streamCallback(orderbook)
            time.sleep(sleep)
