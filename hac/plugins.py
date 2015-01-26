# -*- coding: utf-8 -*-
"""Application plugin system. Web-site processors are pluggable.
"""

import os
import imp
from hac.data import ISiteRegistry
from hac.config import DEFAULTS


# Generic function for dynamically discovering all web-site processors. Returns
# list of objects; all discovered classes are instantiated with empty
# constructor.
def discover_sites(dirs):
    """
    """
    for cdir in dirs:
        if os.path.isdir(cdir):
            for filename in os.listdir(cdir):
                modname, ext = os.path.splitext(filename)
                if ext == '.py':
                    file, path, descr = imp.find_module(modname, [cdir])
                    if file:
                        # Loading the module registers the plugin in
                        # ISiteRegistry
                        mod = imp.load_module(modname, file, path, descr)
    return [ site() for site in ISiteRegistry.sites ]


# Retrieves default and user-specified web-site processors
def get_sites():
    """
    """
    return discover_sites([
        os.path.join(DEFAULTS["config_app_dirpath"],
                     DEFAULTS["sites_dirname"]),
        os.path.join(DEFAULTS["config_user_dirpath"],
                     DEFAULTS["sites_dirname"]),
    ]);

