# -*- coding: utf-8 -*-
"""This module provides the main functionality.
"""
import os
import sys
import textwrap

from hac import DEFAULT_CONFIGS, ExitStatus
from hac.commands import app_commands
from hac.parse_cli import cli_parser
from hac.parse_config import config_parser
from hac.util_common import error
from hac.util_site import plugin_sites_collect, site_match, site_get


def dict_override(a, b):
    """Overriding dictionary values.

    Values in second dictionary override the values in the first one (except
    when relevant value in second dictionary is None).

    >>> dict_override({'a': 1,'b': 2}, {'a': 3,'b': None}) == {'a': 3,'b': 2}
    True

    >>> dict_override({'a': 3,'b': None}, {'a': 1,'b': 2}) == {'a': 1,'b': 2}
    True
    """
    res = {}
    for key in (set(a.keys()) | set(b.keys())):
        if (key in b) and (b[key] != None):
            res[key] = b[key]
        else:
            res[key] = a[key]
    return res


def reduce_list(a):
    """Reduces provided list in two steps:
        1) removes all elements from list that appear prior to any 'no' element,
        2) removes duplicates and sorts elements.

    >>> reduce_list(['cpp', 'no', 'php', 'py', 'php', 'py'])
    ['php', 'py']

    >>> reduce_list(['cpp', 'no', 'php', 'py', 'php', 'no', 'py', 'cpp'])
    ['cpp', 'py']
    """
    b = list(reversed(a))
    if "no" in b:
        ind = b.index("no")
        del b[ind:]
    return sorted(set(b))


def remove_optionals(a):
    """Removes optional arguments that precede mandatory arguments.

    >>> remove_optionals(['--cpp', '-no', 'php', '-t', 'py'])
    ['php', '-t', 'py']

    >>> remove_optionals(['--cpp', '-no'])
    []
    """
    b = a[:]
    while(len(b)>0 and b[0].startswith("-")):
        del b[0]
    return b


def main(args=sys.argv[1:]):
    """Execution flow of the main function:

    1) get configuration (priorities: default < local < cli)
    2) branch according to command (prep, show)
    """

    # -- Configuration files -------------------------------------------------
    # Get default application configuration
    global_config_file = os.path.join(
        DEFAULT_CONFIGS["config_app_dirpath"],
        DEFAULT_CONFIGS["config_filename"])
    assert os.path.exists(global_config_file)
    env_global = config_parser.parse_args(['@' + global_config_file])
    conf_global = vars(env_global)

    # Get user specifirc configuration
    user_config_file = os.path.join(
        DEFAULT_CONFIGS["config_user_dirpath"],
        DEFAULT_CONFIGS["config_filename"])

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
    rargs = remove_optionals(args)
    if (len(rargs) < 1) or (rargs[0] not in app_commands):
        args.insert(0, conf_user["command"])

    # When no location given
    if (len(rargs) == 1) and (rargs[0] in app_commands):
        error("No CONTEST / PROBLEM given!")
        sys.exit(ExitStatus.ERROR)

    # Parse CLI arguments and resolve with respect to configuration files
    env_cli = cli_parser.parse_args(args=args)
    if env_cli:
        conf_all = dict_override(conf_user, vars(env_cli))
    else:
        conf_all = conf_user

    # -- Normalization of input/config ---------------------------------------
    # Reduce lang, runner lists and extract problems
    conf_all["lang"] = reduce_list(conf_all["lang"])
    conf_all["runner"] = reduce_list(conf_all["runner"])
    conf_all["problems"] = conf_all["problems"][0]

    # Normalize location member (should be URL)
    if not conf_all['location'].startswith('http://') and \
       not conf_all['location'].startswith('https://'):
        conf_all['location'] = 'http://' + conf_all['location']

    # -- Retrieve contest and problem info -----------------------------------
    # Discover site-processor plugins (user-defined and default)
    sites = plugin_sites_collect()

    # NOTE: Done in two steps for consistency and testability
    # 1) Match site, retrieve site-url
    site_url = site_match(sites, conf_all)
    # 2) Extract site object
    site_obj = site_get(sites, site_url)

    # Use web-site processor to get contest data
    contest_url = site_obj.match_contest(conf_all)
    contest_obj = site_obj.get_contest(contest_url)

    # Use web-site processor to get problems data
    problems_urls = site_obj.match_problems(conf_all)
    problems_objs = site_obj.get_problems(problems_urls)

    # -- Execute command (e.g. prepare environment for problems )-------------

    # TODO to-logging
    import pprint; pp = pprint.PrettyPrinter(indent=4)
    print("USER"); pp.pprint(conf_user)
    print("ALL"); pp.pprint(conf_all)

    # TODO to-logging
    print("Site: {0}".format(site_obj.url))
    print("Contest URL: {0}".format(contest_url))
    for p in problems_urls:
        print("Problems URLs: {0}".format(p))

    # TODO #1 web page-information DS
    # TODO #2 web-parsing DS and processor
    # TODO #3 decipher which problems to fetch (URL, other) [when no selected,
    #         get all]
    # TODO #4 show command
    # TODO #5 prep command

    # TODO create whole directory structure for dir that doesn't exist
    # TODO resolve paths got from user (~ etc.)
    # TODO configurable name of directories for site (ID or NAME)
    # TODO configurable name of directories for contest (ID or NAME)
    # TODO configurable name of directories for problem (ID or NAME)
    # TODO quiet mode -> don't show errors
    # TODO support for site-specific templates and multiple templates per language

