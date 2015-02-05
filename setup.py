#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import switch
version = switch.__version__

setup(
    name='switch',
    version=version,
    author='',
    author_email='acquayefrank@gmail.com',
    packages=[
        'switch',
    ],
    include_package_data=True,
    install_requires=[
        'Django>=1.7.1',
    ],
    zip_safe=False,
    scripts=['switch/manage.py'],
)