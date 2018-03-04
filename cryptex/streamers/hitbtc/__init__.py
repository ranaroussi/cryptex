#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .hitbtc import HitbtcChannel as channel
from .wrapper import HitbtcWrapper as wrapper
from .streamer import HitbtcStreamer as streamer

__version__ = 0.1
__exchange__ = "hitbtc"
__method__ = "websocket"
