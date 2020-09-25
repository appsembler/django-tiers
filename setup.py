#!/usr/bin/env python

from setuptools import setup, find_packages

import tiers

setup(
    name='django-tiers',
    version=tiers.__version__,
    description='Django tier management',
    long_description=open('README.md').read(),
    author='Appsembler',
    url='https://github.com/appsembler/django-tiers',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    packages=find_packages(exclude=['tests', 'fake_organizations']),
    install_requires=[
        'django<3',
        'django-model-utils',
        'python-dateutil',
    ],
)
