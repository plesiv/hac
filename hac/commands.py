# -*- coding: utf-8 -*-
"""Implementation of application commands.

Commands can access following entries from dictionary "args":

    - conf_global: dictionary containing default application settings,
    - conf_user: dictionary containing user settings from configuration files
                 (override default application settings),
    - conf_all: dictionary containing command-line settings (override user
                settings from configuration files),
    - plugin_langs: dictionary mapping language template designation to the
                    contents of language template file
    - plugin_runners: dictionary (of dictionaries) mapping runner templates
                      designation to the dictionary which map language template
                      designation to the contents of processed runner template
                      file
    - plugin_sites: list of all available site-processors (objects whose classes
             inherit from hac.data.ISite),
    - site_obj: selected site-processor (object whose class inherit from
                hac.data.ISite),
    - contest_obj: selected contest (instance of hac.data.Contest),
    - problems_objs: list of selected problems (instances of hac.data.Problem).
"""
import sys
import os
from os.path import realpath, exists, isdir, join
from pprint import PrettyPrinter

import hac
from hac import DataType, ExitStatus
from hac.util_common import warn, error, safe_mkdir, safe_fwrite


def _command_prep(**args):
    """Prepares the environment for selected problems.

    This command is idempotent irrespective of the "--force" switch.
    """
    conf_all = args['conf_all']
    dir_working = realpath(conf_all['workdir'])

    # 1) Working directory has to exist.
    if not isdir(dir_working):
        error('Directory "' + dir_working + '" does not exist!')
        sys.exit(ExitStatus.ERROR)

    # 2) Establish contest directory.
    contest_obj = args['contest_obj']
    if conf_all['subdir_depth'] == 2:
        dir_contest = join(dir_working, contest_obj.ID)
        safe_mkdir(dir_contest, force=conf_all['force'])
    else:
        dir_contest = dir_working

    # Proceed if there exists directory hierachy until this point
    if (isdir(dir_contest)):

        # 3) Establish problems directories.
        problems_objs = args['problems_objs']
        if conf_all['subdir_depth'] >= 1:
            problems_dirs = {}
            for prob in problems_objs:
                problems_dirs[prob] = join(dir_contest, prob.ID)
                safe_mkdir(problems_dirs[prob], force=conf_all['force'])
        else:
            problems_dirs = {prob: dir_contest for prob in problems_objs}

        plugin_langs = args['plugin_langs']
        selected_langs = conf_all['lang']
        sep_langs = hac.SETTINGS_CONST['plugin_temp_sep'][DataType.LANG]

        plugin_runners = args['plugin_runners']
        selected_runners = conf_all['runner']
        sep_runners = hac.SETTINGS_CONST['plugin_temp_sep'][DataType.RUNNER]

        # 4) Create language and runner templates.
        # For each problem ...
        for prob in problems_objs:
            if isdir(problems_dirs[prob]):
                problem_path = join(problems_dirs[prob], prob.ID)

                # ... create every combiantion of selected runner/language.
                for runn in selected_runners:
                    for lang in selected_langs:
                        assert sep_runners in runn
                        assert runn in plugin_runners
                        assert sep_langs in lang
                        assert lang in plugin_langs

                        runn_ext = runn.split(sep_runners)[0]
                        lang_ext = lang.split(sep_langs)[0]

                        if lang_ext in plugin_runners[runn]:
                            runner_file = problem_path + os.extsep + \
                                          lang_ext + os.extsep + runn_ext
                            safe_fwrite(runner_file,
                                        plugin_runners[runn][lang_ext],
                                        force=conf_all['force'])
                            lang_file = problem_path + os.extsep + lang_ext
                            safe_fwrite(lang_file, plugin_langs[lang],
                                        force=conf_all['force'])
                        else:
                            warn("Combination [{0}/{1}] does not exist!"
                                  .format(runn, lang_ext))


def _command_show(**args):
    """Displays information about:
        - configuration (application default and user specific),
        - command line arguments.

    Expects labels for arguments to be contained in "args_text" argument.
    """

    # Prepare labels for arguments output
    args_labels_default = {
        'conf_all':       '1c --- Total config (overide 1b) .... ',
        'site_obj':       '3a --- Selected site processor ...... ',
        'contest_obj':    '3b --- Selected contest ............. ',
        'problems_objs':  '3c --- Selected problems ............ ',
    }
    args_labels_verobse = {
        'conf_global':    '1a --- App default config ........... ',
        'conf_user':      '1b --- User files config (override 1a)',
        'plugin_langs':   '2a --- Available language templates . ',
        'plugin_runners': '2b --- Available runner templates ... ',
        'plugin_sites':   '2c --- Available site processors .... ',
    }

    args_labels = args_labels_default
    if hac.SETTINGS_VAR["verbose_output"]:
        args_labels.update(args_labels_verobse)

    # Prepare arguments for printing
    args_printable = {
        'conf_global': args['conf_global'],
        'conf_user': args['conf_user'],
        'conf_all': args['conf_all'],
        'plugin_langs': args['plugin_langs'].keys(),
        'plugin_runners': [], #TODO show all languages for runner
        'plugin_sites': [dict(site) for site in args['plugin_sites']],
        'site_obj': dict(args['site_obj']),
        'contest_obj': dict(args['contest_obj']),
        'problems_objs': [dict(prob) for prob in args['problems_objs']]
    }
    #TODO language x runner matrix

    # Construct dictionary with data to print
    data = {args_labels[key]: args_printable[key] for key in args_labels}

    # Pretty-print data
    printer = PrettyPrinter(indent=1, width=1)
    printer.pprint(data)


# Application commands collected in dictionary
app_commands = { "prep": _command_prep,
                 "show": _command_show }

