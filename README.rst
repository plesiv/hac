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

- *any programming language* usable from the command-line,
- *any runner* usable from the command-line (examples: *shell scripts*,
  *Makefiles*, *ant scripts*),
- *any site* that exposes information about contests/problems in an uniform and
  web-accessible form (examples: `Codeforces <http://codeforces.com/>`_,
  `Codechef <http://www.codechef.com/>`_).


=======
Support
=======

If lack of support for particular programming language or site irks you, please
check `Contribute`_ section. This section contains current up-to-date support
information.


**Sites:**

- `Codeforces <http://codeforces.com/>`_


**Runner/language combinations:**

+-----------------+----------------------+----------------------+
|                 |         C++          |        Python        |
+=================+======================+======================+
| **POSIX shell** |  *sh.9*  /  *cpp.9*  |  *sh.9*  /  *py.9*   |
+-----------------+----------------------+----------------------+


**OS supported:**

- Linux (tested)
- MAC OS X (probably, not tested)


**Python versions:**

- 2.7
- 3.3
- 3.4



============
Installation
============

To install **hac** you need to have `pip`_ installed on your system. Since
**hac** messes with the file-system it is strongly advisable to install it as
regular user (to mitigate the responsibility that comes with the power ;) ):

.. code-block:: bash

    $ pip install --upgrade --user hac


Install at system-wide level as super-user at *your own* risk:

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

**1a)** Prepare these things for problems "B" and "C" from Codeforces contest
#527:

- source-file from *cpp* *highest priority* template (has lowest *X* among all
  *cpp.X* templates),
- runner from *sh.9* template (gets interpolated for *cpp* language template),
- pre-tests downloaded from `Codeforces <http://codeforces.com/>`_.

.. code-block:: bash

    $ mkdir ~/contests && cd ~/contests
    $ hac -d2 -lcpp -rsh.9 prep http://codeforces.com/527 B C


With default configuration *any* of the following lines is equivalent to the
line above:

.. code-block:: bash

    $ hac -lcpp.9 -rsh.9 prep http://codeforces.com/527 b c
    $ hac http://codeforces.com/527 B C
    $ hac CODEFORCES/527/B 3
    $ hac cf/527 2 3


**1b)** Write solution for problem "B" and test it on pre-tests:

.. code-block:: bash

    $ cd 527/B
    $ # ... modify B.cpp
    $ ./B.cpp.sh -e  # test solution on pre-tests
    $ ./B.cpp.sh -c  # clean generated outputs


**1c)** Debug solution for problem "B" on 2nd pre-test:

.. code-block:: bash

    $ ./B.cpp.sh -d 2


**2)** Display verbose information about:

- **hac**'s configuration,
- available sites, runner and language templates,
- selected site, contest and problems,
- problems' information for Codeforces contest #527.

.. code-block:: bash

    $ hac -v show http://codeforces.com/527
    $ # ... for terse information message
    $ hac -V show http://codeforces.com/527


-------------
Configuration
-------------

User specific configuration is located in ``~/.config/hac`` directory by
default (set ``HAC_CONFIG_DIR`` environment variable to change it). What
follows are approaches of how to setup user specific configuration.

**[NOT recommended]** Copy all default-configuration to user's configuration
directory and customize copied files:

.. code-block:: bash

    $ hac --copy-config
    $ # ... edit files in ~/.config/hac


**[Recommended]** Approach that prevents possible over-shadowing of updated
default-configuration files (when **hac** gets updated):

- copy all default-configuration files in a temporary directory,
- customize files in a temporary directory,
- move *only customized* files to ``~/.config/hac``,
- remove temporary directory.

.. code-block:: bash

    $ HAC_CONFIG_DIR=~/temp_config hac --copy-config
    $ cd ~/temp_config
    $ # ... a) customize interesting files in ~/temp_config
    $ # ... b) move *only* customized files to ~/.config/hac
    $ rm -r ~/temp_config



==================
How **hac** works?
==================

--------
Settings
--------

File ``hacrc`` is the main settings file. Total **hac** settings are calculated
in a *cascaded* manner (similar to *CSS*) by:

