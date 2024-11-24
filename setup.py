import sys
import re
import ast
from setuptools import setup

readme_markdown = None
with open("README.md") as f:
    readme_markdown = f.read()

setup(
    name="PiPocketGeiger",
    version="0.5.0",
    url="https://github.com/MonsieurV/PiPocketGeiger",
    license="MIT",
    author="Yoan Tournade",
    author_email="yoan@ytotech.com",
    description="A library for monitoring radiation with the Radiation Watch "
    "Pocket Geiger.",
    long_description=readme_markdown,
    long_description_content_type="text/markdown",
    packages=["PiPocketGeiger"],
    include_package_data=True,
    zip_safe=True,
    platforms="any",
    install_requires=["rpi-lgpio>=0.6"],
    extras_require={"dev": ["flake8", "pylint"]},
)
