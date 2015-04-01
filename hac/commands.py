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
from pprint import PrettyPrinter

import hac


def _command_prep(**args):
    """Prepares the environment for selected problems.
    """
    print ("Command: prep")

def _command_show(**args):
    """Displays information about:
        - configuration (application default and user specific),
        - command line arguments.

    Expects labels for arguments to be contained in "args_text" argument.
    """

    # Prepare labels for arguments output
    args_labels_default = {
        'conf_all':      '1c --- Total configuration      (overrides 1b)',
        'sites':         '2  --- Available site processors              ',
        'site_obj':      '3a --- Selected site processor                ',
        'contest_obj':   '3b --- Selected contest                       ',
        'problems_objs': '3c --- Selected problems                      ',
    }
    args_labels_verobse = {
        'conf_global':   '1a --- App default configuration',
        'conf_user':     '1b --- User files configuration (overrides 1a)'
    }

    args_labels = args_labels_default
    if hac.VERBOSE_OUTPUT:
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

