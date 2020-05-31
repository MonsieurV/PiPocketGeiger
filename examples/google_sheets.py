#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Log radiation levels to a Google Sheets spreadsheet.

Require the gspread package:
    https://github.com/burnash/gspread

Python 2:
$ pip install gspread
Python 3:
$ pip3 install gspread

You'll also need a Google Signed Credentials to access your Google account, please follow instructions from:
    http://gspread.readthedocs.org/en/latest/oauth2.html
Save the file from the account service json file from the Google Console to gdocs-credentials-file.json

Released under MIT License. See LICENSE file.

By Yoan Tournade <yoan@ytotech.com>
"""
import os
from PiPocketGeiger import RadiationWatch
import datetime
import time
import gspread

# Google Docs account credentials.
gc = gspread.service_account(
    filename=os.path.join(os.path.dirname(__file__), "gdocs-credentials-file.json")
)
GDOCS_SPREADSHEET_NAME = "RadiationWatch_Spreadsheet"
gsheet = gc.open(GDOCS_SPREADSHEET_NAME)
# We use first sheet.
worksheet = gsheet.sheet1

# Set headers.
worksheet.update("A1:E1", [["Timestamp", "Duration", "CPM", "uSv/h", "uSv/h error"]])

# Period for logging readings to Google Dosc, in seconds.
LOGGING_PERIOD = 120

if __name__ == "__main__":
    print(
        "Logging to Google Docs {0} each {1} seconds.".format(
            GDOCS_SPREADSHEET_NAME, LOGGING_PERIOD
        )
    )
    with RadiationWatch(24, 23) as radiationWatch:
        while 1:
            time.sleep(LOGGING_PERIOD)
            try:
                readings = radiationWatch.status()
                print("Uploading... {0}.".format(readings))
                worksheet.append_row(
                    [
                        datetime.datetime.now().strftime("%d/%m/%Y %H:%M:00"),
                        readings["duration"],
                        readings["cpm"],
                        readings["uSvh"],
                        readings["uSvhError"],
                    ]
                )
                print("Ok.")
            except Exception as e:
                print("Error writting to Google Sheet:")
                print(e)
