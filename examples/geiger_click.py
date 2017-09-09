#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Play a typical Geiger counter sound on radiation, using callbacks.

Use the aplay command. You'll need a speaker connected to your Raspberry Pi:
    http://www.raspberrypi-spy.co.uk/2013/06/raspberry-pi-command-line-audio/

Released under MIT License. See LICENSE file.

By Yoan Tournade <yoan@ytotech.com>
"""
from PiPocketGeiger import RadiationWatch
import subprocess
import time

if __name__ == "__main__":
    def onRadiation():
        print("Ray appeared!")
        # Play a classic geiger click sound.
        subprocess.Popen(['aplay', 'click.wav'])

    with RadiationWatch(24, 23) as radiationWatch:
        print("Waiting for gamma rays to hit the Pocket Geiger.")
        radiationWatch.register_radiation_callback(onRadiation)
        while 1:
            # Do not keep the CPU busy for nothing: sleep.
            time.sleep(30)
