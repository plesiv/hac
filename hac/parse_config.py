# -*- coding: utf-8 -*-
"""Parsing configuration files.
"""
import argparse


class ParserConfig(argparse.ArgumentParser):
    """Class defining parsers for configuration files. Ignores lines starting
    with '#', and parses all other lines as if they were given on CLI.
    """
    def convert_arg_line_to_args(self, arg_line):
        if len(arg_line) > 0 and arg_line[0] == '#':
            return
        for arg in arg_line.split():
            if not arg.strip():
                continue
            yield arg


def get_bare_config_parser():
    """Returns bare parser for configuration files. Arguments should be added
    to parser manually.
    """
    return ParserConfig(fromfile_prefix_chars='@')

