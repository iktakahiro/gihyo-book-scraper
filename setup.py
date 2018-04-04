#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

__author__ = 'Takahiro Ethan Ikeuchi'

requires = ['scrapy']

setup(
    name="gihyo-book-scraper",
    version="1.0.0",
    packages=['gihyo_book_scraper'],
    install_requires=requires,
    description="Web scraping script to get books data from http://gihyo.jp/book/genre",
    long_description=open('README.md').read(),
    author='Takahiro Ethan Ikeuchi',
    author_email='takahiro.ikeuchi@gmail.com',
    url='https://github.com/iktakahiro/gihyo-book-scraper',
    keywords=["scraping", "crawler"],
    license='MIT',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
    ]
)