- taking settings from ``hacrc`` from default-configuration directory (not
  writable by user),
- overriding above settings with those from ``~/.config/hac/hacrc``,
- overriding all above settings with those from command-line arguments.


---------------------
Templates and plugins
---------------------

Files in ``~/.config/hac`` sub-directories (``lang``, ``runner``, ``site``)
over-shadow files in default-configuration directory *with the same name*. For
example file ``~/.config/hac/lang/temp.9.cpp`` over-shadows ``temp.9.cpp`` in
default-configuration directory.

Template-part ``~/.config/hac/runner/cpp.exec_compile.9.sh`` over-shadows
``cpp.exec_compile.9.sh`` in default-configuration directory. This
template-part gets interpolated in ``temp.9.sh`` runner template when runner
*sh.9* is prepared for any *cpp* language template. Creating and customizing
``~/.config/hac/runner/cpp.exec_compile.9.sh`` allows us change compilation
flags or compiler used for C++ source compilation.

**hac** dynamically discovers all templates and site-plugins when started and
displays information about what's found in:

- help message (``--help`` switch),
- verbose version of ``show`` command results.


-------------------------------
Templates naming and priorities
-------------------------------

Intentionally, **hac** discerns file-types of templates solely according to
template extensions. This means that templates ``*.cc`` and ``*.cpp`` are
considered as being of different file-type as far as **hac** is concerned.

Language templates' filenames are in the format ``temp.<L_PRIORITY>.<L_EXT>``
and should be located in ``lang`` subdirectory of **hac**'s configuration
directory. Label ``<L_PRIORITY>`` denotes priority of the template in
comparison to all other templates with the same ``<L_EXT>`` extension.

**Lower** ``<L_PRIORITY>`` denotes **higher** priority.

Priority labels of runner templates work in the same manner. Runner templates'
filenames are in the format ``temp.<R_PRIORITY>.<R_EXT>`` and runner-parts'
filenames are in the format ``<L_EXT>.<R_PART_LABLEL>.<R_PRIORITY>.<R_EXT>``.

When ``temp.<R_PRIORITY>.<R_EXT>`` runner template is selected together with
any language template with ``<L_EXT>`` extension (*irrespective of language
templates priority!*), runner-part
``<L_EXT>.<R_PART_LABLEL>.<R_PRIORITY>.<R_EXT>`` gets interpolated in
``temp.<R_PRIORITY>.<R_EXT>`` before runner is prepared in the destination
directory. These files should be located in ``runner`` subdirectory.

Priority labels of runner templates and runner-parts are *completely separate*
from the priority labels of language templates, this means that ``temp.9.cpp``
is not directly related to ``temp.9.sh``.

~~~~~~~~
Examples
~~~~~~~~

- If  there are ``temp.5.cpp`` and ``temp.9.cpp`` templates present in ``lang``
  subdirectory, running **hac** with ``-lcpp`` argument would select
  ``temp.5.cpp`` template. To select ``temp.9.cpp`` template one would have to
  run **hac** with explicit ``-lcpp.9`` argument that denotes template's
  *priority*.
- Runner-part ``cpp.dbg_run.9.sh`` is exclusively a runner-part for
  ``temp.9.sh`` runner template (and not for ``temp.3.sh`` or ``temp.4.sh``
  templates).
- Runner-part ``cpp.dbg_run.9.sh`` gets interpolated in ``temp.9.sh`` when
  *any* *cpp* language template is selected (either *cpp.3* or *cpp.9* or even
  *cpp.100*) with *sh.9* runner template. Interpolation is done by replacing
  ``$dbg_run`` label that appears alone in the line in ``temp.9.sh`` with
  appropriately indented contents of ``cpp.dbg_run.9.sh``.


---------------
Running **hac**
---------------

Check **hac**'s help message for more information!

When **hac** is run to prepare the environment (``prep`` command):

- selected language templates are copied for each task to the destination
  directories *unchanged*,
- selected runner templates are *processed (interpolated)* with corresponding
  template-parts before being moved to destination directories.



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

