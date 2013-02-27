#!/usr/bin/python
# -*- coding: utf-8 -*
#Author: Bruce Xin bruce.xin@gmail.com
#CreateDate: 2013-02-26 21:05
'''docstring for setup.py
'''

#stand library import


#third party library import

# setup.py
# Usage: ``python setup.py build_ext --inplace``
from distutils.core import setup, Extension
import numpy
setup(name='_tifffile',
    ext_modules=[Extension('_tifffile', ['tifffile.c'],
                           include_dirs=[numpy.get_include()])])
