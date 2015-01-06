# -*- coding: utf-8 -*-
"""This module provides the main functionality.
"""
import os
import sys
import textwrap

from hac import ExitStatus
from hac.config import \
    DEFAULT_CONFIG_DIR, USER_CONFIG_DIR, CONFIG_FILENAME, config_parser
from hac.cli import cli_parser


def dict_override(a, b):
    """Overriding dictionary values.

    Values in dict b overwrite values in dict a, except when value in dict b is
    None.
    """
    res = {}
    for key in set(a.keys() + b.keys()):
        if key in a:
            res[key] = a[key]
        if (key in b) and (b[key] != None):
            res[key] = b[key]
    return res


def main(args=sys.argv[1:]):
    """Execution flow of the main function:

    1) get configuration (priorities: default < local < cli)
    2) branch according to specified command
    """

    # Get default global configuration
    global_config_file = os.path.join(DEFAULT_CONFIG_DIR, CONFIG_FILENAME)
    env_global = config_parser.parse_args(['@' + global_config_file])

    # Get local configuration
    user_config_file = os.path.join(USER_CONFIG_DIR, CONFIG_FILENAME)
    if os.path.exists(user_config_file):
        env_user = config_parser.parse_args(['@' + user_config_file])

    # Show help and exit when no arguments given.
    if len(args) == 0:
        cli_parser.print_help()
        sys.exit(ExitStatus.ERROR)

    # Parse CLI arguments
    env_cli = cli_parser.parse_args(args=args)

    # Resolve configuration
    conf_user = dict_override(vars(env_global), vars(env_user))
    conf_all = dict_override(conf_user, vars(env_cli))

    print(conf_user)
    print(conf_all)

    # TODO create whole directory structure for dir that doesn't exist

