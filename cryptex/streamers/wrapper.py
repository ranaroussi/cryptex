#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from abc import ABCMeta


class Wrapper():

    __metaclass__ = ABCMeta

    name = "abstract"

    def wsCallback(self, data, raw_data, **kwargs):
        """ this method will be overridden from outside """
        pass

    def streamCallback(self, data, **kwargs):
        """ this method will be overridden from outside """
        pass

    def dataCallback(self, data, **kwargs):
        """ this method will be overridden from outside """
        pass

    def tradesCallback(self, params, raw_data):
        pass

    def orderbookCallback(self, params, raw_data):
        pass

    @staticmethod
    def getPair(base, quote, case="lower", sep=""):
        if case == "lower":
            return base.lower() + sep + quote.lower()
        return base.upper() + sep + quote.upper()

    def getBaseData(self, base, quote, format):
        return {"format": format,
                "exchange": self.name,
                "pair": self.getPair(base, quote),
                "base": base.lower(),
                "quote": quote.lower(),
                "timestamp": int(time.time()),
                "data": {
                    "base": 0.0,
                    "quote": 0.0,
                }}
