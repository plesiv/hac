**************************************
HAC: Helper for Algorithm Competitions
**************************************

HAC is *highly extensible and configurable command-line tool* intended to ease
the boring part of solving algorithm problems:

- preparing directory structure,
- preparing source-code files,
- preparing runner files (scripts used for testing solutions),
- downloading test-cases.


HAC can very easily be extended to work with:

- any programming language usable from the command-line,
- any runner (shell, Makefile, ant) usable from the command-line,
- any site that exposes information about contests/problems in an uniform and
  web-accessible form.


=======
Support
=======

Following sites and runner/language combinations are currently supported. If
this bothers you, please check `Contribute`_ section.


**Sites supported:**

- `Codeforces <http://codeforces.com/>`_


**Runners/languages supported:**

+-----------------+----------------------+---------------------+
|                 |          C++         |        Python       |
+=================+======================+=====================+
| **POSIX shell** | ``sh.9`` / ``cpp.9`` | ``sh.9`` / ``py.9`` |
+-----------------+----------------------+---------------------+

**OS supported:**

- Linux (tested)



============
Installation
============

To install HAC you will need to have `pip`_ installed on your system. Since HAC
messes with the file-system it is strongly advisable to install it in an
environment of the regular user (to mitigate the responsibility that comes with
power ;) ):

.. code-block:: bash

    $ pip install --upgrade --user hac


Install as super-user at *your own* risk:

.. code-block:: bash

    $ # ... switch to super-user
    # pip install --upgrade hac



=====
Usage
=====

Special commands that don't fetch remote data:

.. code-block:: bash

    $ hac -h             # show help
    $ hac --version      # show version
    $ hac --copy-config  # copy configuration


Commands that fetch remote data and processes it (more info in `Examples`_):

.. code-block:: bash

    $ hac [options...] (prep | show) (CONTEST | PROBLEM) [PROBLEM [PROBLEM ...]]


For up-to-date list of command-line arguments and switches check HAC's help
message.


--------
Tutorial
--------

To copy configuration to user's local directory (``~/.config/hac`` by default,
modifiable with ``HAC_CONFIG_DIR`` environment variable) run:

.. code-block:: bash

    $ hac --copy-config


Modify user specific configuration by changing files in ``~/.config/hac``. File
``hacrc`` is main settings file. Total HAC settings are calculated in this
manner:

- defaults are taken from ``hacrc`` from default-configuration directory
  (un-modifiable by user),
- settings are taken from ``~/.config/hac/hacrc`` and those that are present
  there override settings from ``hacrc`` from default-configuration directory,
- settings are taken from command-line arguments and those that are present
  there override settings from ``~/.config/hac/hacrc`` and default ``hacrc``.

Files in ``~/.config/hac`` sub-directories (``lang``, ``runner``, ``site``)
over-shadow files in default-configuration directory with the same name. For
example file ``~/.config/hac/lang/temp.9.cpp`` over-shadows ``temp.9.cpp`` in
default-configuration directory.

Template-part ``~/.config/hac/runner/cpp.exec_compile.9.sh`` over-shadows
``cpp.exec_compile.9.sh`` in default-configuration directory. This
template-part gets interpolated in ``temp.9.sh`` when runner ``sh.9`` is
prepared for any ``cpp`` language template. Modifying
``~/.config/hac/runner/cpp.exec_compile.9.sh`` allows us change compilation
flags or compiler used for C++ source compilation.

It is best to remove *un-modified* files in ``~/.config/hac`` subdirectories to
prevent over-shadowing of updated files in default-configuration directory. To
remove all files in those directories run (**careful, destructive**):

.. code-block:: bash

    $ rm -r ~/.config/hac/*/*


To copy all default-configuration files in a temporary directory (useful when
you want to use any of the default files as a starting point for your custom
file).

.. code-block:: bash

    $ HAC_CONFIG_DIR=~/temp_config hac --copy-config
    $ # ... change some files from ~/temp_config and copy them to ~/.config/hac
    $ rm -r ~/temp_config   # remove temporary directory


When HAC is started, selected language templates are copied to the destination
directories *unchanged* while selected runner templates are *processed*
(interpolated) with corresponding template-parts. For example
``cpp.dbg_run.9.sh`` is interpolated in ``temp.9.sh`` at the point where
``$dbg_run`` label appears alone in the line in ``temp.9.sh`` file.


--------
Examples
--------

**1)** Display verbose information about:

- HAC's configuration,
- available sites, runner and language templates,
- selected site, contest and problems,
- problems' information for Codeforces contest #527.

.. code-block:: bash

    $ hac -v -d0 show http://codeforces.com/527


**2a)** For problems "B" and "C" from Codeforces contest #527 prepare:

- source-file from ``cpp`` *highest priority* template (has lowest X among all
  ``cpp.X`` templates),
- runner from ``sh.9`` template (gets interpolated for ``cpp`` language
  template),
- pre-tests downloaded from Codeforces.

.. code-block:: bash

    $ mkdir ~/CF527
    $ hac -w~/CF527 -d1 -t1 prep http://codeforces.com/527 B C


**2b)** Write solution for problem "B" and test it on pre-tests:

.. code-block:: bash

    $ cd ~/CF527/B
    $ # ... modify B.cpp
    $ ./B.cpp.sh -e  # test solution on pre-tests
    $ ./B.cpp.sh -c  # clean generated outputs


**2c)** Debug solution for problem "B" on 2nd pre-test:

.. code-block:: bash

    $ cd ~/CF527/B
    $ ./B.cpp.sh -d 2



=======
Authors
=======

`Zoran Plesivčak`_ created HAC and `these fine people`_ have contributed.



==========
Contribute
==========

Contributions are more than welcome! Please see `CONTRIBUTING
<https://github.com/plesiv/hac/blob/master/CONTRIBUTING.rst>`_.



==========
Change Log
==========

Please see `CHANGELOG <https://github.com/plesiv/hac/blob/master/CHANGELOG.rst>`_.



=======
Licence
=======

Please see `LICENSE <https://github.com/plesiv/hac/blob/master/LICENSE>`_.


.. _pip: http://www.pip-installer.org/en/latest/index.html
.. _Zoran Plesivčak: http://plesiv.com
.. _these fine people: https://github.com/plesiv/hac/contributors

