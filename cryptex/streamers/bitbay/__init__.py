#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .bitbay import BitbayBase as base
from .wrapper import BitbayWrapper as wrapper
from .streamer import BitbayStreamer as streamer

__version__ = 0.1
__exchange__ = "bitbay"
__method__ = "rest"
