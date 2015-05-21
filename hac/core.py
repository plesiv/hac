# -*- coding: utf-8 -*-
"""This module provides the main functionality.
"""
import os
import sys
import textwrap
from os.path import dirname, realpath

import hac
from hac import DataType, ExitStatus
from hac.commands import app_commands
from hac.parse_common import get_pargs_pack_common, pargs_packed_add
from hac.parse_config import get_bare_config_parser
from hac.parse_cli import get_pargs_pack_cli, get_bare_parser_cli
from hac.util_common import error, dict_override, list_reduce, mainargs_index,\
    choice_generate, choice_normal
from hac.util_data import plugin_collect, plugin_match_site


def main(args=sys.argv[1:]):
    """Execution flow of the main function:

    #TODO Execution flow correct
    ... discover plugins
    ... get configuration (priorities: default < local < cli)
    ... branch according to command (prep, show)
    """

    # -- PLUGIN-SYSTEM -------------------------------------------------------
    # Discover plug-ins and templates.
    plugin_langs = plugin_collect(DataType.LANG)     # Get language-templates
    plugin_runners = plugin_collect(DataType.RUNNER) # Get runners
    plugin_sites = plugin_collect(DataType.SITE)     # Get site-processors

    # Auxiliary data. If
    #   available_langs == ['cpp.0', 'cpp.1', 'py.15']), then
    #   choice_langs    == ['cpp', 'cpp.0', 'cpp.1', 'py', 'py.15']
    available_langs = plugin_langs.keys()
    sep_langs = hac.SETTINGS_CONST['plugin_temp_sep'][DataType.LANG]
    choice_langs = choice_generate(available_langs, sep_langs)

    available_runners = plugin_runners.keys()
    sep_runners = hac.SETTINGS_CONST['plugin_temp_sep'][DataType.RUNNER]
    choice_runners = choice_generate(available_runners, sep_runners)


    # -- READ CONFIG FILES ---------------------------------------------------
    # Construct and use parsers (utilize data from plug-ins).

    # Get parser arguments.
    pargs_pack_common = get_pargs_pack_common(
            choice_langs = choice_langs,
            choice_runners = choice_runners,
    )
    pargs_pack_cli = get_pargs_pack_cli()

    # Add arguments to parsers.
    parser_config = get_bare_config_parser()
    parser_cli = get_bare_parser_cli()

    pargs_packed_add(parser_config, pargs_pack_common)
    pargs_packed_add(parser_cli, pargs_pack_common)
    pargs_packed_add(parser_cli, pargs_pack_cli)

    # Get default application configuration (from files).
    global_config_file = os.path.join(
        hac.SETTINGS_VAR["app_root_dir"],
        hac.SETTINGS_CONST["config_app_path"],
        hac.SETTINGS_CONST["config_filename"])
    assert os.path.exists(global_config_file)
    env_global = parser_config.parse_args(['@' + global_config_file])
    conf_global = vars(env_global)

    # Get user specific configuration (from files).
    user_config_file = os.path.join(
        hac.SETTINGS_CONST["config_user_path"],
        hac.SETTINGS_CONST["config_filename"])

    if os.path.exists(user_config_file):
        env_user = parser_config.parse_args(['@' + user_config_file])
        # Resolve configuration read from files
        conf_user = dict_override(conf_global, vars(env_user))
    else:
        conf_user = conf_global


    # -- READ CLI ------------------------------------------------------------
    # Special handling of CLI arguments.

    # -> Print help message and exit if:
    #     - no arguments given OR
    #     - "-h" or "--help" is given as optional argument
    if (len(args) == 0) or any([o in args for o in ("-h", "--help")]):
         parser_cli.print_help()
         sys.exit(ExitStatus.ERROR)
 
    # -> Print application version and exit if:
    #     - "-V" or "--version" is given as optional argument
    if any([o in args for o in ("-V", "--version")]):
        print(
        "hac v{0}, License {1}, Copyright (C) 2014-2015 {2}".format(
                                    hac.__version__,
                                    hac.__license__,
                                    hac.__author__))
        sys.exit(ExitStatus.ERROR)

    # -> Use default command (from configuration files) if:
    #     - no command given
    margs_ind = mainargs_index(args)
    if (margs_ind == len(args)) or (args[margs_ind] not in app_commands):
        args.insert(margs_ind, conf_user["command"])

    # -> Notify user and exit if:
    #     - no location (legal CONTEST / PROBLEM) given
    if (len(args) == margs_ind + 1) and (args[margs_ind] in app_commands):
        error("No CONTEST / PROBLEM given!")
        sys.exit(ExitStatus.ERROR)


    # Regular handling of CLI arguments. Parse CLI arguments and resolve with
    # respect to configuration files.
    env_cli = parser_cli.parse_args(args=args)
    if env_cli:
        conf_all = dict_override(conf_user, vars(env_cli))
    else:
        conf_all = conf_user


    # -- PROCESS CONFIG / CLI ------------------------------------------------
    # Normalize aggregated configuration.

    # Reduce lang, runner lists and extract problems.
    conf_all["lang"] = list_reduce(conf_all["lang"])
    conf_all["runner"] = list_reduce(conf_all["runner"])
    conf_all["problems"] = conf_all["problems"][0]

    # Normalize lang and runner lists.
    # If available_langs == ['cpp.0', 'cpp.1', 'py.15'], then
    # conf_all["runner"] == ['cpp.0', 'cpp.1', 'py'] is normalized to
    # ['cpp.0', 'py.15']
    conf_all["lang"] = choice_normal(conf_all["lang"], available_langs)
    conf_all["runner"] = choice_normal(conf_all["runner"], available_runners)

    # Normalize location member (should be URL).
    if not conf_all['location'].startswith('http://') and \
       not conf_all['location'].startswith('https://'):
        conf_all['location'] = 'http://' + conf_all['location']


    # -- PROCESS AND PREPARE DATA --------------------------------------------
    # NOTE: Matching done in two steps for testability.

    # Get site processor:
    #     1) Match site-processor, gets url of matched processor.
    site_url = plugin_match_site(plugin_sites, conf_all)
    #     2) Extract site-processor.
    site_matched = [site for site in plugin_sites if site_url == site.url]
    assert site_matched
    site_obj = site_matched[0]

    # Get contest data (utilize web-site processor).
    contest_url = site_obj.match_contest(conf_all)
    contest_obj = site_obj.get_contest(contest_url)

    # Get problems data (utilize web-site processor).
    problems_urls = site_obj.match_problems(conf_all)
    problems_objs = site_obj.get_problems(problems_urls)


    # -- EXECUTE -------------------------------------------------------------
    assert conf_all["command"] in app_commands

    # Execute selected command with all relevant information
    return app_commands[conf_all["command"]](
        conf_global = conf_global,
        conf_user = conf_user,
        conf_all = conf_all,
        plugin_langs = plugin_langs,
        plugin_runners = plugin_runners,
        plugin_sites = plugin_sites,
        site_obj = site_obj,
        contest_obj = contest_obj,
        problems_objs = problems_objs)

    # TODO problems selectable by number and letter
    # TODO notify about non-existence of the given problem
    # TODO #3 decipher which problems to fetch (URL, other) [when no selected,
    #         get all]
    # TODO resolve paths got from user (~ etc.)
    # TODO configurable name of directories for site (ID or NAME)
    # TODO configurable name of directories for contest (ID or NAME)
    # TODO configurable name of directories for problem (ID or NAME)

