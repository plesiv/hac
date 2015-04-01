#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The main entry point. Invoke as 'python hac'.
"""
import sys
from os.path import dirname, realpath

import hac
from hac.core import main


if __name__ == '__main__':
    # Initialize global application settings
    hac.init_settings()
    hac.HAC_ROOT_DIR = dirname(realpath(__file__))

    # Start the application
    sys.exit(main())

