#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .exmo import ExmoBase as base
from .wrapper import ExmoWrapper as wrapper
from .streamer import ExmoStreamer as streamer

__version__ = 0.1
__exchange__ = "exmo"
__method__ = "rest"
