# -*- coding: utf-8 -*-
"""Common utilities.
"""
import re
import sys
import os
import stat
import shutil
from os.path import exists, isdir
from shutil import rmtree


# -- Printing to CLI ----------------------------------------------------------
def warn(msg):
    sys.stderr.write("WARNING: " + msg + os.linesep)

def error(msg):
    sys.stderr.write("ERROR: " + msg + os.linesep)


# -- Lists and dictionaries ---------------------------------------------------
def dict_override(a, b):
    """Overriding dictionary values.

    Values in second dictionary override the values in the first one (except
    when relevant value in second dictionary is None).

    >>> dict_override({'a': 1,'b': 2}, {'a': 3,'b': None}) == {'a': 3,'b': 2}
    True

    >>> dict_override({'a': 3,'b': None}, {'a': 1,'b': 2}) == {'a': 1,'b': 2}
    True

    >>> dict_override({'a': 6,'b': None}, {'b': 7}) == {'a': 6,'b': 7}
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

    >>> list_reduce(['js', 'no', 'c', 'cc', 'php', 'no', 'py', 'cpp'])
    ['cpp', 'py']
    """
    b = list(reversed(a))
    if "no" in b:
        ind = b.index("no")
        del b[ind:]
    return sorted(set(b))


# -- Command line arguments ---------------------------------------------------
def mainargs_index(a):
    """Removes optional arguments that precede mandatory arguments.

    >>> mainargs_index(['-lcpp', '--no', '-t', 'php', 'py'])
    3

    >>> mainargs_index(['--cpp', '--no'])
    2

    >>> mainargs_index([])
    0
    """
    indices = [i for i, v in enumerate(a) if not v.startswith("-")]
    return indices[0] if indices else len(a)


def choice_generate(a, separator='.'):
    """Returns input list with additional entries that represent choices
    without priority specifiers.

    >>> choice_generate(['no', 'cpp.0', 'cpp.1'])
    ['cpp', 'cpp.0', 'cpp.1', 'no']

    >>> choice_generate(['no', 'cpp.0', 'cpp.1', 'py.15'])
    ['cpp', 'cpp.0', 'cpp.1', 'no', 'py', 'py.15']
    """
    separator = '.'
    b = set(a)
    for e in a:
        if separator in e:
            b.add(e.split(separator)[0])
    return sorted(b)


def choice_normal(a, all_canonic, separator='.'):
    """Normalizes list a so that among multiple choices that differ only in
    priority modifier, just the highest priority one is present in the output
    list. All the members in the output list are in the canonic form
    <TYPE>.<PRIORITY>.

    List all_canonic contains the all available canonic entries.

    If in there is entry without the priority modifier in the input list, it
    corresponds to the request for highest priority choice available (one with
    lowest priority modifier).

    >>> choice_normal(['cpp.0', 'cpp.1', 'py'], ['cpp.0', 'cpp.1', 'py.15'])
    ['cpp.0', 'py.15']

    >>> choice_normal(['cpp', 'py.1', 'py'], ['cpp.1', 'py.0', 'py.1'])
    ['cpp.1', 'py.0']

    DEFINITIONS:
        - regular entries: 'cpp', 'cpp.0', 'py', 'py.15'
        - canonic entries: 'cpp.0', 'py.15'
        - bare entries: 'cpp', 'py'
    """
    separator = '.'
    assert all([separator in ec for ec in all_canonic])
    c2c = {ec: ec for ec in all_canonic}  # Map canonic to canonic.

    r2c = c2c.copy()                      # Map regular to canonic.
    for ec in sorted(set(all_canonic)):
        eb = ec.split(separator)[0]
        if eb not in r2c:
            r2c[eb] = ec

    r2b = {}                              # Map regular to bare.
    for er in r2c:
        assert separator in r2c[er]
        r2b[er] = r2c[er].split(separator)[0]

    b_track = set()
    ret = []
    for er in sorted(set(a)):
        eb = r2b[er]
        ec = r2c[er]
        if eb not in b_track:
            b_track.add(eb)
            ret.append(ec)

    return ret


# -- Templating ---------------------------------------------------------------
def indent(text, ws=''):
    """Implementation of textwrap.indent (textwrap.indent not available on
    Python 2).

    >>> indent('a\\n  \\n b', '   ')
    '   a\\n  \\n    b'
    """
    lines = [ws + ln if (ln and not ln.isspace()) else ln
                     for ln in text.rstrip().split(os.linesep)]
    return os.linesep.join(lines)


