# -*- coding: utf-8 -*-
"""Utilities for application plugin-system.

NOTE: for simplicity, language and runner templates are referred to as plug-ins
      in this file (along with site plug-ins).
"""
import imp
import os
import sys
import re

if sys.version_info.major == 2:
    from urlparse import urlparse
else:
    from urllib.parse import urlparse

import hac
from hac import DataType
from hac.data import ISiteRegistry


_plugin_filename_regex = {
    DataType.LANG: r"(?P<temp>[^.]+)\.(?P<prio>[^.]+)\.(?P<ext>[^.]+)",
    DataType.RUNNER: r"(?P<temp>[^.]+)\.(?P<prio>[^.]+)\.(?P<ext>[^.]+)",
}

# -- Languages ----------------------------------------------------------------
def _plugin_discover_langs(dirs):
    """Discovers all available programming language templates in a given list
    of directories.

    Programming language template file-names are expected to be in the format:

        <PLUGIN_TEMP>.<PRIORITY>.<LANGUAGE-EXTENSION>

    Where:

        * <PLUGIN_TEMP> is application constant setting (from SETTINGS_CONST).
        * <PRIORITY> is the integer higher or equal to zero. Lower <PRIORITY>
                     number indicates higher priority.

    For example highest priority Python language template would have filename:

        temp.0.py

    Function returns dictionary mapping "<LANGUAGE-EXTENSION>.<PRIORITY>" to
    the contents of the given language template file.
    """
    filename_pattern = re.compile(_plugin_filename_regex[DataType.LANG]);

    langs = {}
    for cdir in dirs:
        if os.path.isdir(cdir):
            for filename in os.listdir(cdir):
                tokens = filename_pattern.search(filename)
                if tokens: # Filename matches specified regular expression
                    key = tokens.group("ext") + "." + tokens.group("prio")
                    if (key not in langs):
                        with open(os.path.join(cdir, filename), 'r') as f:
                            contents = f.read()
                        langs[key] = contents
    return langs


# -- Runners ------------------------------------------------------------------
def _plugin_discover_runners(dirs):
    """
    """
    pass

# -- Sites --------------------------------------------------------------------
def _plugin_discover_sites(dirs):
    """Dynamically discovers all web-site processors in a given list of
    directories.

    Returns list of site-processor objects. Site processors occurring in a
    directories earlier in the input list have a higher priority. All
    discovered classes are instantiated with empty constructor.
    """
    for cdir in dirs:
        if os.path.isdir(cdir):
            for filename in os.listdir(cdir):
                froot, fext = os.path.splitext(filename)
                if fext == ".py":
                    fname, fpath, fdescr = imp.find_module(froot, [cdir])
                    if fname:
                        # Register discovered site-processor module in
                        # ISiteRegistry.sites
                        mod = imp.load_module(froot, fname, fpath, fdescr)
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
_plugin_discover_funcs = {
    DataType.LANG: _plugin_discover_langs,
    DataType.RUNNER: _plugin_discover_runners,
    DataType.SITE: _plugin_discover_sites,
}


def plugin_collect(data_type):
    """Retrieves application default and user-specified plug-ins.

    User-specified plug-ins of the same name override application default
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

