#!/usr/bin/env python
import os

from distutils.core import setup
from distutils.command.install import INSTALL_SCHEMES

VERSION = '0.1'

setup(name='django-jimmypage',
    version=VERSION,
    description="Generational page cacheing for Django",
    author='Charlie DeTar',
    author_email='cfd@media.mit.edu',
    url='http://github.com/yourcelf/jimmypage',
    packages=['jimmypage'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
)

