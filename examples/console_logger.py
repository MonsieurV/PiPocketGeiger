#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Log radiation levels to the console.

Released under MIT License. See LICENSE file.

By Yoan Tournade <yoan@ytotech.com>
"""
import time
from PiPocketGeiger import RadiationWatch

if __name__ == "__main__":
    # Create the RadiationWatch object, specifying the used GPIO pins ...
    with RadiationWatch(24, 23) as radiationWatch:
        while 1:
            # ... and simply print readings each 5 seconds.
            print(radiationWatch.status())
            time.sleep(5)
            # That's all.
