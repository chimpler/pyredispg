#!/usr/bin/env python

import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTestCommand(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name='pyredispg',
    version='0.0.3',
    description='Run Redis in Postgres',
    long_description='Run Redis in Postgres',
    keywords='postgres, python, tests',
    license='Apache License 2.0',
    author='Simulmedia',
    author_email='francois.dangngoc@gmail.com',
    url='http://github.com/chimpler/pyredispg/',
    packages=['pyredispg'],
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    install_requires=[
        'gevent',
	'yoyo-migration',
        'psycopg2==2.6',
        'pyhocon==0.3.35',
    ],
    tests_require=[
        'flake8',
        'pytest'
    ],
    test_suite='tests',
    cmdclass={
        'test': PyTestCommand
    }
)
