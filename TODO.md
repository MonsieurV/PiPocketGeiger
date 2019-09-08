# Create a C library based on wiring PI

The library should be the most "bare" possible: running as a process
to process measurements and allowing to dispatch signals to external
processes for ray events.

http://wiringpi.com/
http://wiringpi.com/download-and-install/
http://wiringpi.com/reference/
http://wiringpi.com/reference/priority-interrupts-and-threads/
https://elinux.org/RPi_Low-level_peripherals

Or also pigpio https://github.com/joan2937/pigpio

Alternative, see C code from RPi.GPIO http://hg.code.sf.net/p/raspberry-gpio-python/code/file/314568df26f8/source/py_gpio.c

We can start from the refined C++ code from the Arduino library
https://github.com/MonsieurV/ArduinoPocketGeiger

Then we could reconstruct the current Python library based on this C lib
(as a wrapper or user).

# Add instructions to enable RT capabilities on Raspbian


RT_PREEMPT
https://raspberrypi.stackexchange.com/a/1820/87271
https://emlid.com/raspberry-pi-real-time-kernel/

See also:
https://rt.wiki.kernel.org/index.php/Main_Page
https://wiki.archlinux.org/index.php/Realtime_kernel_patchset
