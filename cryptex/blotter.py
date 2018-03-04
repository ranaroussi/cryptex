#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
import time
import importlib
import signal

import pandas as pd
import numpy as np

import multitasking

multitasking.set_engine("process")
signal.signal(signal.SIGINT, multitasking.killall)


def datetime64_to_datetime(dt):
    """ convert numpy's datetime64 to datetime """
    dt64 = np.datetime64(dt)
    ts = (dt64 - np.datetime64('1970-01-01T00:00:00')) / np.timedelta64(1, 's')
    return datetime.utcfromtimestamp(ts)


class Blotter():

    def __init__(self, market, bar_handler=None,
                 tick_handler=None, book_handler=None):

        self._last_col = "quote"
        self._size_col = "base"
        if market in ["poloniex", "bittrex"]:
            self._last_col = "base"
            self._size_col = "quote"

        self._bars = {}
        self._ticks = {}
        self._freqs = {}
        self._last_tick_meta = {}

        # connect to market
        self.market = importlib.import_module('streamers.' + market.lower()).streamer()
        self.market.streamCallback = self.streamCallback

        # data handlers
        self.bar_handler = self.on_bar
        if bar_handler:
            self.bar_handler = bar_handler

        self.tick_handler = self.on_tick
        if tick_handler:
            self.tick_handler = tick_handler

        self.book_handler = self.on_orderbook
        if book_handler:
            self.book_handler = book_handler

    # ----------------------------------------

    @multitasking.task
    def add_stale_ticks(self):
        while True:
            for pair in list(self._ticks.keys()):
                if pair not in self._ticks:
                    continue

                last_tick_meta = self._last_tick_meta[pair]
                last_tick = self._ticks[pair][-1:].copy()
                seconds_since = (datetime.utcnow() - datetime64_to_datetime(
                    last_tick.index.values[-1])).total_seconds()

                if seconds_since >= 1:
                    last_tick['ts'] = datetime.utcnow()
                    last_tick.set_index('ts', inplace=True)

                    sizecol = last_tick_meta[self._size_col]
                    last_tick[sizecol] = 0
                    self._bar_constructur(pair, last_tick)

            time.sleep(1)

    # ----------------------------------------

    def stream(self, base, quote, freq='1T', orderbook=False):
        self._freqs[base.lower() + quote.lower()] = freq

        if orderbook:
            self.market.streamOrderbook(base, quote)
        self.market.streamTrades(base, quote)

        # for even _bar frequency, serve stale ticks with 0 volume
        self.add_stale_ticks()

    # ----------------------------------------

    @staticmethod
    def _metadata(data):
        data = dict(data)
        del data['data']
        return data

    # ----------------------------------------

    def _bar_constructur(self, pair, tick):
        last_tick_meta = self._last_tick_meta[pair]
        freq = self._freqs[pair]

        # add to _ticks df
        if pair not in self._ticks.keys():
            self._ticks[pair] = tick

        self._ticks[pair] = pd.concat([self._ticks[pair], tick])
        self._ticks[pair].index = pd.to_datetime(self._ticks[pair].index)

        # resample _ticks to bars
        last_col = last_tick_meta[self._last_col]
        size_col = last_tick_meta[self._size_col]
        _bar = self._ticks[pair][last_col].resample(freq).ohlc()
        _bar['volume'] = self._ticks[pair][size_col].resample(freq).sum()

        # replace latest _bar data with resampled ticks
        if pair not in self._bars.keys():
            self._bars[pair] = _bar

        bar_count = len(self._bars[pair])
        self._bars[pair] = self._bars[pair][self._bars[pair].index != _bar.index[-1]]
        self._bars[pair] = pd.concat([self._bars[pair], _bar[-1:]])

        # leave last bar only
        if len(self._bars[pair]) > bar_count:
            self._bars[pair] = self._bars[pair][-1:].copy()
            self.bar_handler(self._bars[pair], **last_tick_meta)

    # ----------------------------------------

    def streamCallback(self, data):
        # copy data
        data = dict(data) if isinstance(data, dict) else dict(data[0])

        if "format" not in data:
            return

        # unify pair
        data['pair'] = data['base'].lower() + data['quote'].lower()

        if data["format"] == "trade":
            tick = pd.DataFrame(index=[data['timestamp']], data=data['data'])
            tick.columns = [data[x] for x in tick.columns][::-1]
            tick.index = pd.to_datetime(tick.index, unit='s')

            self._last_tick_meta[data['pair']] = self._metadata(data)

            self.tick_handler(tick, **self._metadata(data))
            self._bar_constructur(data['pair'], tick)

        elif data["format"] == "orderbook":
            bids = pd.DataFrame(data=data['data']['bids'])
            bids.columns = [data[x] for x in bids.columns][::-1]

            asks = pd.DataFrame(data=data['data']['asks'])
            asks.columns = [data[x] for x in asks.columns][::-1]

            self.book_handler(bids, asks, **self._metadata(data))

    # ----------------------------------------

    @staticmethod
    def on_orderbook(df_bids, df_asks, **kwargs):
        pass

    @staticmethod
    def on_tick(df, **kwargs):
        pass

    @staticmethod
    def on_bar(df, **kwargs):
        pass
