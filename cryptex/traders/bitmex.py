#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# BitMex API
import requests
import json
import pandas as pd
from requests.auth import AuthBase
import time
import hashlib
import hmac
from future.builtins import bytes
from future.standard_library import hooks
with hooks():  # Python 2/3 compat
    from urllib.parse import urlparse, quote_plus


from ..trader import BaseTrader

def prepare_data(data):
    if data is None:
        data = {}
    elif isinstance(data, (bytes, bytearray)):
        data = data.decode('utf8')
    return data

# Generates an API signature.
# https://testnet.bitmex.com/app/apiKeysUsage#Authenticating-with-an-API-Key
def generate_signature(secret, method, url, nonce, data=None):
    """Generate a request signature compatible with BitMEX."""

    # Parse the url so we can remove the base and extract just the path.
    parsedURL = urlparse(url)
    path = parsedURL.path
    if parsedURL.query:
        path = path + '?' + parsedURL.query

    data = prepare_data(data)

    # print "Computing HMAC: %s" % method + path + str(nonce) + data
    message = method.upper() + path + str(nonce) + data

    signature = hmac.new(bytes(secret, 'utf8'), bytes(
        message, 'utf8'), digestmod=hashlib.sha256).hexdigest()
    return signature


class APIKeyAuth(AuthBase):

    """Attaches API Key Authentication to the given Request object."""

    def __init__(self, apiKey, apiSecret):
        """Init with Key & Secret."""
        self.apiKey = apiKey
        self.apiSecret = apiSecret

    def __call__(self, r):
        """Called when forming a request - generates api key headers."""
        # modify and return the request
        nonce = int(round(time.time() * 1000))
        r.headers['api-nonce'] = str(nonce)
        r.headers['api-key'] = self.apiKey
        r.headers['api-signature'] = generate_signature(
            self.apiSecret, r.method, r.url, nonce, r.body or '')
        # print(nonce, r.headers)
        return r


class BitMEX(BaseTrader):
    def __init__(self, api_key, api_secret, testnet=False):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = 'https://www.bitmex.com'
        if testnet:
            self.base_url = 'https://testnet.bitmex.com'

    # -----------------------------------

    # -----------------------------------

    def get_positions(self, symbol=None, openonly=True, **kwargs):
        kwargs['symbol'] = symbol
        kwargs['filter'] = { 'isOpen': openonly }

        if "columns" not in kwargs:
             kwargs['columns'] = ','.join([
                'currentQty',
                'avgCostPrice',
                'lastPrice',
                'breakEvenPrice',
                'bankruptPrice',
                'commission',
                'unrealisedCost',
                'unrealisedGrossPnl',
                'unrealisedPnl',
                'unrealisedPnlPcnt',
                'unrealisedRoePcnt',
                'unrealisedTax',
                'varMargin'])

        kwargs, filter_str = self.filter_kwargs(kwargs)
        auth = APIKeyAuth(self.api_key, self.api_secret)
        return self.get('/api/v1/position?filter='+filter_str, auth, **kwargs)

    def get_positions_raw(self, symbol=None, openonly=True, **kwargs):
        kwargs['columns'] = ''

        kwargs['filter'] = { 'isOpen': openonly }
        auth = APIKeyAuth(self.api_key, self.api_secret)
        return self.get_positions(symbol, openonly, auth, **kwargs)

    def get_balance(self, **kwargs):
        wallets = self.get_wallet(**kwargs)
        for wallet in wallets:
            if wallet['transactType'].lower() == 'total':
                return wallet


    def get_orders(self, symbol=None, openonly=True, reverse=True, **kwargs):
        kwargs['symbol'] = symbol
        kwargs['reverse'] = 'true' if reverse else 'false'

        kwargs, filter_str = self.filter_kwargs(kwargs)
        auth = APIKeyAuth(self.api_key, self.api_secret)
        return self.get('/api/v1/order?filter='+filter_str, auth, **kwargs)


    def send_order(self, symbol, qty=None, price=None,
                   stop=None, trailing_stop=None, hidden=False, **kwargs):
        """
        order defaults to:
        'Limit' when price is specified
        'Stop' when stop is specified
        'StopLimit' when price and stop are specified
        """

        kwargs['symbol'] = symbol

        if hidden:
            kwargs['displayQty'] = 0

        if qty is not None:
            kwargs['orderQty'] = qty

        if price is not None:
            kwargs['price'] = price

        if stop is not None:
            kwargs['stop'] = stop

        if trailing_stop is not None:
            kwargs['pegOffsetValue'] = trailing_stop
            kwargs['pegPriceType'] = 'TrailingStopPeg'

        auth = APIKeyAuth(self.api_key, self.api_secret)
        return self.post('/api/v1/order', auth, **kwargs)


    def close_position(self, symbol):
        return self.send_order(symbol, execInst='Close')


    def update_order(self, orderId, qty=None, **kwargs):
        if qty is not None:
            kwargs['orderQty'] = qty

        kwargs['orderID'] = orderId
        auth = APIKeyAuth(self.api_key, self.api_secret)
        return self.put('/api/v1/order', auth, **kwargs)


    def cancel_orders(self, orderId=None, clOrdId=None, text=''):
        kwargs = { 'text':  text }

        if orderId is not None:
            if isinstance(orderId, str):
                orderId = [orderId]
            kwargs['orderID'] = orderId

        auth = APIKeyAuth(self.api_key, self.api_secret)

        if clOrdId is not None:
            if isinstance(clOrdId, str):
                clOrdId = [clOrdId]
            kwargs['clOrdID'] = clOrdId

            return self.delete('/api/v1/order', auth, **kwargs)
        return self.delete('/api/v1/order/all', auth, **kwargs)

    def set_order_ttl(self, timeout=60):
        return self.post('/api/v1/order/cancelAllAfter', timeout=timeout*1000)

