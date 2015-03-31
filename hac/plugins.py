# -*- coding: utf-8 -*-
"""Application plugin system. Web-site processors are pluggable.
"""

import os
import imp
from hac import DEFAULT_CONFIGS
from hac.data import ISiteRegistry


# Generic function for dynamically discovering all web-site processors. Returns
# list of objects; all discovered classes are instantiated with empty
# constructor.
def discover_sites(dirs):
    """
    """
    for cdir in dirs:
        if os.path.isdir(cdir):
            for filename in os.listdir(cdir):
                mname, mext = os.path.splitext(filename)
                if mext == ".py":
                    fname, path, descr = imp.find_module(mname, [cdir])
                    if fname:
                        # Loading the module registers the web-site processor
                        # class in ISiteRegistry.sites
                        mod = imp.load_module(mname, fname, path, descr)
    return [ site() for site in ISiteRegistry.sites ]


# Retrieves default and user-specified web-site processors
def collect_sites():
    """User-specified web-site processors of the same name override default
    processors.
    """
    return discover_sites([
        os.path.join(DEFAULT_CONFIGS["config_user_dirpath"],
                     DEFAULT_CONFIGS["sites_dirname"]),
        os.path.join(DEFAULT_CONFIGS["config_app_dirpath"],
                     DEFAULT_CONFIGS["sites_dirname"]),
    ])

