#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Broadcast radiation levels to Twitter.

Require the twython packages:
    https://github.com/ryanmcgrath/twython
You'll also need a Twitter application credentials:
    https://apps.twitter.com

Released under MIT License. See LICENSE file.

By Yoan Tournade <yoan@ytotech.com>
"""
from PiPocketGeiger import RadiationWatch
import time
from twython import Twython

# Twitter application credentials.
APP_KEY = 'your_app_key'
APP_SECRET = 'your_app_secret'
OAUTH_TOKEN = 'your_app_oauth_token'
OAUTH_TOKEN_SECRET = 'your_app_oauth_token_secret'

# Your place name or exact location. Keep it short or it won't fit the tweet!
MY_PLACE = "(37 Rue de Rennes, Paris, France)"

# Period for twitting, in seconds.
TWITTING_PERIOD = 120

if __name__ == "__main__":
    print("Twitting each {0} seconds.".format(TWITTING_PERIOD))
    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    with RadiationWatch(24, 23) as radiationWatch:
        while 1:
            time.sleep(TWITTING_PERIOD)
            try:
                readings = radiationWatch.status()
                print("Twitting... {0}.".format(readings))
                twitter.update_status(
                    status='Radiation in my house {0}: '
                    '{1} uSv/h +/- {2} -- {3} CPM @radiation_watch'.format(
                        MY_PLACE, readings['uSvh'], readings['uSvhError'],
                        readings['cpm']))
                print("Ok.")
            except Exception as e:
                print(e)
