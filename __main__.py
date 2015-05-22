#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2014-2015  Zoran Plesivčak <z@plesiv.com>
# This software is distributed under the terms of the GNU GPL version 2.

"""The main entry point. Invoke as 'python hac'.
"""
import sys
from os.path import dirname, realpath

import hac


if __name__ == '__main__':
    from hac.core import main
    sys.exit(main())

