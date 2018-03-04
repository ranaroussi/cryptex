#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .itbit import ItbitBase as base
from .wrapper import ItbitWrapper as wrapper
from .streamer import ItbitStreamer as streamer

__version__ = 0.1
__exchange__ = "itbit"
__method__ = "rest"
