import sys
from setuptools import setup, find_packages

if sys.version_info.major == 2:
    raise Exception("Python version 3 is required.")

setup(name='Tiling',
    version='1.0.0',
    description='A package for tilings.',
    author='Ville Makinen',
    author_email='ville.p.makinen@nls.fi',
    license='GPLV3',
    packages=find_packages(),
    zip_safe=False,
    test_suite='tests',
    install_requires=('numpy'))
