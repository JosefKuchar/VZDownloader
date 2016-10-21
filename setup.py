#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "vzdownload",
    version = "1.0.0",
    author = "Josef Kuchař",
    author_email = "email@josefkuchar.cz",
    description = "Tool for creating song-book from velkyzpevnik.cz",
    license = "GPLv3",
    keywords = "downloader tool python",
    url = "https://github.com/JosefKuchar/VZDownloader",
    long_description = read("readme.md"),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Utilities",
        "License :: GNUv3 License"
    ],
    install_requires = [
        "colorama",
        "pdfkit",
        "natsort"
    ]
)
