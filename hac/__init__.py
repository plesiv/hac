# -*- coding: utf-8 -*-
"""hac - Helper for Algorithm Competitions
"""
import os
import sys


_python_version = '.'.join(map(str, list(sys.version_info[0:3])))

__author__ = 'Zoran Plesivčak'
__version__ = '0.1.0 (Python {0})'.format(_python_version)
__license__ = 'GPLv2'


# -- Enums --------------------------------------------------------------------
class DataType(object):
    """Data types."""
    LANG = 0
    RUNNER = 1
    SITE = 2


class ExitStatus(object):
    """Exit status code constants."""
    OK = 0
    ERROR = 1


# -- Settings -----------------------------------------------------------------

# Application constant settings.
SETTINGS_CONST = {
    "app_root_dir": os.path.abspath(os.path.dirname(__file__)),
    "config_filename": "hacrc",
    "config_app_path": "config",
    "config_user_path": \
        os.environ.get('HAC_CONFIG_DIR',
        os.path.expanduser('~/.config/hac')),
    "plugin_path": {
        DataType.LANG: "lang",
        DataType.RUNNER: "runner",
        DataType.SITE: "site",
    },
    "plugin_temp_sep": {
        DataType.LANG: ".",
        DataType.RUNNER: ".",
    },
    "plugin_temp_part_prefix": {
        DataType.RUNNER: r"\$",
    },
}

