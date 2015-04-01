# -*- coding: utf-8 -*-
"""Implementation of application commands.

Each command expects dictionary "args" to contain following entries:

    - conf_global: dictionary containing default application settings,
    - conf_user: dictionary containing user settings from configuration files
                 (override default application settings),
    - conf_all: dictionary containing command-line settings (override user
                settings from configuration files),
    - sites: list of all available site-processors (objects whose classes
             inherit from hac.data.ISite),
    - site_obj: selected site-processor (object whose class inherit from
                hac.data.ISite),
    - contest_obj: selected contest (instance of hac.data.Contest),
    - problems_objs: list of selected problems (instances of hac.data.Problem).
"""
import sys
from os import mkdir
from os.path import realpath, exists, isdir, join
from pprint import PrettyPrinter

import hac
from hac import ExitStatus
from hac.util_common import warn, error, mkdir_safe


def _command_prep(**args):
    """Prepares the environment for selected problems.

    This command is idempotent irrespective of the "--force" switch.
    """
    conf_all = args['conf_all']
    dir_working = realpath(conf_all['workdir'])

    # Directories #1: working directory has to exist
    if not isdir(dir_working):
        error('Directory "' + dir_working + '" does not exist!')
        sys.exit(ExitStatus.ERROR)

    # Directories #2: contest directory
    contest_obj = args['contest_obj']
    if conf_all['subdir_depth'] == 2:
        dir_contest = join(dir_working, contest_obj.ID)
        mkdir_safe(dir_contest, force=conf_all['force'])
    else:
        dir_contest = dir_working

    # Directories #3: problems directories
    problems_objs = args['problems_objs']
    if conf_all['subdir_depth'] >= 1:
        problems_dirs = {}
        for prob in problems_objs:
            problems_dirs[prob] = join(dir_contest, prob.ID)
            mkdir_safe(problems_dirs[prob], force=conf_all['force'])
    else:
        problems_dirs = {prob: dir_contest for prob in problems_objs}


def _command_show(**args):
    """Displays information about:
        - configuration (application default and user specific),
        - command line arguments.

    Expects labels for arguments to be contained in "args_text" argument.
    """

    # Prepare labels for arguments output
    args_labels_default = {
        'conf_all':      '1c --- Total config (overide 1b) .... ',
        'site_obj':      '3a --- Selected site processor ...... ',
        'contest_obj':   '3b --- Selected contest ............. ',
        'problems_objs': '3c --- Selected problems ............ ',
    }
    args_labels_verobse = {
        'conf_global':   '1a --- App default config ........... ',
        'conf_user':     '1b --- User files config (override 1a)',
        'sites':         '2  --- Available site processors .... '
    }

    args_labels = args_labels_default
    if hac.SETTINGS_VAR["verbose_output"]:
        args_labels.update(args_labels_verobse)

    # Prepare arguments for printing
    args_printable = {
        'conf_global': args['conf_global'],
        'conf_user': args['conf_user'],
        'conf_all': args['conf_all'],
        'sites': [dict(site) for site in args['sites']],
        'site_obj': dict(args['site_obj']),
        'contest_obj': dict(args['contest_obj']),
        'problems_objs': [dict(prob) for prob in args['problems_objs']]
    }

    # Construct dictionary with data to print
    data = {args_labels[key]: args_printable[key] for key in args_labels}

    # Pretty-print data
    printer = PrettyPrinter(indent=1, width=1)
    printer.pprint(data)


# Application commands collected in dictionary
app_commands = { "prep": _command_prep,
                 "show": _command_show }

