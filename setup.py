#!/usr/local/bin/python3
import os
from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

reqPath = os.path.dirname(os.path.realpath(__file__)) + '/requirements.txt'
print(reqPath)
install_requires = [] # We have everythin in requirements.txt right now
if os.path.isfile(reqPath):
    with open(reqPath) as f:
        install_requires = f.read().splitlines()

setup(
    name = "AirMobiSim",
    version = "0.0.1a1",
    author = "The AirMobiSim Project",
    author_email = "info@cms-labs.org",
    description = ("The open-source unmanned aerial vehicle simulation framework"),
    license = "GPL-2.0-or-later",
    keywords = "UAV simulation",
    url = "http://airmobisim.org/",
    packages=['src', 'subprojects/tests'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 1 - Alpha",
        "License :: GPL-2.0-or-late",
    ],
    install_requires=install_requires,
)
