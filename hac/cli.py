# -*- coding: utf-8 -*-
"""CLI arguments definition.
"""
import os
import argparse

# Construct parser.
cli_parser = argparse.ArgumentParser(
    description=
        """how to use...
        """,#TODO
    epilog="Examples...",#TODO
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)

commmon_args = [
    # TODO DEFAULTS and CHOICES from configs
    {
        "names": ("-d", "--subdir-depth"),
        "params": {
            "default": 1,
            "type": int,
            "choices": [0, 1, 2],
            "help":
                """Additional directory depth at which to work; 0 - current
                directory, 1 - directory per task, 2 - directory for contest
                and sub-directory per task""",
            "dest": "subdir_depth"
        }
    },
    {
        #TODO if -lno -> clear all previous langs
        #TODO multiple langs separated by comma ?
        #TODO for no lang in final and executor present -> output executors template
        "names": ("-l", "--lang"),
        "params": {
            "action": "append",
            "default": "no",
            "choices": ["no", "py", "cpp"],
            "help":
                """Languages for which to prepare the environment""",
            "dest": "lang"
        }
    },
    {
        "names": ("-r", "--runner"),
        "params": {
            "action": "append",
            "default": "no",
            "choices": ["no", "sh"],
            "help":
                """Runners for which to prepare the environment""",
            "dest": "runner"
        }
    },
    {
        "names": ("-w", "--workdir"),
        "params": {
            "default": os.curdir,
            "help":
                """Change working directory for program""",
            "metavar": "DIR",
            "dest": "workdir"
        }
    },
    {
        "names": ("-t", "--testcases"),
        "params": {
            "default": 1,
            "choices": [0, 1],
            "help":
                """Prepare testcases (e.g. I/O samples); 0 - no testcases, 1 -
                pretests""",
            "dest": "testcases"
        }
    },
    #TODO force defaults to False
    #TODO remove defaults in help
    (
        {
            "names": ("-f", "--force"),
            "params": {
                "action": "store_true",
                "help": "Overwrite existing files",
                "dest": "force"
            }
        },
        {
            "names": ("-F", "--no-force"),
            "params": {
                "action": "store_false",
                "help": "Warn if files already exist",
                "dest": "force"
            }
        },
    )
]

#TODO version to cli arguments
#TODO test-cases for arguments

for arg in commmon_args:
    # Mutually exclusive group of arguments for arguments in tuple.
    if type(arg) == tuple:
        group = cli_parser.add_mutually_exclusive_group()
        for subarg in arg:
            group.add_argument(*subarg["names"], **subarg["params"])

    # Regular arguments.
    else:
        cli_parser.add_argument(*arg["names"], **arg["params"])


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
