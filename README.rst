**************************************
HAC: Helper for Algorithm Competitions
**************************************
|license| |pypi_version| |pypi_downloads| |python_versions| |linux_build| |code_quality|


**hac** is *extensible* and *configurable* command-line tool for algorithm
competitions. It:

- prepares directory structures and source files,
- prepares runner files (scripts used to test solutions),
- downloads test-cases.


=======
Install
=======

Recommended to install as non-root:

.. code-block:: bash

    $ pip install --upgrade --user hac


=====
Usage
=====

---------
Example 1
---------

**A)** For problems "A", "B" and "C" from `Codeforces contest #527
<http://codeforces.com/contest/527>`_ prepare:

- source file from *cpp* highest priority template (has lowest *X* among
  *cpp.X* language templates),
- runner from *sh.5* template (interpolated for *cpp* language template),
- test-cases downloaded from `Codeforces <http://codeforces.com/>`_.

.. code-block:: bash

    $ hac -lcpp -rsh.5 codeforces/527 a b c


With default configuration all of the next lines do same as the one above:

.. code-block:: bash

    $ hac -lcpp.5 -rsh.5 prep http://codeforces.com/527/A B C
    $ hac prep codeforces.com/527 B 1 c
    $ hac -d2 CODEFORCES/527 1 2 3
    $ hac forc/527 a b c


**B)** Write solution for problem "B" and test it on test-cases:

.. code-block:: bash

    $ cd 527/B
    $ # ... modify B.cpp
    $ ./B.cpp.sh -e  # test solution on test-cases
    $ ./B.cpp.sh -c  # clean generated outputs


**C)** Debug solution for problem "B" on 2nd test-case:

.. code-block:: bash

    $ ./B.cpp.sh -d 2


---------
Example 2
---------

Display general information about **hac**:

.. code-block:: bash

    $ hac --help
    $ hac --version

Display information about **hac** and selected site/problems:

.. code-block:: bash

    $ hac -v show codeforces/527     # verbose
    $ hac -V show codeforces/527     # terse




=======
Support
=======

**Sites:**

+------------------------------------------------+----------------------+----------------------+
| Site \\ Fetching problems from                 |       Contest        |        Archive       |
+================================================+======================+======================+
| `Codeforces.com <http://codeforces.com/>`_     |        **YES**       |       **NO**         |
+------------------------------------------------+----------------------+----------------------+
| `Rosalind <http://rosalind.info/>`_            |                      |       **YES**        |
+------------------------------------------------+----------------------+----------------------+
| `Sphere online judge <http://www.spoj.com/>`_  |                      |       **PARTIAL**    |
+------------------------------------------------+----------------------+----------------------+
| `Codechef <https://www.codechef.com/>`_        |        **NO**        |       **NO**         |
+------------------------------------------------+----------------------+----------------------+


**Runner/language combinations:**

+-----------------+----------------+------------------+-----------------+-------------------+------------------+
|                 |         C      |        C++       |       Python    |       Java        |       Pascal     |
+=================+================+==================+=================+===================+==================+
| **POSIX shell** | *sh.5* / *c.5* | *sh.5* / *cpp.5* | *sh.5* / *py.5* | *sh.5* / *java.5* | *sh.5* / *pas.5* |
+-----------------+----------------+------------------+-----------------+-------------------+------------------+



=============
Configuration
=============

User specific configuration should be placed in ``~/.config/hac`` directory by
default (to change configuration directory you need to set ``HAC_CONFIG_DIR``
environment variable).

In order to configure **hac** according to your preferences:

1. copy default configuration files in a temporary directory,

.. code-block:: bash

    $ HAC_CONFIG_DIR=~/temp_config hac --copy-config

2. customize interesting files in ``~/temp_config``,
3. move *only customized* files to ``~/.config/hac``, e.g.

.. code-block:: bash

    $ mkdir -p ~/.config/hac
    $ cp ~/temp_config/hacrc ~/.config/hacrc

4. remove temporary directory.

.. code-block:: bash

    $ rm -r ~/temp_config

This approach is desirable because only configuration files that differ from
the default ones should be present in configuration directory, thereby
effectively overshadowing the default configuration.



==========
Additional
==========

For more information about **hac** please see `User manual
<https://github.com/plesiv/hac/blob/master/MANUAL.rst>`_

For information about *contributions* please check `Contributing
<https://github.com/plesiv/hac/blob/master/MANUAL.rst#contributing>`_ chapter
from *User manual*.



==========
Change Log
==========

Please see `CHANGELOG <https://github.com/plesiv/hac/blob/master/CHANGELOG.rst>`_.



=======
Licence
=======

Please see `LICENSE <https://github.com/plesiv/hac/blob/master/LICENSE>`_.


.. |license| image:: https://img.shields.io/github/license/plesiv/hac.svg?style=plastic
   :target: https://github.com/plesiv/hac/blob/master/LICENSE
   :alt: License

.. |pypi_version| image:: https://img.shields.io/pypi/v/hac.svg?style=plastic
   :target: https://pypi.python.org/pypi/hac
   :alt: PyPI Version

.. |pypi_downloads| image:: https://img.shields.io/pypi/dm/hac.svg?style=plastic
   :target: https://pypi.python.org/pypi/hac
   :alt: PyPI Monthly downloads

.. |python_versions| image:: https://img.shields.io/pypi/pyversions/hac.svg?style=plastic
   :target: https://pypi.python.org/pypi/hac
   :alt: PyPI Supported Python versions

.. |linux_build| image:: https://img.shields.io/travis/plesiv/hac/master.svg?label=linux%20build&style=plastic
   :target: http://travis-ci.org/plesiv/hac
   :alt: Linux Build status

.. |code_quality| image:: https://img.shields.io/codacy/0e405bf71d584768aabd44b82f6f4e47.svg?style=plastic
   :target: https://www.codacy.com/app/z_2/hac/files
   :alt: Code Quality
