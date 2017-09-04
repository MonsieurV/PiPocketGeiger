#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Log radiation levels to a Google Docs.

Require the gspread and oauth2client packages:
    https://github.com/burnash/gspread
    https://github.com/google/oauth2client
You'll also need a Google Signed Credentials to access your Google account:
    http://gspread.readthedocs.org/en/latest/oauth2.html

Released under MIT License. See LICENSE file.

By Yoan Tournade <yoan@ytotech.com>
"""
from PiPocketGeiger import RadiationWatch
import datetime
import time
import gspread
import json
from oauth2client.client import SignedJwtAssertionCredentials

# Google Docs account credentials.
keys = json.load(open('gdocs-credentials-file.json'))
scope = ['https://spreadsheets.google.com/feeds']
credentials = SignedJwtAssertionCredentials(
    keys['client_email'],
    keys['private_key'].encode(),
    scope
)
GDOCS_SPREADSHEET_NAME = 'Radiation_Spreadsheet'

# Period for logging readings to Google Dosc, in seconds.
LOGGING_PERIOD = 120

if __name__ == "__main__":
    print("Logging to Google Docs {0} each {1} seconds.".format(
        GDOCS_SPREADSHEET_NAME, LOGGING_PERIOD))
    with RadiationWatch(24, 23) as radiationWatch:
        while 1:
            time.sleep(LOGGING_PERIOD)
            try:
                readings = radiationWatch.status()
                print("Uploading... {0}.".format(readings))
                gspread.authorize(credentials).open(
                    GDOCS_SPREADSHEET_NAME).sheet1.append_row(
                        datetime.datetime.now().strftime('%d/%m/%Y %H:%M:00'),
                        readings['duration'],
                        readings['cpm'],
                        readings['uSvh'],
                        readings['uSvhError'])
                print("Ok.")
            except Exception as e:
                print(e)
