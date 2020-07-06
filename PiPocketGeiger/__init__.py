# -*- coding: utf-8 -*-
"""
Radiation Watch Pocket Geiger Type 5 library for Raspberry Pi.

Documentation and usage at: https://github.com/MonsieurV/PiPocketGeiger

Released under MIT License. See LICENSE file.

Contributed by:
- Radiation-watch.org <http://www.radiation-watch.org/>
- Yoan Tournade <yoan@ytotech.com>

Source for wiring and pin readings:
https://cdn.sparkfun.com/assets/learn_tutorials/1/4/3/GeigerCounterType5_connect_with_microcomputer.pdf
"""
import threading
import math
import time
import RPi.GPIO as GPIO

__all__ = ["RadiationWatch"]

# Number of cells of the history array.
HISTORY_LENGTH = 200
# Duration of each history array cell (seconds).
HISTORY_UNIT = 6
# Process period for the statistics (milliseconds).
PROCESS_PERIOD = 160
MAX_CPM_TIME = HISTORY_LENGTH * HISTORY_UNIT * 1000
# Magic calibration number from the Arduino lib.
K_ALPHA = 53.032

# Bounce delay during which we ignore further edges after an edge.
# In ms.
# See https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/
# We disable it, as we have no bouncing issues.
BOUNCE_DELAY = None


def millis():
    """Return current time in milliseconds.
    """
    return int(round(time.time() * 1000))


class RadiationWatch:
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
            uSvh -- the radiation dose, expressed in microSieverts per hour (uSv/h);
            uSvhError -- the incertitude for the radiation dose."""
        minutes = min(self.duration, MAX_CPM_TIME) / 1000 / 60.0
        cpm = self.count / minutes if minutes > 0 else 0
        return dict(
            duration=round(self.duration / 1000.0, 2),
            cpm=round(cpm, 2),
            uSvh=round(cpm / K_ALPHA, 3),
            uSvhError=round(math.sqrt(self.count) / minutes / K_ALPHA, 3)
            if minutes > 0
            else 0,
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
        self.count = 0
        # Initialize count_history[].
        self.count_history = [0] * HISTORY_LENGTH
        self.history_index = 0
        # Init measurement time.
        self.previous_time = millis()
        self.previous_history_time = millis()
        self.duration = 0
        # Init the GPIO context.
        # Raw data of Radiation Pulse: Not-detected -> High, Detected -> Low.
        GPIO.setup(self.radiation_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # Raw data of Noise Pulse: Not-detected -> Low, Detected -> High.
        GPIO.setup(self.noise_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        # Register local callbacks.
        # As the signal from the radiation pin is high by default
        # and low when a ray hit the sensor, we want to listen on the edges falls.
        GPIO.add_event_detect(
            self.radiation_pin,
            GPIO.FALLING,
            callback=self._on_radiation,
            **{"bouncetime": BOUNCE_DELAY} if BOUNCE_DELAY else {},
        )
        # As the signal from the noise pin is low by default and high when noise occurs,
        # we want to listen on the edges rises.
        GPIO.add_event_detect(
            self.noise_pin,
            GPIO.RISING,
            callback=self._on_noise,
            **{"bouncetime": BOUNCE_DELAY} if BOUNCE_DELAY else {},
        )
        # Enable the timer for processing the statistics periodically.
        self._enable_timer()
        return self

    def close(self):
        """Properly close the resources associated with the driver
        (GPIOs and so on)."""
        # Clean up only used channels.
        GPIO.cleanup([self.radiation_pin, self.noise_pin])
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
        self.timer = threading.Timer(PROCESS_PERIOD / 1000.0, self._process_statistics)
        self.timer.start()

    def _process_statistics(self):
        with self.mutex:
            current_time = millis()
            current_radiation_count = self.radiation_count
            current_noise_count = self.noise_count
            self.radiation_count = 0
            self.noise_count = 0
        if current_noise_count == 0:
            # Store count log.
            self.count_history[self.history_index] += current_radiation_count
            # Add number of counts.
            self.count += current_radiation_count
            # Add ellapsed time to history duration.
            self.duration += abs(current_time - self.previous_time)
        # Shift an array for counting log for each HISTORY_UNIT seconds.
        if current_time - self.previous_history_time >= HISTORY_UNIT * 1000:
            self.previous_history_time += HISTORY_UNIT * 1000
            self.history_index = (self.history_index + 1) % HISTORY_LENGTH
            self.count -= self.count_history[self.history_index]
            self.count_history[self.history_index] = 0
        # Save time of current process period.
        self.previous_time = millis()
        # Enable the timer again.
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
