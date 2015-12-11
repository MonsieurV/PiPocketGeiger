"""
Radiation Watch Pocket Geiger Type 5 library for Raspberry Pi.

Documentation and usage at: https://github.com/MonsieurV/PiPocketGeiger

Released under MIT License. See LICENSE file.

Contributed by:
- Radiation-watch.org <http://www.radiation-watch.org/>
- Yoan Tournade <yoan@ytotech.com>
"""
import RPi.GPIO as GPIO

class RadiationWatch:
    def __init__(self, radiationPin, noisePin):
        self.radiationPin = radiationPin
        self.noisePin = noisePin

    def __enter__(self):
        # Init the GPIO context.
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.radiationPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.noisePin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # Register local callbacks.
        GPIO.add_event_detect(self.radiationPin, GPIO.FALLING,
            callback=self._onRadiation)
        GPIO.add_event_detect(self.noisePin, GPIO.FALLING,
            callback=self._onNoise)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        GPIO.cleanup()

    def _onRadiation(self, channel):
        print("Ray appeared!")

    def _onNoise(self, channel):
        print("Vibration! Stop moving!")

if __name__ == "__main__":
    with RadiationWatch(24, 23) as radiationWatch:
        while 1:
            pass