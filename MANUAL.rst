*******************
Contributing to HAC
*******************

======================
Types of contributions
======================

These are *especially* needed:

- better and more language templates,
- other runner templates,
- template-parts for existing runners and new languages,
- site processors for other sites (e.g. Codechef, UVA Online Judge etc.)


Other contributions needed:

- code or documentation improvements,
- testing and porting HAC to Windows and MAC OS X,
- creating packages for different platforms (e.g. Ubuntu/Debian, MAC OS X).


========================================
Instructions for writing site processors
========================================

------------------------------------
Creating XPATH patterns for scraping
------------------------------------

Install *scrapy* from your distribution's package manager.

Alternatively install *scrapy* via ``pip`` (make sure you're using ``pip`` with
Python 2; Python needs to have support for *sqlite*):

.. code-block:: bash

    user$ pip install --upgrade --user scrapy

Run *scrapy* on desired URL and try out different XPATHs.

.. code-block:: bash

    user$ scrapy shell 'http://scrapy.org' --nolog
      >>> response.xpath("//h1/text()").extract()[0]

When devising the XPATH for desired element it's easiest to use developer tools
in one of the modern browsers. For example Chrome enables user to ``Copy
XPATH`` of a selected element. Iterate on this XPATH in ``scrapy`` shell until
you reach satisfactory form.


========================
Development instructions
========================

*TODO*: To be written...

