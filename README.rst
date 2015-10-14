**************************************
HAC: Helper for Algorithm Competitions
**************************************

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



-------------
Configuration
-------------

User specific configuration is located in ``~/.config/hac`` directory by
default (set ``HAC_CONFIG_DIR`` environment variable to change this). 

To configure **hac**:

- copy all default-configuration files in a temporary directory,

.. code-block:: bash

    $ HAC_CONFIG_DIR=~/temp_config hac --copy-config

- customize files in a temporary directory ``~/temp_config``,
- move *only customized* files to ``~/.config/hac``, e.g.

.. code-block:: bash

    $ mkdir -p ~/.config/hac
    $ cp ~/temp_config/hacrc ~/.config/hacrc

- remove temporary directory.

.. code-block:: bash

    $ rm -r ~/temp_config

This approach is desirable because only configuration files that differ from
the default ones should be present in user's configuration directory, so that
only selected default configuration will be overshadowed.



==========
Contribute
==========

Contributions are welcome! Please see `CONTRIBUTING
<https://github.com/plesiv/hac/blob/master/CONTRIBUTING.rst>`_.



==========
Change Log
==========

Please see `CHANGELOG <https://github.com/plesiv/hac/blob/master/CHANGELOG.rst>`_.



=======
Licence
=======

Please see `LICENSE <https://github.com/plesiv/hac/blob/master/LICENSE>`_.



===========
User Manual
===========

**hac** can be extended very easily to work with:

- *any programming language* usable from the command-line,
- *any runner* usable from the command-line (examples: *shell scripts*,
  *Makefiles*, *ant scripts*),
- *any site* that exposes information about contests/problems in an uniform and
  web-accessible form (examples: `Codeforces <http://codeforces.com/>`_,
  `Codechef <http://www.codechef.com/>`_).


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

~~~~~~~~~~~~~~
Clarifications
~~~~~~~~~~~~~~

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

