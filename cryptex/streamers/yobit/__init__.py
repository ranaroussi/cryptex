#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .yobit import YobitBase as base
from .wrapper import YobitWrapper as wrapper
from .streamer import YobitStreamer as streamer

__version__ = 0.1
__exchange__ = "yobit"
__method__ = "rest"
