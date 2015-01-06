# -*- coding: utf-8 -*-
"""This module provides the main functionality.
"""
import sys

from hac import ExitStatus
from hac.cli import cli_parser


def main(args=sys.argv[1:]):
    """Execution flow of the main function:

    1) get configuration (priorities: default < local < cli)
    2) branch according to specified command
    """

    # Show help and exit when no arguments given.
    if len(args) == 0:
        cli_parser.print_help()
        sys.exit(ExitStatus.ERROR)

    # TODO read default configuration
    # TODO read local configuration

    # Override default and user configuration with CLI arguments
    args = cli_parser.parse_args(args=args) # TODO env add

