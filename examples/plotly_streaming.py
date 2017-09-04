#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Streaming radiation levels on https://plot.ly.

Require the plotly package and your credentials:
    https://plot.ly/python/user-guide/#Step-1

Released under MIT License. See LICENSE file.

By Yoan Tournade <yoan@ytotech.com>
"""
from PiPocketGeiger import RadiationWatch
import time
import datetime
import plotly.plotly as py
from plotly.graph_objs import Scatter, Data, Stream, Figure, Layout

# Plotly credentials.
USERNAME = 'your_plotly_username'
API_KEY = 'your_api_key'
STREAMING_TOKEN = 'a_streaming_token'
PLOT_TITLE = 'Radiation dose (Gamma rays)'

# Period for streaming readings to Plotly, in seconds.
STREAMING_PERIOD = 5

if __name__ == "__main__":
    print("Streaming to Plotly each {0} seconds.".format(STREAMING_PERIOD))
    stream = None
    try:
        radiationWatch = RadiationWatch(24, 23).setup()
        py.sign_in(USERNAME, API_KEY)
        url = py.plot(
            Figure(
                layout=Layout(
                    title=PLOT_TITLE,
                    xaxis=dict(title='Timestamp'),
                    yaxis=dict(title='Dose (uSv/h)')),
                data=Data([
                    Scatter(
                        x=[], y=[],
                        mode='lines',
                        stream=Stream(token=STREAMING_TOKEN))])),
            filename=PLOT_TITLE)
        print("Plotly graph URL: {0}".format(url))
        stream = py.Stream(STREAMING_TOKEN)
        stream.open()
        while 1:
            readings = radiationWatch.status()
            x = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            print("Streaming... {0}.".format([x, readings['uSvh']]))
            stream.write(dict(x=x, y=readings['uSvh']))
            time.sleep(STREAMING_PERIOD)
    except Exception as e:
        print(e)
    finally:
        radiationWatch.close()
        if stream:
            stream.close()
