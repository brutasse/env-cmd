# coding: utf-8
from setuptools import setup

with open('README.rst', 'r') as f:
    long_description = f.read()

setup(
    name='env-cmd',
    version='1.0',
    url='https://github.com/brutasse/env-cmd',
    license='BSD',
    author=u'Bruno Renié',
    description=("A simple wrapper for executing virtualenv commands and "
                 "passing them environment variables via a config file."),
    long_description=long_description,
    py_modules=('env_cmd',),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    classifiers=(
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ),
)
