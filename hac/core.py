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


def main(args=sys.argv[1:]):
    """Execution flow of the main function:

    1) get configuration (priorities: default < local < cli)
    2) branch according to specified command
    """

    # TODO read default configuration
    cont = config_parser.parse_args(
        ['@' + os.path.join(DEFAULT_CONFIG_DIR, CONFIG_FILENAME)])
    print(vars(cont))
    sys.exit(ExitStatus.ERROR)

    # Show help and exit when no arguments given.
    if len(args) == 0:
        cli_parser.print_help()
        sys.exit(ExitStatus.ERROR)


    # TODO read local configuration

    # Override default and user configuration with CLI arguments
    args = cli_parser.parse_args(args=args) # TODO env add
    print(vars(args))

    # TODO create whole directory structure which doesn't exist
