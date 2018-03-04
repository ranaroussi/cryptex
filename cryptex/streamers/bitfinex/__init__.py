#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .bitfinex import BitfinexChannel as channel
from .wrapper import BitfinexWrapper as wrapper
from .streamer import BitfinexStreamer as streamer

__version__ = 0.1
__exchange__ = "bitfinex"
__method__ = "websocket"