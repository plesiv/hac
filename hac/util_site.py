# -*- coding: utf-8 -*-
"""Utilities for web-site-processors plugin-system.
"""
import imp
import os
import sys

if sys.version_info.major == 2:
    from urlparse import urlparse
else:
    from urllib.parse import urlparse

from hac import DEFAULT_CONFIGS
from hac.data import ISiteRegistry


def _plugin_sites_discover(dirs):
    """Dynamically discovers all web-site processors in a given directory.

    Returns list of site-processor objects. All discovered classes are
    instantiated with empty constructor.
    """
    for cdir in dirs:
        if os.path.isdir(cdir):
            for filename in os.listdir(cdir):
                mname, mext = os.path.splitext(filename)
                if mext == ".py":
                    fname, path, descr = imp.find_module(mname, [cdir])
                    if fname:
                        # Register discovered site-processor module in
                        # ISiteRegistry.sites
                        mod = imp.load_module(mname, fname, path, descr)
    return [ site() for site in ISiteRegistry.sites ]


def plugin_sites_collect():
    """ Retrieves default and user-specified web-site processors

    User-specified web-site processors of the same name override default
    processors.
    """
    return _plugin_sites_discover([
        os.path.join(DEFAULT_CONFIGS["config_user_dirpath"],
                     DEFAULT_CONFIGS["sites_dirname"]),
        os.path.join(DEFAULT_CONFIGS["config_app_dirpath"],
                     DEFAULT_CONFIGS["sites_dirname"]),
    ])


# TODO crowd-source writing of this function
def site_match(sites, conf): #very-stupid matching now
    for site in sites:
        hostname = urlparse(conf['location']).hostname.lower()
        if(hostname in site.name.lower() or hostname in site.ID.lower()):
            return site.url
    return sites[0].url


# Exactracting site with exact url
def site_get(sites, url):
    for site in sites:
        if(url == site.url):
            return site
    return None

