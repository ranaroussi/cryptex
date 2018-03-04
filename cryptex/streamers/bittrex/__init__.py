#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .bittrex import BittrexBase as base
from .wrapper import BittrexWrapper as wrapper
from .streamer import BittrexStreamer as streamer

__version__ = 0.1
__exchange__ = "bittrex"
__method__ = "rest"
