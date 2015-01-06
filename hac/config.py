# -*- coding: utf-8 -*-
"""Parsing configuration files.
"""
import os
import argparse

from hac.parse import common_args, add_packed_arguments


# Configuration in filesystem.
DEFAULT_CONFIG_DIR = "config"
USER_CONFIG_DIR = os.environ.get('HAC_CONFIG_DIR', os.path.expanduser('~/.config/hac'))
CONFIG_FILENAME = "hacrc"
# TODO Windows compat


# Custom parser, ignores lines starting with '#'
class ConfigParser(argparse.ArgumentParser):

    def convert_arg_line_to_args(self, arg_line):
        if len(arg_line) > 0 and arg_line[0] == '#':
            return
        for arg in arg_line.split():
            if not arg.strip():
                continue
            yield arg


# Construct configuration parser with common arguments.
config_parser = ConfigParser(fromfile_prefix_chars='@')
add_packed_arguments(config_parser, common_args)

