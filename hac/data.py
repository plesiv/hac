# -*- coding: utf-8 -*-
"""Data-structures definitons for:
    - web-sites
    - contests
    - problems
"""
from abc import ABCMeta, abstractmethod

import hac
from hac.util_common import with_metaclass


# -- Dynamic data (plugins) ---------------------------------------------------
class ISiteRegistry(ABCMeta):
    """Dynamic registry of sites (plugin architecture).
    """
    sites = []
    def __init__(cls, name, bases, attrs):
        if name != 'ISite':
            ISiteRegistry.sites.append(cls)


@with_metaclass(ISiteRegistry)
class ISite(object):
    """Site template.
    """

    def __init__(self, name=None, ID=None, url=None, time_limit_ms=2000,
                 memory_limit_kbyte=262144, source_limit_kbyte=64):
        self.name = name
        self.ID = ID
        self.url = url
        self.time_limit_ms = time_limit_ms
        self.memory_limit_kbyte = memory_limit_kbyte
        self.source_limit_kbyte = source_limit_kbyte

    @staticmethod
    def get_props(verbose=False):
        return ['ID', 'url'] if not verbose else \
               ['name', 'ID', 'url', 'time_limit_ms', 'memory_limit_kbyte',
                'source_limit_kbyte']

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


# -- Containers ---------------------------------------------------------------
class Contest(object):
    """Contest info container.
    """

    def __init__(self, name=None, ID=None, url=None):
        self.name = name
        self.ID = ID
        self.url = url

    @staticmethod
    def get_props(verbose=False):
        return ['ID', 'url'] if not verbose else \
               ['name', 'ID', 'url']


class Problem(object):
    """Problem info container.
    """

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

    @staticmethod
    def get_props(verbose=False):
        return ['ID', 'url'] if not verbose else \
               ['name', 'ID', 'url', 'time_limit_ms', 'memory_limit_kbyte',
                'source_limit_kbyte', 'inputs', 'outputs']

