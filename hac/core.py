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
from hac.parse_config import get_bare_parser_config
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

    # -- Discover plug-ins and templates -------------------------------------
    plugin_langs = plugin_collect(DataType.LANG)     # Get language-templates
    plugin_runners = plugin_collect(DataType.RUNNER) # Get runners
    plugin_sites = plugin_collect(DataType.SITE)     # Get site-processors

    # Helper data. If available_langs == ['cpp.0', 'cpp.1', 'py.15']), then
    # choice_langs == ['cpp', 'cpp.0', 'cpp.1', 'py', 'py.15']
    available_langs = plugin_langs.keys()
    sep_langs = hac.SETTINGS_CONST['plugin_temp_sep'][DataType.LANG]
    choice_langs = choice_generate(available_langs, sep_langs)

    available_runners = plugin_runners.keys()
    sep_runners = hac.SETTINGS_CONST['plugin_temp_sep'][DataType.RUNNER]
    choice_runners = choice_generate(available_runners, sep_runners)


    # -- Construct parsers (uses data from plug-ins) -------------------------
    # Get parser arguments.
    pargs_pack_common = get_pargs_pack_common(
            choice_langs = choice_langs,
            choice_runners = choice_runners,
    )
    pargs_pack_cli = get_pargs_pack_cli()

    # Add arguments to parsers.
    parser_config = get_bare_parser_config()
    parser_cli = get_bare_parser_cli()

    pargs_packed_add(parser_config, pargs_pack_common)
    pargs_packed_add(parser_cli, pargs_pack_common)
    pargs_packed_add(parser_cli, pargs_pack_cli)


    # -- Get configuration from files ----------------------------------------
    # Get default application configuration.
    global_config_file = os.path.join(
        hac.SETTINGS_VAR["app_root_dir"],
        hac.SETTINGS_CONST["config_app_path"],
        hac.SETTINGS_CONST["config_filename"])
    assert os.path.exists(global_config_file)
    env_global = parser_config.parse_args(['@' + global_config_file])
    conf_global = vars(env_global)

    # Get user specific configuration.
    user_config_file = os.path.join(
        hac.SETTINGS_CONST["config_user_path"],
        hac.SETTINGS_CONST["config_filename"])

    if os.path.exists(user_config_file):
        env_user = parser_config.parse_args(['@' + user_config_file])
        # Resolve configuration read from files
        conf_user = dict_override(conf_global, vars(env_user))
    else:
        conf_user = conf_global


    # -- Get configuration from CLI ------------------------------------------
    # Show help and exit when no arguments given.
    if len(args) == 0:
        parser_cli.print_help()
        sys.exit(ExitStatus.ERROR)

    # When no command given, use default from configuration files.
    margs_ind = mainargs_index(args)
    if (margs_ind == len(args)) or (args[margs_ind] not in app_commands):
        args.insert(margs_ind, conf_user["command"])

    # When no location given, notify user.
    if (len(args) == margs_ind + 1) and (args[margs_ind] in app_commands):
        error("No CONTEST / PROBLEM given!")
        sys.exit(ExitStatus.ERROR)

    # Parse CLI arguments and resolve with respect to configuration files
    env_cli = parser_cli.parse_args(args=args)
    if env_cli:
        conf_all = dict_override(conf_user, vars(env_cli))
    else:
        conf_all = conf_user


    # -- Normalize aggregated configuration ----------------------------------
    # Reduce lang, runner lists and extract problems
    conf_all["lang"] = list_reduce(conf_all["lang"])
    conf_all["runner"] = list_reduce(conf_all["runner"])
    conf_all["problems"] = conf_all["problems"][0]

    # Normalize lang and runner lists
    # If available_langs == ['cpp.0', 'cpp.1', 'py.15'], then
    # conf_all["runner"] == ['cpp.0', 'cpp.1', 'py'] is normalized to
    # ['cpp.0', 'py.15']
    conf_all["lang"] = choice_normal(conf_all["lang"], available_langs)
    conf_all["runner"] = choice_normal(conf_all["runner"], available_runners)

    # Normalize location member (should be URL)
    if not conf_all['location'].startswith('http://') and \
       not conf_all['location'].startswith('https://'):
        conf_all['location'] = 'http://' + conf_all['location']


    # NOTE: Following tasks each done in two steps for testability.
    # -- Match site processor ------------------------------------------------
    # 1) Match site, retrieve site-url
    site_url = plugin_match_site(plugin_sites, conf_all)
    # 2) Extract site object
    site_matched = [site for site in plugin_sites if site_url == site.url]
    assert site_matched
    site_obj = site_matched[0]


    # -- Retrieve contest and problem info -----------------------------------
    # Use web-site processor to get contest data
    contest_url = site_obj.match_contest(conf_all)
    contest_obj = site_obj.get_contest(contest_url)

    # Use web-site processor to get problems data
    problems_urls = site_obj.match_problems(conf_all)
    problems_objs = site_obj.get_problems(problems_urls)

    # -- Execute selected command --------------------------------------------
    assert conf_all["command"] in app_commands

    # TODO: adjust verbosity according to settings
    hac.SETTINGS_VAR["verbose_output"] = False

    # Execute selected command with all relevant information
    app_commands[conf_all["command"]](
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
    # TODO #5 prep command

    # TODO create whole directory structure for dir that doesn't exist
    # TODO resolve paths got from user (~ etc.)
    # TODO configurable name of directories for site (ID or NAME)
    # TODO configurable name of directories for contest (ID or NAME)
    # TODO configurable name of directories for problem (ID or NAME)
    # TODO quiet mode -> don't show errors
    # TODO support for site-specific templates and multiple templates per language

