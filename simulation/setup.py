'''
Copyright (C) 2015 Jeison Pacateque, Santiago Puerto

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
'''

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

# python setup_cython.py build_ext --inplace

import numpy

ext = Extension("laplacian", ["laplacian.pyx"],
    include_dirs = [numpy.get_include()],
    # adding openmp arguments for openmp variant (not required normally)
    extra_compile_args=['-fopenmp'],
    extra_link_args=['-fopenmp']
    )

# note that the compile and link flags with -fopenmp and *only* required for
# the prange variant, they aren't required for the range(...) version and
# could be removed

#this line says to Cython where numpy is
setup(ext_modules=[ext],
      cmdclass = {'build_ext': build_ext})


