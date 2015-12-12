#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Log radiation levels to a Google Docs.

Requires the gspread package:
    https://github.com/burnash/gspread
You'll also need a Google Signed Credentials to access your Google account:
    http://gspread.readthedocs.org/en/latest/oauth2.html

Released under MIT License. See LICENSE file.

By Yoan Tournade <yoan@ytotech.com>
"""
from PiPocketGeiger import RadiationWatch
import datetime
import time
import gspread

# Google Docs account email and password.
GDOCS_EMAIL = 'example@gmail.com'
GDOCS_PASSWORD = 'password'
GDOCS_SPREADSHEET_NAME = 'Radiation_Laussou_France'

LOGGING_PERIOD = 120

if __name__ == "__main__":
    print("Logging to Google Docs {0} each {1} seconds".format(
        GDOCS_SPREADSHEET_NAME, LOGGING_PERIOD))
    with RadiationWatch(24, 23) as radiationWatch:
        while 1:
            time.sleep(LOGGING_PERIOD)
            try:
                status = radiationWatch.status()
                print("Uploading... {0}".format(status))
                gspread.login(GDOCS_EMAIL, GDOCS_PASSWORD).open(
                    GDOCS_SPREADSHEET_NAME).sheet1.append_row((
                        datetime.datetime.now().strftime('%d/%m/%Y %H:%M:00'),
                        status[0],
                        status[1],
                        status[2],
                        status[3]))

                print("Ok.")
            except Exception as e:
                print(e)
