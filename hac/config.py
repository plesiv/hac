# -*- coding: utf-8 -*-
"""Parsing configuration files.
"""
import os
import argparse

from hac.parse import common_args, add_packed_arguments


# Application configuration constants.
DEFAULTS = {
    "config_filename": "hacrc",
    "config_app_dirpath": "config",
    "config_user_dirpath": os.environ.get('HAC_CONFIG_DIR',
        os.path.expanduser('~/.config/hac')),
    "sites_dirname": "site"
}

# Custom configuration-file parser, ignores lines starting with '#'
class ConfigParser(argparse.ArgumentParser):

    def convert_arg_line_to_args(self, arg_line):
        if len(arg_line) > 0 and arg_line[0] == '#':
            return
        for arg in arg_line.split():
            if not arg.strip():
                continue
            yield arg


# Construct configuration-file parser with common arguments.
config_parser = ConfigParser(fromfile_prefix_chars='@')
add_packed_arguments(config_parser, common_args)

# TODO Windows compat
