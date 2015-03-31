# -*- coding: utf-8 -*-
"""Data-structures definitons for:
    - web-sites
    - contests
    - problems
"""

from abc import ABCMeta, abstractmethod


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
    """
    """
    def __init__(self, url=None, name=None, ID=None, time_limit_ms=2000,
                 memory_limit_kbyte=262144, source_limit_kbyte=64):
        self.url = url
        self.name = name
        self.ID = ID
        self.time_limit_ms = time_limit_ms
        self.memory_limit_kbyte = memory_limit_kbyte
        self.source_limit_kbyte = source_limit_kbyte

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
    def __init__(self, url=None, name=None, ID=None):
        self.url = url
        self.name = name
        self.ID = ID

# Problem data-structure
class Problem(object):
    def __init__(self, url=None, name=None, ID=None, time_limit_ms=2000,
                 memory_limit_kbyte=262144, source_limit_kbyte=64, inputs=[],
                 outputs=[]):
        self.url = url
        self.name = name
        self.ID = ID
        self.time_limit_ms = time_limit_ms
        self.memory_limit_kbyte = memory_limit_kbyte
        self.source_limit_kbyte = source_limit_kbyte
        self.inputs = inputs
        self.outputs = outputs

