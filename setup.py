# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='ASF_IPC',
    version='1.1.2',
    packages=['ASF_IPC'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'requests',
        'websockets'
    ],
    author='deluxghost',
    author_email='deluxghost@gmail.com',
    description='A simple Python 3.6+ library of ArchiSteamFarm IPC API',
    long_description='Check GitHub page for usages.',
    license='GPL v3',
    url='https://github.com/deluxghost/ASF_IPC/'
)
