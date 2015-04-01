# -*- coding: utf-8 -*-
"""hac - Helper for Algorithm Competitions
"""
import os


__author__ = 'Zoran Plesivčak'
__version__ = '0.1.0'
__license__ = 'GPLv2'


# Initializes shared settings
def init_settings():
    global VAR_SETTINGS
    VAR_SETTINGS = {
        "app_root_dir": '/',
        "verbose_output" : False,
    }

# Application configuration constants.
CONST_SETTINGS = {
    "config_filename": "hacrc",
    "config_app_dirpath": "config",
    "config_user_dirpath": \
        os.environ.get('HAC_CONFIG_DIR',
        os.path.expanduser('~/.config/hac')),
    "dir_langs": "lang",
    "dir_runners": "runner",
    "dir_sites": "site",
}

# Enumeration containing exit-status codes.
class ExitStatus(object):
    """Exit status code constants."""
    OK = 0
    ERROR = 1
