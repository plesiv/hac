# -*- coding: utf-8 -*-
"""Parsing configuration files.
"""
import argparse

from hac.parse_common import common_args, add_packed_arguments


# TODO Document HAC_CONFIG_DIR var
# TODO Windows compat
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

