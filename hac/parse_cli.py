# -*- coding: utf-8 -*-
"""Parsing CLI arguments.
"""
import os
import argparse


"""Parse arguments used in CLI parser.
"""
_pargs_pack_cli = [
    {
        "names": ("location",),
        "params": {
            "help":
"""Contest or problem identifier. It can be either:
  - contest/problem URL
  - string of form "website-ID/contest-ID"
""",
            "metavar": "(CONTEST | PROBLEM)",
        }
    },
    {
        "names": ("problems",),
        "params": {
            "action": "append",
            "nargs": "*",
            "help":
"""Optional identifiers for additional problems from
contest specified by previous argument. Identifiers
can be either:
  - problem's ID
  - problem's index (counting from 1)
""",
            "metavar": "PROBLEM"
        }
    },
]


def get_pargs_pack_cli():
    """Returns CLI parse arguments.
    """
    return _pargs_pack_cli


# Parser notes.
_parser_cli_description = "how to use..." #TODO
_parser_cli_epilog = "Examples..." #TODO


def get_bare_cli_parser():
    """Returns bare CLI parser object without arguments. Arguments should be
    added to parser manually.
    """
    return argparse.ArgumentParser(
        description = _parser_cli_description,
        epilog = _parser_cli_epilog,
        formatter_class=argparse.RawTextHelpFormatter
    )

