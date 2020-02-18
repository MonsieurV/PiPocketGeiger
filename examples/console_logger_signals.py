#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Log radiation hits or noise signals to the console.

Released under MIT License. See LICENSE file.

By Yoan Tournade <y@yoantournade.com>
"""
import time
from PiPocketGeiger import RadiationWatch

def example_run_context():
    example_run_context.hit_flag = False

    def onRadiation():
        example_run_context.hit_flag = True
        print("Ray appeared!")

    def onNoise():
        print("Noisy and moving around here!")

    # Create the RadiationWatch object, specifying the used GPIO pins ...
    with RadiationWatch(24, 23) as radiation_watch:
        print("Waiting for gamma rays to hit the Pocket Geiger.")
        radiation_watch.register_radiation_callback(onRadiation)
        radiation_watch.register_noise_callback(onNoise)
        while 1:
            # ... and print readings after radiation hit.
            if example_run_context.hit_flag:
                print(radiation_watch.status())
                example_run_context.hit_flag = False
            time.sleep(3)

if __name__ == "__main__":
    example_run_context()
