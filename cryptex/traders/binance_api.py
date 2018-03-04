#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.parse import urlencode
import time
import hashlib
import hmac
import requests


class BinanceAPI(object):
    """
    Simple REST API utility class for Binance
    https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md


    API_KEY = 'rbyZoZVIZ4Z4kgqzqVqykeVWa3rvo0DH9NrXT7nDnIieD5CTlMD96uiCcX82L9sn'
    API_SECRET = '1uG1eIb8UTlgR8vhaN1Mi2BYYdea3Y4UgWRqZmpwfkRWHV6cz1tkzB4NyZLmoZSL'

    from binance_api import BinanceAPI

    binance = BinanceAPI(API_KEY, API_SECRET)
    binance.get('/v3/openOrders', symbol='BNBBTC')
    """

    # --- private methods ---
    def __init__(self, api_key, api_secret):
        self.base_url = 'https://api.binance.com/api'
        self.__api_key = api_key
        self.__api_secret = api_secret
        self.__methods = {
            'GET': requests.get,
            'POST': requests.post,
            'DELETE': requests.delete,
            'PUT': requests.put
        }

        # sync server time
        server_time = self.get('/v1/time')['serverTime']
        self.timestamp_diff = server_time - int(time.time() * 1000)

    def __api_call(self, method, endpoint, data=None, ttl=5000, auth=False):
        # "fix" endpoint
        endpoint = endpoint.replace('/api/', '/')

        # prepare data
        data = data if isinstance(data, dict) else {}

        querystring = urlencode(data)

        if auth:
            # append signature to data
            data['recvWindow'] = ttl
            data['timestamp'] = int(time.time() * 1000) + self.timestamp_diff
            data['signature'] = hmac.new(self.__api_secret.encode('utf-8'),
                                         urlencode(data).encode('utf-8'),
                                         hashlib.sha256).hexdigest()

        # get requests MUST use querystring
        if method == 'GET':
            querystring = urlencode(data)
            if querystring != '':
                endpoint += '?' + querystring

        # make the call
        return self.__methods[method](self.base_url + endpoint,
                                      headers={'X-MBX-APIKEY': self.__api_key},
                                      data=data).json()

    # --- public methods ---
    def get(self, endpoint, ttl=5000, auth=None, **kwargs):
        """ Initiate a GET api call """
        if auth is None:
            auth = ("v1/" not in endpoint)
        return self.__api_call('GET', endpoint, kwargs, ttl, auth)

    def post(self, endpoint, ttl=5000, **kwargs):
        """ Initiate a POST api call """
        return self.__api_call('POST', endpoint, kwargs, ttl, True)

    def delete(self, endpoint, ttl=5000, **kwargs):
        """ Initiate a DELETE api call """
        return self.__api_call('DELETE', endpoint, kwargs, ttl, True)

    def put(self, endpoint, ttl=5000, **kwargs):
        """ Initiate a PUT api call """
        return self.__api_call('PUT', endpoint, kwargs, ttl, True)
