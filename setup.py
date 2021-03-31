# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in sail_bpm/__init__.py
from sail_bpm import __version__ as version

setup(
	name='sail_bpm',
	version=version,
	description='sailbpm',
	author='sailbpm',
	author_email='sailbpm@gmail.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
