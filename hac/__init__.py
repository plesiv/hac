# -*- coding: utf-8 -*-
"""hac - Helper for Algorithm Competitions
"""
import os


__author__ = 'Zoran Plesivčak'
__version__ = '0.1.0'
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
def init_settings():
    """Initializes shared settings. All shared settings are visible throughout
    the whole application. Some of these settings are configurable via
    command-line/configuration-files switches.

    These settings are:
        - visible throughout the whole application,
        - modifiable by
    """
    global SETTINGS_VAR

    # Application variable settings
    SETTINGS_VAR = {
        "app_root_dir": '/',
        "verbose_output" : False,
    }

# Application constant settings.
SETTINGS_CONST = {
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
    "plugin_temp": {
        DataType.LANG: "temp",
        DataType.RUNNER: "temp",
    },
    "plugin_temp_sep": {
        DataType.LANG: ".",
        DataType.RUNNER: ".",
    },
    "plugin_temp_part_prefix": {
        DataType.RUNNER: r"\$",
    },
}

