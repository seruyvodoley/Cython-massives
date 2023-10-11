"""файл setup"""
from distutils.core import setup
from Cython.Build import cythonize

setup(
    name='dynamic_array_cc',
    ext_modules=cythonize("dynamic_array_c.pyx"),
)

