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
from hac.parse_cli import cli_parser
from hac.parse_config import config_parser
from hac.util_common import dict_override, list_reduce, mainargs_index, error
from hac.util_data import plugin_collect, plugin_match_site


def main(args=sys.argv[1:]):
    """Execution flow of the main function:

    1) get configuration (priorities: default < local < cli)
    2) branch according to command (prep, show)
    """

    # -- Discover pluggins and templates -------------------------------------
    # Discover site-processor plugins (user-defined and default)
    sites = plugin_collect(DataType.SITE)


    # -- Read configuration files --------------------------------------------
    # Get default application configuration
    global_config_file = os.path.join(
        hac.SETTINGS_VAR["app_root_dir"],
        hac.SETTINGS_CONST["config_app_path"],
        hac.SETTINGS_CONST["config_filename"])
    assert os.path.exists(global_config_file)
    env_global = config_parser.parse_args(['@' + global_config_file])
    conf_global = vars(env_global)

    # Get user specifirc configuration
    user_config_file = os.path.join(
        hac.SETTINGS_CONST["config_user_path"],
        hac.SETTINGS_CONST["config_filename"])

    if os.path.exists(user_config_file):
        env_user = config_parser.parse_args(['@' + user_config_file])
        # Resolve configuration read from files
        conf_user = dict_override(conf_global, vars(env_user))
    else:
        conf_user = conf_global

    # -- Custom CLI handling -------------------------------------------------
    # Show help and exit when no arguments given.
    if len(args) == 0:
        cli_parser.print_help()
        sys.exit(ExitStatus.ERROR)

    # When no command given, use default from configuration files
    margs_ind = mainargs_index(args)
    if (margs_ind == len(args)) or (args[margs_ind] not in app_commands):
        args.insert(margs_ind, conf_user["command"])

    # When no location given (application command is the last argument)
    if (len(args) == margs_ind + 1) and (args[margs_ind] in app_commands):
        error("No CONTEST / PROBLEM given!")
        sys.exit(ExitStatus.ERROR)

    # Parse CLI arguments and resolve with respect to configuration files
    #from pudb import set_trace; set_trace()
    env_cli = cli_parser.parse_args(args=args)
    if env_cli:
        conf_all = dict_override(conf_user, vars(env_cli))
    else:
        conf_all = conf_user

    # -- Normalization of input/config ---------------------------------------
    # Reduce lang, runner lists and extract problems
    conf_all["lang"] = list_reduce(conf_all["lang"])
    conf_all["runner"] = list_reduce(conf_all["runner"])
    conf_all["problems"] = conf_all["problems"][0]

    # Normalize location member (should be URL)
    if not conf_all['location'].startswith('http://') and \
       not conf_all['location'].startswith('https://'):
        conf_all['location'] = 'http://' + conf_all['location']

    # -- Retrieve contest and problem info -----------------------------------
    # NOTE: Done in two steps for consistency and testability
    # 1) Match site, retrieve site-url
    site_url = plugin_match_site(sites, conf_all)
    # 2) Extract site object
    site_matched = [site for site in sites if site_url == site.url]
    assert site_matched
    site_obj = site_matched[0]

    # Use web-site processor to get contest data
    contest_url = site_obj.match_contest(conf_all)
    contest_obj = site_obj.get_contest(contest_url)

    # Use web-site processor to get problems data
    problems_urls = site_obj.match_problems(conf_all)
    problems_objs = site_obj.get_problems(problems_urls)

    # -- Execute command (e.g. prepare environment for problems )-------------
    assert conf_all["command"] in app_commands

    # TODO: adjust verbosity according to settings
    hac.SETTINGS_VAR["verbose_output"] = False

    # Execute selected command with all relevant information
    app_commands[conf_all["command"]](
        conf_global = conf_global,
        conf_user = conf_user,
        conf_all = conf_all,
        sites = sites,
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

