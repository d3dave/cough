#!/usr/bin/env python3
import os
from setuptools import setup

root = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(root, 'README.md')) as readme_file:
    long_description = readme_file.read()

setup(
    name='cough',
    version='0.2.1',
    description='Write COFF object files',
    long_description=long_description,
    author='David D. Dorfman',
    author_email='d3dave@users.noreply.github.com',
    url='https://github.com/d3dave/cough',
    packages=['cough'],
    license='MIT',
    keywords='coff pe obj build development',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Operating System :: Microsoft :: Windows'
    ],
)
