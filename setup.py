#!/usr/bin/env python
#-----------------------------------------------------------------------------
# Copyright (c) 2013-2014, Ray Osborn
#-----------------------------------------------------------------------------

from distutils.core import setup
from setuptools import find_packages

setup(name='PyCal',
      version='0.1',
      description='Online Calendar',
      author='Ray Osborn',
      author_email='rayosborn@mac.com',
      url='https://github.com/rayosborn/pycal',
      package_dir = {'': 'src'},
      packages = find_packages('src')
)