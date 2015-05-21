# -*- coding: utf-8 -*-
"""Parsing CLI arguments.
"""
import os
import argparse


"""Parse arguments used in CLI parser.
"""
_pargs_pack_cli = [
    # TODO refactor (some arguments handled by parser, some handled manually)
    # -> remove from argparse when custom help is written
    {
        "names": ("location",),
        "params": {
            "help":
                """Unique identifier for contest (options: [a] URL, [b]
                'website ID'/'contest ID') or specific problem (URL)""",
            "metavar": "(CONTEST | PROBLEM)",
        }
    },
    #TODO format help better
    {
        "names": ("problems",),
        "params": {
            "action": "append",
            "nargs": "*",
            "help":
                """Optional identifiers for additional problems (options: [a]
                problem's ID, [b] problem's number) from contest specified by
                previous argument""",
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
    )

