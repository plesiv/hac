****************
HAC: User Manual
****************

**hac** can be extended very easily to work with:

- *any programming language* usable from the command-line,
- *any runner* usable from the command-line (examples: *shell scripts*,
  *Makefiles*, *ant scripts*),
- *any site* that exposes information about contests/problems in an uniform and
  web-accessible form (examples: `Codeforces <http://codeforces.com/>`_,
  `Sphere online judge <http://www.spoj.com/>`_).



=====
Usage
=====

Special commands that don't fetch remote data:

.. code-block:: bash

    $ hac --help         # show help
    $ hac --version      # show version
    $ hac --copy-config  # copy configuration (to ~/.config/hac by default)


Commands that fetch remote data and process it:

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



============
Contributing
============

These are *especially* needed:

- better and more language templates,
- other runner templates,
- template-parts for existing runners and other languages,
- site processors for other sites (e.g. Codechef, UVA Online Judge etc.)


Other contributions needed:

- code or documentation improvements,
- testing and porting HAC to Windows and MAC OS X,
- creating packages for different platforms (e.g. Ubuntu/Debian, MAC OS X).


----------------------------------------
Instructions for writing site processors
----------------------------------------

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Creating XPATH patterns for scraping
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Install *scrapy* from your distribution's package manager.

Alternatively install *scrapy* via ``pip`` (make sure you're using ``pip`` with
Python 2; Python needs to have support for *sqlite*):

.. code-block:: bash

    $ pip install --upgrade --user scrapy

Run *scrapy* on desired URL and try out different XPATHs.

.. code-block:: bash

    $ scrapy shell 'http://scrapy.org' --nolog
  >>> response.xpath("//h1/text()").extract()[0]

When devising the XPATH for desired element it's easiest to use developer tools
in one of the modern browsers. For example Chrome enables user to ``Copy
XPATH`` of a selected element. Iterate on this XPATH in ``scrapy`` shell until
you reach satisfactory form.


------------------------
Development instructions
------------------------

*TODO*: To be written...

