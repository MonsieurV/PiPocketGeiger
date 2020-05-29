# Introduction

I currently own a Raspberry pi 4 with a [TV Hat](https://www.raspberrypi.org/blog/raspberry-pi-tv-hat/) I use to broadcast an IPTV on my local network. I would love to use the same Raspberry for my radiation detection.

After some research, I found the following pins are used by the TV Hat ([source](https://www.raspberrypi.org/forums/viewtopic.php?t=235171#p1483088)):
 - 5V - pin#2, pin#4
 - 3V3 - pin#1, pin#17 (not connected)
 - GND - pin#6, pin#9, pin#14, pin#20, pin#25, pin#30, pin#34 pin,#39
 - SPI MOSI - pin#19
 - SPI MISO - pin#21
 - SPI SCLK - pin#23
 - SPI SC0 - pin#24
 - ID_SD - pin#27
 - ID_SC - pin#28
 
The [Pocket Geiger](http://www.radiation-watch.co.uk/index.php) needs:
 - An alimentation pin
 - A ground pin
 - Two GPIOs pins
 
To make sure I can wire both at the same time, let's look at the pinout of my Raspberry Pi.

```sh
sudo apt-get install python3-pip
sudo pip3 install gpiozero
pinout
```

This gives me the following:
```
,--------------------------------.
| oooooooooooooooooooo J8   +======
| 1ooooooooooooooooooo  PoE |   Net
|  Wi                    oo +======
|  Fi  Pi Model 4B  V1.1 oo      |
|        ,----.               +====
| |D|    |SoC |               |USB3
| |S|    |    |               +====
| |I|    `----'                  |
|                   |C|       +====
|                   |S|       |USB2
| pwr   |HD|   |HD| |I||A|    +====
`-| |---|MI|---|MI|----|V|-------'
Revision           : c03111
SoC                : BCM2711
RAM                : 4096Mb
Storage            : MicroSD
USB ports          : 4 (excluding power)
Ethernet ports     : 1
Wi-fi              : True
Bluetooth          : True
Camera ports (CSI) : 1
Display ports (DSI): 1
J8:
   3V3  (1) (2)  5V
 GPIO2  (3) (4)  5V
 GPIO3  (5) (6)  GND
 GPIO4  (7) (8)  GPIO14
   GND  (9) (10) GPIO15
GPIO17 (11) (12) GPIO18
GPIO27 (13) (14) GND
GPIO22 (15) (16) GPIO23
   3V3 (17) (18) GPIO24
GPIO10 (19) (20) GND
 GPIO9 (21) (22) GPIO25
GPIO11 (23) (24) GPIO8
   GND (25) (26) GPIO7
 GPIO0 (27) (28) GPIO1
 GPIO5 (29) (30) GND
 GPIO6 (31) (32) GPIO12
GPIO13 (33) (34) GND
GPIO19 (35) (36) GPIO16
GPIO26 (37) (38) GPIO20
   GND (39) (40) GPIO21
```

So I should be able to use pins 17, 20, 37 and 38 for my Pocket Geiger.

Let's prepare it!

# Preparation

## Soldering

First of all, I soldered a 5 pin female header on the Pocket Geiger so that I can use jumper cables to connect it to the Raspberry.

## Box

The Pocket Geiger comes with a nice box which didn't fit because of my female header so I cutted a small hole with a hobby knife.

*Note:* You can put the two brass plates on each side of the Pocket Geiger to ignore Beta waves.

## Connection

I then connected:
- +V to pin 17
- GND to nothing
- SIG to pin 37 (GPIO26)
- GND to pin 20
- NS to pin 38 (GPIO20)

# Install

```sh
sudo apt-get install python3-rpi.gpio
sudo pip3 install PiPocketGeiger
```

![](/buildlogs/gregoire-rpi4/img02.jpg?raw=true "Soldering of Pocket Geiger Type 5 pins")

------------------

By Grégoire, May 2020.
