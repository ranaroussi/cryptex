#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .cex import CexChannel as channel
from .wrapper import CexWrapper as wrapper
from .streamer import CexStreamer as streamer

__version__ = 0.1
__exchange__ = "cex"
__method__ = "websocket"
