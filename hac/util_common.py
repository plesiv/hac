# -*- coding: utf-8 -*-
"""Common utilities.
"""
import sys
from os import mkdir, remove
from os.path import exists, isdir


# -- Printing to STDERR -------------------------------------------------------
def warn(msg):
    sys.stderr.write("WARNING: " + msg + "\n")

def error(msg):
    sys.stderr.write("ERROR: " + msg + "\n")


# -- Helpers for lists and dictionaries ---------------------------------------
def dict_override(a, b):
    """Overriding dictionary values.

    Values in second dictionary override the values in the first one (except
    when relevant value in second dictionary is None).

    >>> dict_override({'a': 1,'b': 2}, {'a': 3,'b': None}) == {'a': 3,'b': 2}
    True

    >>> dict_override({'a': 3,'b': None}, {'a': 1,'b': 2}) == {'a': 1,'b': 2}
    True
    """
    res = {}
    for key in (set(a.keys()) | set(b.keys())):
        if (key in b) and (b[key] != None):
            res[key] = b[key]
        else:
            res[key] = a[key]
    return res


def list_reduce(a):
    """Reduces provided list in two steps:
        1) removes all elements from list that appear prior to any 'no' element,
        2) removes duplicates and sorts elements.

    >>> list_reduce(['cpp', 'no', 'php', 'py', 'php', 'py'])
    ['php', 'py']

    >>> list_reduce(['cpp', 'no', 'php', 'py', 'php', 'no', 'py', 'cpp'])
    ['cpp', 'py']
    """
    b = list(reversed(a))
    if "no" in b:
        ind = b.index("no")
        del b[ind:]
    return sorted(set(b))


def mainargs_index(a):
    """Removes optional arguments that precede mandatory arguments.

    >>> mainargs_index(['-lcpp', '--no', '-t', 'php', 'py'])
    3

    >>> mainargs_index(['--cpp', '--no'])
    2

    >>> mainargs_index([])
    0
    """
    indices = [ i for i, v in enumerate(a) if not v.startswith("-") ]
    return indices[0] if indices else len(a)


# -- Filesystem operations ----------------------------------------------------
def mkdir_safe(path, force=False):
    """Carefully handles directory creation. Notifies about special
    occurrences.

    Argument force used to decide if priorly existing file named "path" should
    be replaced with directory named "path".
    """
    if not exists(path):
        mkdir(path)
    else:
        if isdir(path):
            warn('Directory "' + path + '" already exists!')
        else:
            # Distinguish between two cases (depending on argument force), if:
            #
            #   - path exists and
            #   - it's not a directory
            #
            if force:
                warn('Deleting file "' + path + '" and creating directory!')
                remove(path)
                mkdir(path)
            else:
                warn('"' + path + '" is not a directory!')

