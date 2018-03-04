#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .kraken import KrakenBase as base
from .wrapper import KrakenWrapper as wrapper
from .streamer import KrakenStreamer as streamer

__version__ = 0.1
__exchange__ = "kraken"
__method__ = "rest"
