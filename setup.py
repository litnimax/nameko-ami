#!/usr/bin/env python
from setuptools import setup

setup(
    name='nameko-ami',
    version='1.0',
    description='Nameko Asterisk Manager (AMI) extension',
    author='Max Lit',
    author_email='max.lit.mbox@gmail.com',
    url='http://github.com/litnimax/nameko-ami',
    py_modules=['nameko_ami'],
    install_requires=[
        "nameko>=2.5.1",
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
    zip_safe=False,
    license='Apache License, Version 2.0',
    classifiers=[
        "Programming Language :: Python",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 2.7",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
    ]
)
