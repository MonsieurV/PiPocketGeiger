"""
PiPocketGeiger
-----
Radiation Watch Pocket Geiger Type 5 library for Raspberry Pi.

Links
`````
* `code and documentation <https://github.com/MonsieurV/PiPocketGeiger>`_
"""
import re
import ast
from setuptools import setup

setup(
    name='PiPocketGeiger',
    version=0.1,
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