def indent_distribute(text, mapps, kprefix=r'\$'):
    """Arguments are:

        * text - template-text,
        * mapps - maps template-part name to template-part contents.

    Only template parts whose names occur as the first non-whitespace
    characters on the line in the template-text are considered. Function
    processes template-text and template-parts by:

        * distributing whitespace before template-part name found in
          template-text to the lines of corresponding template-part contents
          (this matched whitespace is removed from template-text),
        * removes everything after template-part name until the end-of-line.

    >>> indent_distribute(' $pat', {'pat': 'a\\n b\\n  \\nc'})
    ('$pat', {'pat': ' a\\n  b\\n  \\n c'})
    """
    rtext = text
    rmapps = mapps
    for key in mapps:
        pattern = re.compile(r'^(?P<ws>\s*)(?P<part>' + kprefix + key + r'\b)',
            re.MULTILINE)
        token = pattern.search(text)

        if token:
            ws = token.group('ws')
            part = token.group('part')
            rtext = re.sub(pattern, part, rtext)
            rmapps[key] = indent(mapps[key], ws)

    return rtext, rmapps


# -- Filesystem ---------------------------------------------------------------
def safe_mkdir(path, force=False):
    """Carefully handles directory creation. Notifies about special
    occurrences.

    Argument force used to decide if priorly existing file named "path" should
    be replaced with directory named "path".
    """
    if not exists(path):
        os.mkdir(path)
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
                os.remove(path)
                os.mkdir(path)
            else:
                warn('"' + path + '" is not a directory!')


def safe_cpdir(path_from, path_to, force=False):
    """Carefully handles recursive directory copying. Notifies about special
    occurrences.

    Argument force used to decide if priorly existing files in destination
    directory should be replaced with new files from source.
    """
    # When force is true (branching):
    #
    #
    # - source is DIR  && destination is DIR  -> do nothing
    #
    # - source is FILE && destination is DIR  \
    # - source is DIR  && destination is FILE  -> remove destination
    # - source is FILE && destination is FILE /
    #
    if force:
        if exists(path_from) and not isdir(path_from) and isdir(path_to):
            warn('Replacing directory "' + path_to + '"!')
            rmtree(path_to)

        if exists(path_from) and exists(path_to) and not isdir(path_to):
            warn('Replacing file "' + path_to + '"!')
            os.remove(path_to)

    # When source is directory (sequence):
    #
    # 1) destination doesn't exist -> create directory
    # 2) destination is directory  -> recursively copy
    #
    if isdir(path_from):
        if exists(path_to) and not isdir(path_to):
            warn('File named "' + path_to + '" already exists!')

        if not exists(path_to):
            os.mkdir(path_to)

        if isdir(path_to):
            for fp in os.listdir(path_from):
                safe_cpdir(os.path.join(path_from, fp),
                           os.path.join(path_to, fp),
                           force)

    # When source is file:
    #
    # - destination doesn't exist -> copy file
    #
    elif exists(path_from):
        if exists(path_to):
            warn('File/directory named "' + path_to + '" already exists!')
        else:
            shutil.copyfile(path_from, path_to)


def safe_fwrite(path, contents="", force=False, executable=False):
    """Carefully handles file writing. Notifies about special occurrences.

    Argument force used to decide if priorly existing file named "path" should
    be overwritten with provided contents.
    """
    # Path exists and is directory.
    if isdir(path):
        if force:
            warn('Deleting directory "' + path + '" and creating file!')
            rmtree(path)
        else:
            warn('Directory named "' + path + '" already exists!')

    # Path exists but is not directory.
    elif exists(path):
        if force:
            warn('Deleting file "' + path + '" and creating file!')
            os.remove(path)
        else:
            warn('File named "' + path + '" already exists!')

    # Writing to file.
    if not exists(path):
        with open(path, 'w') as f:
            f.write(contents)

    # Make file executable for everyone
    if executable:
        perms = os.stat(path)
        os.chmod(path, perms.st_mode | stat.S_IEXEC |
                                       stat.S_IXGRP |
                                       stat.S_IXOTH)


# -- Metaclassing (portable, works on Python2/Python3) ------------------------
def with_metaclass(mcls):
    def decorator(cls):
        body = vars(cls).copy()
        # Clean out class body.
        body.pop('__dict__', None)
        body.pop('__weakref__', None)
        return mcls(cls.__name__, cls.__bases__, body)
    return decorator

