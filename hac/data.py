# -*- coding: utf-8 -*-
"""Data-structures definitons for:
    - web-sites
    - contests
    - problems

Converting objects of type ISite, Contest and Problem to dictionary (via "dict"
function) depends on global application setting
hac.VAR_SETTINGS["verbose_output"] being initialized.
"""
from abc import ABCMeta, abstractmethod

import hac


# Utility: portable (Python2/Python3) metaclassing
def with_metaclass(mcls):
    def decorator(cls):
        body = vars(cls).copy()
        # clean out class body
        body.pop('__dict__', None)
        body.pop('__weakref__', None)
        return mcls(cls.__name__, cls.__bases__, body)
    return decorator


# Web-site data-structure
class ISiteRegistry(ABCMeta):
    sites = []
    def __init__(cls, name, bases, attrs):
        if name != 'ISite':
            ISiteRegistry.sites.append(cls)


@with_metaclass(ISiteRegistry)
class ISite(object):
    """Site template.
    """
    keys_default = ['ID', 'url']
    keys_verbose = ['name', 'ID', 'url', 'time_limit_ms', 'memory_limit_kbyte',
                    'source_limit_kbyte']

    def __init__(self, name=None, ID=None, url=None, time_limit_ms=2000,
                 memory_limit_kbyte=262144, source_limit_kbyte=64):
        self.name = name
        self.ID = ID
        self.url = url
        self.time_limit_ms = time_limit_ms
        self.memory_limit_kbyte = memory_limit_kbyte
        self.source_limit_kbyte = source_limit_kbyte

    def __iter__(self):
        keys = ISite.keys_verbose if hac.VAR_SETTINGS["verbose_output"] else ISite.keys_default
        for key in keys:
            yield (key, getattr(self, key))

    @abstractmethod
    def match_contest(self, conf):
        """Returns well formated contest URL according to user input.
        """
        pass

    @abstractmethod
    def get_contest(self, url):
        """Expects well formated URL. Returns Contest object.
        """
        pass

    @abstractmethod
    def match_problems(self, conf):
        """Returns list of well formated problem URLs according to user input.
        """
        pass

    @abstractmethod
    def get_problems(self, urls):
        """Expects list of well formated URLs. Returns list of Problem objects.
        """
        pass


# Contest data-structure
class Contest(object):
    """Contest info container.
    """
    keys_default = ['ID', 'url']
    keys_verbose = ['name', 'ID', 'url']

    def __init__(self, name=None, ID=None, url=None):
        self.name = name
        self.ID = ID
        self.url = url

    def __iter__(self):
        keys = Contest.keys_verbose if hac.VAR_SETTINGS["verbose_output"] else Contest.keys_default
        for key in keys:
            yield (key, getattr(self, key))


# Problem data-structure
class Problem(object):
    """Problem info container.
    """
    keys_default = ['ID', 'url']
    keys_verbose = ['name', 'ID', 'url', 'time_limit_ms', 'memory_limit_kbyte',
                    'source_limit_kbyte', 'inputs', 'outputs']

    def __init__(self, name=None, ID=None, url=None, time_limit_ms=2000,
                 memory_limit_kbyte=262144, source_limit_kbyte=64, inputs=None,
                 outputs=None):
        self.name = name
        self.ID = ID
        self.url = url
        self.time_limit_ms = time_limit_ms
        self.memory_limit_kbyte = memory_limit_kbyte
        self.source_limit_kbyte = source_limit_kbyte
        self.inputs = inputs or []
        self.outputs = outputs or []

    def __iter__(self):
        keys = Problem.keys_verbose if hac.VAR_SETTINGS["verbose_output"] else Problem.keys_default
        for key in keys:
            yield (key, getattr(self, key))

