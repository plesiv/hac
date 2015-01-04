# -*- coding: utf-8 -*-
"""This module provides the main functionality.
"""
import sys


def main(args=sys.argv[1:]):
    """
    """

    from hac.cli import parser
    print(parser)

    # When no arguments given show Help
    #if len(args) == 0:
        #parser.print_help()
        #sys.exit(ExitStatus.ERROR)

