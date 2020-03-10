#!/usr/bin/env python
import os
import re
from setuptools import setup


def get_version():
    version_file = open(os.path.join(
        os.path.dirname(__file__), 'nameko_ami', '__init__.py')).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='nameko-ami',
    version=get_version(),
    description='Nameko Asterisk Manager (AMI) extension',
    author='Max Lit',
    author_email='max.lit.mbox@gmail.com',
    url='http://github.com/litnimax/nameko-ami',
    py_modules=['nameko_ami'],
    install_requires=[
        "nameko>=2.8.5",
        "pyst2",
    ],
    packages=('nameko_ami',),
    package_dir={'nameko_ami': 'nameko_ami'},
    extras_require={
        'dev': [
            "coverage==4.0.3",
            "flake8==3.3.0",
            "pylint==1.8.2",
            "pytest==2.8.3",
        ]
    },
    zip_safe=True,
    license='GNU LESSER GENERAL PUBLIC LICENSE V3',
    classifiers=[
        "Programming Language :: Python",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
    ]
)
