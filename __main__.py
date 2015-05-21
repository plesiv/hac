#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The main entry point. Invoke as 'python hac'.
"""
import sys
from os.path import dirname, realpath

import hac


if __name__ == '__main__':
    from hac.core import main
    sys.exit(main())

