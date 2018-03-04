#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import importlib

from future.builtins import bytes
from future.standard_library import hooks
with hooks():  # Python 2/3 compat
    from urllib.parse import urlparse, quote_plus

from abc import ABCMeta, abstractmethod

import requests
import pandas as pd


def Trader(market, **kwargs):
    return importlib.import_module(
        'traders.' + market.lower()).init(**kwargs).Trader()


class BaseTrader():

    __metaclass__ = ABCMeta

    base_url = "/"

    # -----------------------------------

    @staticmethod
    def as_df(data):
        df = pd.DataFrame(data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index(['timestamp'], inplace=True)
        df.sort_index(inplace=True)
        return df

    @staticmethod
    def filter_kwargs(kwargs):
        filter_str = ""
        if 'filter' in kwargs:
            filter_str = quote_plus(json.dumps(kwargs['filter']))
            del kwargs['filter']

        return kwargs, filter_str

    @staticmethod
    def prepare_data(data):
        if data is None:
            data = {}
        elif isinstance(data, (bytes, bytearray)):
            data = data.decode('utf8')
        return data

    # -----------------------------------

    @abstractmethod
    def get_positions(self, symbol=None, openonly=True, **kwargs):
        pass

    @abstractmethod
    def get_balance(self, **kwargs):
        pass

    @abstractmethod
    def get_orders(self, symbol=None, openonly=True, reverse=True, **kwargs):
        pass

    @abstractmethod
    def send_order(self, symbol, qty=None, price=None,
                   stop=None, trailing_stop=None, hidden=False, **kwargs):
        pass

    @abstractmethod
    def close_position(self, symbol):
        pass

    @abstractmethod
    def update_order(self, orderId, qty=None, **kwargs):
        pass

    @abstractmethod
    def cancel_orders(self, orderId=None, clOrdId=None, text=''):
        pass

    @abstractmethod
    def set_order_ttl(self, timeout=60):
        pass
        # return self.post('/api/v1/order/cancelAllAfter', timeout=timeout * 1000)

    # -----------------------------------

    def get(self, path, auth=None, **kwargs):
        data = self.prepare_data(kwargs)
        url = self.base_url + path
        # auth = APIKeyAuth(self.api_key, self.api_secret)
        return requests.get(url, data=data, auth=auth).json()

    def post(self, path, auth=None, **kwargs):
        data = self.prepare_data(kwargs)
        url = self.base_url + path
        return requests.post(url, data=data, auth=auth).json()

    def put(self, path, auth=None, **kwargs):
        data = self.prepare_data(kwargs)
        url = self.base_url + path
        return requests.put(url, data=data, auth=auth).json()

    def delete(self, path, auth=None, **kwargs):
        data = self.prepare_data(kwargs)
        url = self.base_url + path
        return requests.delete(url, data=data, auth=auth).json()
