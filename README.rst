**************************************
HAC: Helper for Algorithm Competitions
**************************************

**hac** is *highly extensible and configurable command-line tool* intended to
ease the boring part of solving algorithm problems:

- preparing directory structure,
- preparing source-code files,
- preparing runner files (scripts used for testing solutions),
- downloading test-cases.


**hac** can be extended very easily to work with:

- any programming language usable from the command-line,
- any runner usable from the command-line (examples: *shell scripts*,
  *Makefiles*, *ant scripts*),
- any site that exposes information about contests/problems in an uniform and
  web-accessible form (examples: `Codeforces <http://codeforces.com/>`_,
  `Codechef <http://www.codechef.com/>`_).


=======
Support
=======

If lack of support for particular programming language or site irks you, please
check `Contribute`_ section. This section contains current up-to-date support
info.


**Sites supported:**

- `Codeforces <http://codeforces.com/>`_


**Runner/language combinations supported:**

+-----------------+----------------------+
|                 |     POSIX shell      |
+=================+======================+
|     **C++**     |  *sh.9*  /  *cpp.9*  |
+-----------------+----------------------+
|   **Python**    |  *sh.9*  /  *py.9*   |
+-----------------+----------------------+


**OS supported:**

- Linux (tested)


**Python versions**

- 2.7
- 3.3
- 3.4



============
Installation
============

To install **hac** you need to have `pip`_ installed on your system. Since
**hac** messes with the file-system it is strongly advisable to install it as
regular user (to mitigate the responsibility that comes with power ;) ):

.. code-block:: bash

    $ pip install --upgrade --user hac


Install as super-user at *your own* risk:

.. code-block:: bash

    user$ # ... switch to super-user
    root$ pip install --upgrade hac



=====
Usage
=====

Special commands that don't fetch remote data:

.. code-block:: bash

    $ hac --help         # show help
    $ hac --version      # show version
    $ hac --copy-config  # copy configuration (to ~/.config/hac by default)


Commands that fetch remote data and process it (more info in `Examples`_):

.. code-block:: bash

    $ hac [options...] (prep | show) (CONTEST | PROBLEM) [PROBLEM [PROBLEM ...]]


For up-to-date list of command-line arguments and switches check **hac**'s help
message.


--------
Examples
--------

**1)** Display verbose information about:

- **hac**'s configuration,
- available sites, runner and language templates,
- selected site, contest and problems,
- problems' information for Codeforces contest #527.

.. code-block:: bash

    $ hac -v show http://codeforces.com/527


**2a)** For problems "B" and "C" from Codeforces contest #527 prepare:

- source-file from *cpp* *highest priority* template (has lowest *X* among
  all *cpp.X* templates),
- runner from *sh.9* template (gets interpolated for *cpp* language template),
- pre-tests downloaded from `Codeforces <http://codeforces.com/>`_.

.. code-block:: bash

    $ mkdir ~/contests && cd ~/contests
    $ hac -d2 -lcpp -rsh.9 prep http://codeforces.com/527 B C


With default configuration *any* of the following lines is equivalent to the
one above:

.. code-block:: bash

    $ hac -lcpp.9 -rsh.9 prep http://codeforces.com/527 b c
    $ hac http://codeforces.com/527 B C
    $ hac cf/527 2 3


**2b)** Write solution for problem "B" and test it on pre-tests:

.. code-block:: bash

    $ cd 527/B
    $ # ... modify B.cpp
    $ ./B.cpp.sh -e  # test solution on pre-tests
    $ ./B.cpp.sh -c  # clean generated outputs


**2c)** Debug solution for problem "B" on 2nd pre-test:

.. code-block:: bash

    $ ./B.cpp.sh -d 2


--------
Tutorial
--------

To copy configuration to user's local directory (``~/.config/hac`` by default,
modifiable with ``HAC_CONFIG_DIR`` environment variable) run:

.. code-block:: bash

    $ hac --copy-config


Modify user specific configuration by changing files in ``~/.config/hac``. File
``hacrc`` is main settings file. Total **hac** settings are calculated in a
*cascaded* manner (similar in concept to how CSS works) by:

- taking settings from ``hacrc`` from default-configuration directory (not
  writable by user),
- overriding above settings with those from ``~/.config/hac/hacrc``,
- overriding above settings with those from command-line arguments.

Files in ``~/.config/hac`` sub-directories (``lang``, ``runner``, ``site``)
over-shadow files in default-configuration directory with the same name. For
example file ``~/.config/hac/lang/temp.9.cpp`` over-shadows ``temp.9.cpp`` in
default-configuration directory.

Template-part ``~/.config/hac/runner/cpp.exec_compile.9.sh`` over-shadows
``cpp.exec_compile.9.sh`` in default-configuration directory. This
template-part gets interpolated in ``temp.9.sh`` when runner *sh.9* is
prepared for any *cpp* language template. Modifying
``~/.config/hac/runner/cpp.exec_compile.9.sh`` allows us change compilation
flags or compiler used for C++ source compilation.

It is best to remove *un-customized* files in
``~/.config/hac/{lang,runner,site}`` subdirectories to prevent possible
over-shadowing of updated files in default-configuration directory (when
**hac** gets updated). To remove all files in those directories run (**careful,
destructive**):

.. code-block:: bash

    $ rm -r ~/.config/hac/*/*


If you want to use any of the default configuration/template files as a
starting point for your customized files, you can:

- copy all default-configuration files in a temporary directory,
- modify and move to ``~/.config/hac`` files of interest and throw away others.

.. code-block:: bash

    $ HAC_CONFIG_DIR=~/temp_config hac --copy-config
    $ # ... modify interesting files in ~/temp_config and move them to
    $ # ... ~/.config/hac
    $ rm -r ~/temp_config   # remove temporary directory


When **hac** is run to prepare the environment (``prep`` command):

- selected language templates are copied for each task to the destination
  directories *unchanged*,
- selected runner templates are *processed (interpolated)* with corresponding
  template-parts. For example if *cpp* and *sh.9* are selected, contents of
  ``cpp.dbg_run.9.sh`` are interpolated in ``temp.9.sh`` (appropriately
  indented) at the point of where label ``$dbg_run`` occurs alone in the line
  in ``temp.9.sh`` file.


Priority labels of runner templates and runner-parts are *completely separate*
from the priority labels of language templates. This means that

- ``cpp.dbg_run.9.sh`` is exclusively a runner-part for ``temp.9.sh`` runner
  template (and not for ``temp.3.sh`` or ``temp.4.sh`` for example),
- on the other hand, ``cpp.dbg_run.9.sh`` gets interpolated in ``temp.9.sh``
  when *any* *cpp* language template is selected (either *cpp.3* or *cpp.9* or
  even *cpp.100*) with *sh.9* runner template.



=======
Authors
=======

`Zoran Plesivčak`_ created **hac** and `these fine people`_ have contributed.



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

