# -*- coding: utf-8 -*-
import codecs
import os
import re

from setuptools import setup


def read(*parts):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


setup(
    name='ASF_IPC',
    version=find_version('ASF', '__init__.py'),
    packages=['ASF'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.6, <4',
    install_requires=[
        'aiohttp',
        'cchardet',
    ],
    author='deluxghost',
    author_email='deluxghost@gmail.com',
    description='A simple Python 3.6+ library of ArchiSteamFarm IPC API',
    long_description='Check GitHub page for usage.',
    license='GPL v3',
    url='https://github.com/deluxghost/ASF_IPC/'
)
