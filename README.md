# Raspberry Pi Pocket Geiger library

A Raspberry Pi library to interface with the [Radiation Watch Pocket Geiger counter](http://www.radiation-watch.co.uk/) (Type 5).

![](/misc/type5.jpg?raw=true "Radiation Watch Type 5 Pocket Geiger counter")

The library monitors the Pocket Geiger through interrupts - using the RPi.GPIO package -, processes the hourly [Sievert dose](https://en.wikipedia.org/wiki/Sievert) and allows to get back the data using a simple interface. It comes with examples to log data on a file, to a Google Docs Spreadsheet or to Plotly, giving you some ideas of what to do with it.

Learn more about the Pocket Geiger counter on the Radiation Watch [FAQ](http://www.radiation-watch.co.uk/faqs) and on [our blog](https://blog.ytotech.com/2015/12/06/radiation-watch-arduino/). Actually it is not a proper Geiger-Müller counter, but a Photodiode PIN sensor that can nevertheless effectively counts Gamma radiation.

## Getting started

### Install the library

Using pip:

```
pip install PiPocketGeiger
```

https://pypi.python.org/pypi/PiPocketGeiger/

### Wire your Pocket Geiger to your Raspberry Pi board

You can for example wire the radiation and the noise pin on respectively the `GPIO24` and `GPIO23` of your Raspberry Pi.

TODO Schema wiring

The pin used are specified at the creation of the library object:

```
with RadiationWatch(24, 23) as radiationWatch:
  pass # Do something with the lib.
```

[Pocket Geiger Type 5 interface specification](http://www.radiation-watch.co.uk/uploads/5t.pdf).

### Launch the console printer example

TODO

### Log the results on a file

TODO

### Plot in real-time with Python

TODO

Remember the Pocket Geiger can't record correctly in presence of vibration, so keep the whole stationary during the measurements. You can't use it as a mobile unit of measurement. For that purpose you may look at the [bGeigie Nano](http://blog.safecast.org/bgeigie-nano/) from the Safecast project.

-----------------------

Like it? Not so much? [Tell us](mailto:yoan@ytotech.com).

Happy hacking!

### Credits

Created upon the [Radiation Watch sample code](http://radiation-watch.sakuraweb.com/share/ARDUINO.zip).

### Contribute

Feel free to [open a new ticket](https://github.com/MonsieurV/PiPocketGeiger/issues/new) or submit a PR to improve the lib.
