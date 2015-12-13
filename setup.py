"""
==============
PiPocketGeiger
==============

Radiation Watch Pocket Geiger Type 5 library for Raspberry Pi.

Usage
=====
::

    from PiPocketGeiger import RadiationWatch
    import time

    with RadiationWatch(24, 23) as radiationWatch:
        while 1:
            print(radiationWatch.status())
            time.sleep(5)


See GitHub repository for complete documentation.
"""
import re
import ast
from setuptools import setup

setup(
    name='PiPocketGeiger',
    version='0.1a',
    url='https://github.com/MonsieurV/PiPocketGeiger',
    license='MIT',
    author='Yoan Tournade',
    author_email='yoan@ytotech.com',
    description='A library for monitoring radiation with the Radiation Watch '
                'Pocket Geiger.',
    long_description=__doc__,
    packages=['PiPocketGeiger'],
    include_package_data=True,
    zip_safe=True,
    platforms='any',
    install_requires=[
        'RPi.GPIO>=0.5.0a',
    ]
)
