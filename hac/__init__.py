# -*- coding: utf-8 -*-
"""hac - Helper for Algorithm Competitions
"""
import os


__author__ = 'Zoran Plesivčak'
__version__ = '0.1.0'
__license__ = 'GPLv2'


# Initializes shared settings
def init_settings():

    # Application top directory
    global HAC_ROOT_DIR
    HAC_ROOT_DIR = '/'

    # Controls the verbosity of output
    global VERBOSE_OUTPUT
    VERBOSE_OUTPUT = False

# Application configuration constants.
DEFAULT_CONFIGS = {
    "config_filename": "hacrc",
    "config_app_dirpath": "config",
    "config_user_dirpath": \
        os.environ.get('HAC_CONFIG_DIR',
        os.path.expanduser('~/.config/hac')),
    "sites_dirname": "site"
}

# Enumeration containing exit-status codes.
class ExitStatus(object):
    """Exit status code constants."""
    OK = 0
    ERROR = 1
