#!/usr/bin/env python
from setuptools import setup
import adl

setup(
    name='py-adl',
    version=adl.VERSION,
    description='Adl wrapper script written in python.',
    url='https://github.com/cronyakatsuki/py-adl',
    author='Crony Akatsuki',
    author_email='cronyakatsuki@gmail.com',
    license='GPL-3.0',
    py_modules=['adl'],
    entry_points={
        'console_scripts': [
            'adl=adl:main',
        ],
    },
    keywords=['trackma', 'animld', 'anime', 'adl', 'linux', 'windows'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: GPL-3.0 License',
        'Programming Language :: Python :: 3',
        'Operating System :: POSIX :: Linux :: Windows'
    ],
)
