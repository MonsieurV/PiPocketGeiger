#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Log radiation levels to a CSV file.

Released under MIT License. See LICENSE file.

By Yoan Tournade <yoan@ytotech.com>
"""
from PiPocketGeiger import RadiationWatch
import datetime
import time
import csv

FILENAME = "radiation.csv"
LOGGING_PERIOD = 30

if __name__ == "__main__":
    try:
        radiationWatch = RadiationWatch(24, 23)
        radiationWatch.setup()
        print("Logging to the file {0} each {1} seconds.".format(
            FILENAME, LOGGING_PERIOD))
        with open(FILENAME, 'w') as myfile:
            writer = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            writer.writerow(
                ['date', 'duration', 'CPM', 'uSv/h', 'uSv/h error'])
            while 1:
                readings = radiationWatch.status()
                print("Logging... {0}.".format(readings))
                writer.writerow([
                    datetime.datetime.now().strftime('%d/%m/%Y %H:%M:00'),
                    readings['duration'],
                    readings['cpm'],
                    readings['uSvh'],
                    readings['uSvhError']])
                time.sleep(LOGGING_PERIOD)
                myfile.flush()
    finally:
        radiationWatch.close()
