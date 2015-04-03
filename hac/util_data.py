# -*- coding: utf-8 -*-
"""Utilities for application plugin-system.

NOTE: for simplicity, language and runner templates are referred to as plug-ins
      in this file (along with site plug-ins).
"""
import imp
import os
import sys

if sys.version_info.major == 2:
    from urlparse import urlparse
else:
    from urllib.parse import urlparse

import hac
from hac import DataType
from hac.data import ISiteRegistry


# -- Languages ----------------------------------------------------------------
def _plugin_discover_langs(dirs):
    """
    """
    pass


# -- Runners ------------------------------------------------------------------
def _plugin_discover_runners(dirs):
    """
    """
    pass

# -- Sites --------------------------------------------------------------------
def _plugin_discover_sites(dirs):
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


# TODO crowd-source writing of this function
def plugin_match_site(sites, conf): #very-stupid matching now
    """Must return a site. Reasonable default site if can't match any site
    explicitly.
    """
    for site in sites:
        hostname = urlparse(conf['location']).hostname.lower()
        if(hostname in site.name.lower() or hostname in site.ID.lower()):
            return site.url
    return sites[0].url


# -- Common data utilities ----------------------------------------------------
_plugin_discover_funcs = []
_plugin_discover_funcs.insert(DataType.LANG, _plugin_discover_langs)
_plugin_discover_funcs.insert(DataType.RUNNER, _plugin_discover_runners)
_plugin_discover_funcs.insert(DataType.SITE, _plugin_discover_sites)


def plugin_collect(data_type):
    """Retrieves application default and user-specified plug-ins.

    User-specified plug-ins of the same name override applicatin default
    plug-ins.
    """
    plugin_path = hac.SETTINGS_CONST["plugin_path"][data_type]
    plugin_discover = _plugin_discover_funcs[data_type]

    return plugin_discover([
        os.path.join(hac.SETTINGS_CONST["config_user_path"],
                     plugin_path),
        os.path.join(hac.SETTINGS_VAR["app_root_dir"],
                     hac.SETTINGS_CONST["config_app_path"],
                     plugin_path),
    ])

