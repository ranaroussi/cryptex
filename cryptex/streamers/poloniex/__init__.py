
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .poloniex import PoloniexBase as base
from .wrapper import PoloniexWrapper as wrapper
from .streamer import PoloniexStreamer as streamer

__version__ = 0.1
__exchange__ = "poloniex"
__method__ = "rest"
