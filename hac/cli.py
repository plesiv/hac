# -*- coding: utf-8 -*-
"""Parsing CLI arguments.
"""
import os
import argparse

from hac.parse import common_args, add_packed_arguments


# Construct CLI parser.
cli_parser = argparse.ArgumentParser(
    description=
        """how to use...
        """,#TODO
    epilog="Examples...",#TODO
)


# Add common arguments to CLI parser.
add_packed_arguments(cli_parser, common_args)


# Add CLI specific arguments.
cli_parser.add_argument(
    "location",
    #TODO format help better
    help=
        """Unique identifier for contest (options: [a] URL, [b] 'website ID'/'contest
        ID') or specific problem (URL)""",
    metavar="(CONTEST | PROBLEM)",
    #metavar="(CONTEST | CONTEST URL | PROBLEM URL)",
)
cli_parser.add_argument(
    "problems",
    action="append",
    nargs="*",
    help=
        """Optional identifiers for additional problems (options: [a] problem's
        ID, [b] problem's number) from contest specified by previous
        argument""",
    metavar="PROBLEM"
    #metavar="[(PROBLEM ID | PROBLEM ORDINAL NUMBER | PROBLEM URL) ...]",
)
