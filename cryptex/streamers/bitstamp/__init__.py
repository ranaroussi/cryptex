#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .bitstamp import BitstampChannel as channel
from .wrapper import BitstampWrapper as wrapper
from .streamer import BitstampStreamer as streamer

__version__ = 0.1
__exchange__ = "bitstamp"
__method__ = "websocket"
