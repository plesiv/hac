# -*- coding: utf-8 -*-
"""Common functionality for parsing CLI/configuration.
"""
import os

import hac
from hac import DataType
from hac.commands import app_commands, app_commands_help


_commands_choices = sorted(app_commands.keys())
_commands_help = "\n".join(["Command to be executed:"] +
                            [app_commands_help[com]
                                for com in sorted(app_commands.keys())])


"""Constant common parse arguments used in:

    - parsers for CLI files,
    - parsers for configuration files.
"""
_pargs_pack_common_const = [
    {
        "names": ("--version",),
        "params": {
            "action": "store_true",
            "help": """show application version and exit""",
            "dest": "version",
            "default": False,
        },
    },
    {
        "names": ("--copy-config",),
        "params": {
            "action": "store_true",
            "help":
"""copy configuration to user's local directory
(~/.config/hac by default, modifiable by setting
HAC_CONFIG_DIR environment variable)

""",
            "dest": "copy_config",
            "default": False,
        },
    },
    (
        {
            "names": ("-v", "--verbose"),
            "params": {
                "action": "store_true",
                "help": """increase output verbosity""",
                "dest": "verbose",
                "default": False,
            },
        },
        {
            "names": ("-V", "--terse"),
            "params": {
                "action": "store_true",
                "help": """decrease output verbosity""",
                "dest": "quiet",
                "default": False,
            },
        },
    ),
    {
        "names": ("-d", "--subdir-depth"),
        "params": {
            "type": int,
            "choices": [0, 1, 2],
            "help":
"""Additional levels at which to create files:
  0 - working directory,
  1 - directory for each problem,
  2 - directory for contest and sub-directory every
      task""",
            "dest": "subdir_depth"
        }
    },
    {
        "names": ("-w", "--workdir"),
        "params": {
            "help":
"""Change working directory (it has to exist).
Current directory by default.""",
            "metavar": "WD",
            "dest": "workdir"
        }
    },
    {
        "names": ("-t", "--tests"),
        "params": {
            "type": int,
            "choices": [0, 1],
            "help":
"""Prepare testcases (I/O samples):
  0 - no testcases
  1 - pretests""",
            "dest": "tests"
        }
    },
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
            "choices": _commands_choices,
            "help": _commands_help,
            "metavar": " | ".join(_commands_choices)
        }
    },
]

def get_pargs_pack_common(choice_langs = [], choice_runners = []):
    """Returns merge of constant and variable common parse arguments.
    """
    _pargs_pack_common_var = [
        {
            "names": ("-l", "--lang"),
            "params": {
                "action": "append",
                "choices": ['no'] + choice_langs,
                "help":
                    """Language-templates to copy""",
                "dest": "lang"
            }
        },
        {
            "names": ("-r", "--runner"),
            "params": {
                "action": "append",
                "choices": ['no'] + choice_runners,
                "help": """Runner-templates to process and copy""",
                "dest": "runner"
            }
        },
    ]

    return _pargs_pack_common_const + _pargs_pack_common_var


def pargs_packed_add(parser, pack):
    """Unpacks parse arguments and adds them to parser.

    Each element in pack is either:

      - dict to be unpacked directly in `add_argument`
      - tuple containing dicts of arguments that should be put in
        mutually-exclusive group

    """
    for arg in pack:
        # Unpack mutually-exclusive group (tuple).
        if type(arg) == tuple:
            group = parser.add_mutually_exclusive_group()
            for subarg in arg:
                group.add_argument(*subarg["names"], **subarg["params"])

        # Unpack regular argument.
        else:
            parser.add_argument(*arg["names"], **arg["params"])

