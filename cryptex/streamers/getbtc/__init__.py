#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .getbtc import GetbtcBase as base
from .wrapper import GetbtcWrapper as wrapper
from .streamer import GetbtcStreamer as streamer

__version__ = 0.1
__exchange__ = "getbtc"
__method__ = "rest"
