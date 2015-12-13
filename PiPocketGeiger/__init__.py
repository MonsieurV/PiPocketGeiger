#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Radiation Watch Pocket Geiger Type 5 library for Raspberry Pi.

Documentation and usage at: https://github.com/MonsieurV/PiPocketGeiger

Released under MIT License. See LICENSE file.

Contributed by:
- Radiation-watch.org <http://www.radiation-watch.org/>
- Yoan Tournade <yoan@ytotech.com>
"""
import RPi.GPIO as GPIO
import threading
import math
import time
__all__ = ['RadiationWatch']

# Number of cells of the history array.
HISTORY_LENGTH = 200
# Duration of each history array cell, in seconds.
HISTORY_CELL_DURATION = 6
# Process period for the statistics, in milliseconds.
PROCESS_PERIOD = 160
MAX_CPM_TIME = HISTORY_LENGTH * HISTORY_CELL_DURATION * 1000
# Magic calibration number from the Arduino lib.
K_ALPHA = 53.032

def millis():
    return int(round(time.time() * 1000))

class RadiationWatch:
    def __init__(self, radiationPin, noisePin, numbering=GPIO.BCM):
        """Initialize the Radiation Watch library, specifying the pin numbers
        for the radiation and noise pin.
        You can also specify the pin numbering mode (BCM numbering by default)."""
        GPIO.setmode(numbering)
        self.radiationPin = radiationPin
        self.noisePin = noisePin
        self.mutex = threading.Lock()
        self.radiationCallback = None
        self.noiseCallback = None

    def status(self):
        """Return current readings, as a dictionary with:
            duration -- the duration of the measurements, in seconds;
            cpm -- the radiation count by minute;
            uSvh -- the radiation dose, exprimed in Sievert per house (uSv/h);
            uSvhError -- the incertitude for the radiation dose."""
        minutes = min(self.duration, MAX_CPM_TIME) / 1000 / 60.0
        cpm = self.cpm / minutes if minutes > 0 else 0
        return dict(
            duration=round(self.duration / 1000.0, 2),
            cpm=round(cpm, 2),
            uSvh=round(cpm / K_ALPHA, 3),
            uSvhError=round(math.sqrt(self.cpm) / minutes / K_ALPHA, 3) \
                if minutes > 0 else 0
            )

    def registerRadiationCallback(self, callback):
        """Register a function that will be called on radiation occurrence. """
        self.radiationCallback = callback

    def registerNoiseCallback(self, callback):
        """Register a function that will be called on noise occurrence. """
        self.noiseCallback = callback

    def __enter__(self):
        return self.setup()

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def setup(self):
        # Initialize the statistics variables.
        self.radiationCount = 0
        self.noiseCount = 0
        self.cpm = 0
        self.cpmHistory = [0] * HISTORY_LENGTH
        self.historyIndex = 0
        self.lastTime = millis()
        self.duration = 0
        self.lastShift = None
        # Init the GPIO context.
        GPIO.setup(self.radiationPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.noisePin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # Register local callbacks.
        GPIO.add_event_detect(self.radiationPin, GPIO.FALLING,
            callback=self._onRadiation)
        GPIO.add_event_detect(self.noisePin, GPIO.FALLING,
            callback=self._onNoise)
        # Enable the timer for processing the statistics periodically.
        self._enableTimer()
        return self

    def close(self):
        GPIO.cleanup()
        with self.mutex:
            self.timer.cancel()

    def _onRadiation(self, channel):
        with self.mutex:
            self.radiationCount += 1
        if self.radiationCallback:
            self.radiationCallback()

    def _onNoise(self, channel):
        with self.mutex:
            self.noiseCount += 1
        if self.noiseCallback:
            self.noiseCallback()

    def _enableTimer(self):
        self.timer = threading.Timer(
            PROCESS_PERIOD / 1000.0, self._processStatistics)
        self.timer.start()

    def _processStatistics(self):
        with self.mutex:
            currentTime = millis()
            if self.noiseCount == 0:
                durationSeconds = int(self.duration / 1000)
                if durationSeconds % HISTORY_CELL_DURATION == 0 \
                        and self.lastShift != durationSeconds:
                    # Shift a cell in the history array each HISTORY_CELL_DURATION.
                    self.lastShift = durationSeconds
                    self.historyIndex += 1
                    if self.historyIndex >= HISTORY_LENGTH:
                        self.historyIndex = 0
                    if self.cpm and self.cpmHistory[self.historyIndex] > 0:
                        self.cpm -= self.cpmHistory[self.historyIndex]
                    self.cpmHistory[self.historyIndex] = 0
                self.cpmHistory[self.historyIndex] += self.radiationCount
                self.cpm += self.radiationCount
                self.duration += abs(currentTime - self.lastTime)
            self.lastTime = millis()
            self.radiationCount = 0
            self.noiseCount = 0
            if self.timer:
                self._enableTimer()

if __name__ == "__main__":
    def onRadiation():
        print("Ray appeared!")

    def onNoise():
        print("Vibration! Stop moving!")

    with RadiationWatch(24, 23) as radiationWatch:
        radiationWatch.registerRadiationCallback(onRadiation)
        radiationWatch.registerNoiseCallback(onNoise)
        while 1:
            print(radiationWatch.status())
            time.sleep(5)
