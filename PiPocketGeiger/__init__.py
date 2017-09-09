# -*- coding: utf-8 -*-
"""
Radiation Watch Pocket Geiger Type 5 library for Raspberry Pi.

Documentation and usage at: https://github.com/MonsieurV/PiPocketGeiger

Released under MIT License. See LICENSE file.

Contributed by:
- Radiation-watch.org <http://www.radiation-watch.org/>
- Yoan Tournade <yoan@ytotech.com>
"""
import threading
import math
import time
import RPi.GPIO as GPIO
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
    """Return current time in milliseconds.
    """
    return int(round(time.time() * 1000))


class RadiationWatch(object):
    """Driver object for the Pocket Geiger Type 5 connected on Raspberry Pi GPIOs.

    Usage:
    ```
    with RadiationWatch(24, 23) as radiationWatch:
        # Do something with the lib.
        print(radiationWatch.status())
    ```
    """
    def __init__(self, radiation_pin, noise_pin, numbering=GPIO.BCM):
        """Initialize the Radiation Watch library, specifying the pin numbers
        for the radiation and noise pin.
        You can also specify the pin numbering mode (BCM numbering by
        default)."""
        GPIO.setmode(numbering)
        self.radiation_pin = radiation_pin
        self.noise_pin = noise_pin
        self.mutex = threading.Lock()
        self.radiation_callback = None
        self.noise_callback = None

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
            uSvhError=round(math.sqrt(self.cpm) / minutes / K_ALPHA, 3)
            if minutes > 0 else 0
            )

    def register_radiation_callback(self, callback):
        """Register a function that will be called on radiation occurrence. """
        self.radiation_callback = callback

    def register_noise_callback(self, callback):
        """Register a function that will be called on noise occurrence. """
        self.noise_callback = callback

    def __enter__(self):
        return self.setup()

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def setup(self):
        """Initialize the driver by setting up GPIO interrupts
        and periodic statistics processing. """
        # Initialize the statistics variables.
        self.radiation_count = 0
        self.noise_count = 0
        self.cpm = 0
        self.cpm_history = [0] * HISTORY_LENGTH
        self.history_index = 0
        self.last_time = millis()
        self.duration = 0
        self.last_shift = None
        # Init the GPIO context.
        GPIO.setup(self.radiation_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.noise_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # Register local callbacks.
        GPIO.add_event_detect(
            self.radiation_pin,
            GPIO.FALLING,
            callback=self._on_radiation
        )
        GPIO.add_event_detect(
            self.noise_pin,
            GPIO.FALLING,
            callback=self._on_noise
        )
        # Enable the timer for processing the statistics periodically.
        self._enable_timer()
        return self

    def close(self):
        """Properly close the resources associated with the driver
        (GPIOs and so on)."""
        GPIO.cleanup()
        with self.mutex:
            self.timer.cancel()

    def _on_radiation(self, _channel):
        with self.mutex:
            self.radiation_count += 1
        if self.radiation_callback:
            self.radiation_callback()

    def _on_noise(self, _channel):
        with self.mutex:
            self.noise_count += 1
        if self.noise_callback:
            self.noise_callback()

    def _enable_timer(self):
        self.timer = threading.Timer(
            PROCESS_PERIOD / 1000.0, self._process_statistics)
        self.timer.start()

    def _process_statistics(self):
        with self.mutex:
            current_time = millis()
            if self.noise_count == 0:
                duration_seconds = int(self.duration / 1000)
                if duration_seconds % HISTORY_CELL_DURATION == 0 \
                        and self.last_shift != duration_seconds:
                    # Shift a cell in the history array each
                    # HISTORY_CELL_DURATION.
                    self.last_shift = duration_seconds
                    self.history_index += 1
                    if self.history_index >= HISTORY_LENGTH:
                        self.history_index = 0
                    if self.cpm and self.cpm_history[self.history_index] > 0:
                        self.cpm -= self.cpm_history[self.history_index]
                    self.cpm_history[self.history_index] = 0
                self.cpm_history[self.history_index] += self.radiation_count
                self.cpm += self.radiation_count
                self.duration += abs(current_time - self.last_time)
            self.last_time = millis()
            self.radiation_count = 0
            self.noise_count = 0
            if self.timer:
                self._enable_timer()


if __name__ == "__main__":
    def on_radiation():
        """Test radiation event handler"""
        print("Ray appeared!")

    def on_noise():
        """Test noise event handler"""
        print("Vibration! Stop moving!")

    with RadiationWatch(24, 23) as radiationWatch:
        radiationWatch.register_radiation_callback(on_radiation)
        radiationWatch.register_noise_callback(on_noise)
        while 1:
            print(radiationWatch.status())
            time.sleep(5)
