#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distribute_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

from d2to1_testpackage.version import D2TO1_VERSION

setup(
    setup_requires=['d2to1>=%s' % D2TO1_VERSION],
    d2to1=True,
)
