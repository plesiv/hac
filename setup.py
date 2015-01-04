from setuptools import setup, find_packages
from codecs import open

import hac


def long_description():
    with open('README.md', encoding='utf-8') as f:
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
    url='https://github.com/plesiv/hac/blob/master/README.md',
    download_url='https://github.com/plesiv/hac',
    author=hac.__author__,
    author_email='zplesiv@gmail.com',
    license='hac.__license__',

    packages=find_packages(exclude=['tests*']),
    entry_points=entry_points,
    extras_require={},
    install_requires=[],
    tests_require=[],
    cmdclass={},

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Intended Audience :: Education',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Topic :: Education',
    ],
    keywords='algorithm competitions',
    include_package_data=True,
)
