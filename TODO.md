# GPIO Python library

Migrate to [gpiozero](https://gpiozero.readthedocs.io/en/latest/installing.html)
https://gpiozero.readthedocs.io/en/stable/migrating_from_rpigpio.html

(Much easier installation?)

# Low-level library

## Create a C library based on wiring PI

The library should be the most "bare" possible: running as a process
to process measurements and allowing to dispatch signals to external
processes for ray events.

http://wiringpi.com/
http://wiringpi.com/download-and-install/
http://wiringpi.com/reference/
http://wiringpi.com/reference/priority-interrupts-and-threads/
https://elinux.org/RPi_Low-level_peripherals

Or also pigpio https://github.com/joan2937/pigpio

We can start from the refined C++ code from the Arduino library
https://github.com/MonsieurV/ArduinoPocketGeiger

Then we could reconstruct the current Python library based on this C lib
(as a wrapper or user).

## Go core

Alternative: code the core library in Go.

https://gist.github.com/simoncos/49463a8b781d63b5fb8a3b666e566bb5

# Add instructions to enable RT capabilities on Raspbian

RT_PREEMPT
https://raspberrypi.stackexchange.com/a/1820/87271
https://emlid.com/raspberry-pi-real-time-kernel/

See also:
https://rt.wiki.kernel.org/index.php/Main_Page
https://wiki.archlinux.org/index.php/Realtime_kernel_patchset
