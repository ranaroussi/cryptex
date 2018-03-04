#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from cryptex.data import poloniex as marketdata
# from cryptex.actions import poloniex as markethandler

"""
Notes
- ploniex AND bittrex uses a reverse base/quote => USDT/BTC
- kraken uses XBT as BTC symbol
"""

def streamCallback(data):
    """ default callback """
    print(">>>>>", data)


if __name__ == '__main__':

    # initialize streamer
    streamer = marketdata.streamer()

    # set callback
    streamer.streamCallback = streamCallback

    # run streamers
    streamer.streamOrderbook(base="usdt", quote="btc")
    # streamer.streamTrades(base="usdt", quote="btc")

    # streamer.streamOrderbook(base="eth", quote="btc")
    # streamer.streamTrades(base="eth", quote="btc")
