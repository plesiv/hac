import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
from codecs import open

import hac


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        # TODO: remove hac/config/{lang,runner} directories from test
        self.test_args = [
            '--doctest-modules', '--verbose',
            './hac',
        ]
        self.test_suite = True

    def run_tests(self):
        import pytest
        sys.exit(pytest.main(self.test_args))


def long_description():
    with open('README.rst', encoding='utf-8') as f:
        return f.read()

entry_points = {
    'console_scripts': [
        # When installed this way, not going through "__main__.py"
        'hac = hac.core:main',
    ],
}

setup(
    name='hac',
    version=hac.__version__,
    description=hac.__doc__.strip(),
    long_description=long_description(),
    url='https://github.com/plesiv/hac/blob/master/README.rst',
    download_url='https://github.com/plesiv/hac',
    author=hac.__author__,
    author_email='z@plesiv.com',
    license='hac.__license__',

    packages=find_packages(exclude=['tests*']),
    package_data={'hac': ['config/hacrc',
                          'config/lang/*',
                          'config/runner/*',
                          'config/site/*.py']},
    entry_points=entry_points,
    extras_require={},
    install_requires=[
        'requests>=2.3.0',
        'lxml>=3.3.5'
    ],
    tests_require=['pytest'],
    cmdclass = {'test': PyTest},

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Intended Audience :: Education',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Topic :: Education',
    ],
    keywords='algorithm competitions',
)
