# -*- coding: utf-8 -*-
"""Common functionality for parsing CLI/configuration.
"""
import os

import hac
from hac import DataType
from hac.commands import app_commands


# Arguments used in CLI and configuration files. Each element in list is
# either:
#   - dict to be unpacked directly in `add_argument`
#   - tuple containing dicts of arguments that should be put in
#     mutually-exclusive group
common_args = [
    # TODO DEFAULTS and CHOICES from configs
    {
        "names": ("-d", "--subdir-depth"),
        "params": {
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
            "choices": ["py", "cpp"],
            "help":
                """Languages for which to prepare the environment""",
            "dest": "lang"
        }
    },
    {
        "names": ("-r", "--runner"),
        "params": {
            "action": "append",
            "choices": ["no", "sh"],
            "help":
                """Runners for which to prepare the environment""",
            "dest": "runner"
        }
    },
    {
        #TODO document that workdir has to exist beforehand
        "names": ("-w", "--workdir"),
        "params": {
            "help":
                """Change working directory for program""",
            "metavar": "DIR",
            "dest": "workdir"
        }
    },
    {
        "names": ("-t", "--testcases"),
        "params": {
            "type": int,
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
    ),
    {
        "names": ("command",),
        "params": {
            "nargs": "?",
            "choices": sorted(app_commands.keys()),
            "help":
                """Prepare environment or show information about current
                configuration, diagnostics etc.""",
            "metavar": " | ".join(sorted(app_commands.keys()))
        }
    },
]

#TODO version to cli arguments
#TODO test-cases for arguments

# Unpacks arguments and adds them to parser
def add_packed_arguments(parser, pack):
    for arg in pack:
        # Unpack mutually-exclusive group (tuple).
        if type(arg) == tuple:
            group = parser.add_mutually_exclusive_group()
            for subarg in arg:
                group.add_argument(*subarg["names"], **subarg["params"])

        # Unpack regular argument.
        else:
            parser.add_argument(*arg["names"], **arg["params"])

