__author__ = 'ziyasal'

from setuptools import setup

setup(
    name='pyley',
    version='0.2.0',
    author='Ziya SARIKAYA',
    author_email='sarikayaziya@gmail.com',
    packages=['pyley'],
    url='https://github.com/ziyasal/pyley',
    license='LICENSE',
    description='Python client for an open-source graph database Cayley',
    install_requires=['requests'],
    include_package_data=True
)
