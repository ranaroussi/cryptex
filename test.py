#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import signal
import multitasking

from cryptex.blotter import Blotter

multitasking.set_engine("process")
signal.signal(signal.SIGINT, multitasking.killall)


@multitasking.task
def on_orderbook(df_bids, df_asks, **kwargs):
    # print(df_bids, df_asks)
    pass


@multitasking.task
def on_tick(df, **kwargs):
    # print(df)
    pass


@multitasking.task
def on_bar(df, **kwargs):
    # print(df)
    pass


if __name__ == '__main__':

    handler = Blotter(market="binance",
                      bar_handler=on_bar,
                      tick_handler=on_tick,
                      book_handler=on_orderbook)

    handler.stream(base="ETH", quote="BTC", freq='3S', orderbook=True)
