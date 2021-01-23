#!/usr/bin/env  python
# coding=utf-8

from setuptools import setup

setup(
    name='RNAport',
    version='1.0',
    packages=['readProject','utils'],
    url='https://github.com/chenjunhui/RNAport',
    license='GPLv3',
    keywords='RNAport',
    author='chenjunhui',
    author_email='chenjunhui@genomics.cn',
    description='This port only used for preparing RNAref or RNA Denovo pipeline of BGI',
    install_requires=[
        'click==6.7'
    ],

entry_points={'console_scripts':[
    'RNAport=RNAport:RNAPort'
]},
scripts=['RNAport.py'],
python_requires='>=3.0',
classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],

zip_safe=False,
)
