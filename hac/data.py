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

    def __init__(self, name=None, id=None, url=None, time_limit_ms=2000,
                 memory_limit_kbyte=262144, source_limit_kbyte=64):
        self.name = name
        self.id = id
        # 'url' member used to distinguish between different sites.
        self.url = url
        self.time_limit_ms = time_limit_ms
        self.memory_limit_kbyte = memory_limit_kbyte
        self.source_limit_kbyte = source_limit_kbyte

        self._info = None

    @staticmethod
    def get_props(verbose=False):
        return ['id', 'url'] if not verbose else \
               ['name', 'id', 'url', 'time_limit_ms', 'memory_limit_kbyte',
                'source_limit_kbyte']

    @abstractmethod
    def match_contest(self, conf):
        """Generates well formated URL of the contest according to user input.
        """
        pass

    @abstractmethod
    def get_contest(self, url):
        """Fetches data from the provided contest URL and generates contest
        object.
        """
        pass

    @abstractmethod
    def match_problems(self, conf):
        """Generates list of well formated problem URLs according to user
        input.
        """
        pass

    @abstractmethod
    def get_problems(self, urls):
        """Fetches data from the provided problem URLs and generates list of
        problem objects.
        """
        pass


# -- Containers ---------------------------------------------------------------
class Contest(object):
    """Contest info container.
    """

    def __init__(self, name=None, id=None, url=None):
        self.name = name
        self.id = id
        self.url = url

    @staticmethod
    def get_props(verbose=False):
        return ['id', 'url'] if not verbose else \
               ['name', 'id', 'url']


class Problem(object):
    """Problem info container.
    """

    def __init__(self, name=None, id=None, url=None, time_limit_ms=2000,
                 memory_limit_kbyte=262144, source_limit_kbyte=64, inputs=None,
                 outputs=None):
        self.name = name
        self.id = id
        self.url = url
        self.time_limit_ms = time_limit_ms
        self.memory_limit_kbyte = memory_limit_kbyte
        self.source_limit_kbyte = source_limit_kbyte
        self.inputs = inputs or []
        self.outputs = outputs or []

    @staticmethod
    def get_props(verbose=False):
        return ['id', 'url'] if not verbose else \
               ['name', 'id', 'url', 'time_limit_ms', 'memory_limit_kbyte',
                'source_limit_kbyte', 'inputs', 'outputs']

