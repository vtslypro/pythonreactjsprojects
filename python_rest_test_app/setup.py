#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from setuptools import setup, find_packages

try:
    with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
        README = f.read()
except IOError:
    README = "Error loading README file"

with open(os.path.join(os.path.dirname(__file__), 'requirements/internal_requirements.txt')) as req_file_internal:
    required = req_file_internal.read().splitlines()

with open(os.path.join(os.path.dirname(__file__), 'requirements/global_requirements.txt')) as req_file_global:
    required += req_file_global.read().splitlines()

with open(os.path.join(os.path.dirname(__file__), 'rest_test/._version')) as version_file:
    VERSION = version_file.read()

setup(
    name='rest_test_app',
    version=VERSION,
    description="""System rest tests for autocad360 Main server""",
    long_description=README,
    author='Alon itzhaki',
    author_email='alon.itzhaki@autodesk.com',
    url='https://git.autodesk.com/AutoCAD360/python_rest_test_app',
    packages=find_packages(),
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['fixtures/*', '._version', '*.txt', '*.xml', '*.special', '*.json', '*.dwg', '*.zip', '*.bmp', '*.pdf',
             '*.shx', '*.ttf', '*.jpg', '*.gif', '*.png', '*.tif'],
    },
    install_requires=required,
    zip_safe=False,
    keywords='rest_test',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        # 'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
)
