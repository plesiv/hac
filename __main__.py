#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The main entry point. Invoke as 'python hac'.
"""
import sys
from os.path import dirname, realpath

import hac


if __name__ == '__main__':
    # Initialize global application settings
    hac.init_settings()
    hac.SETTINGS_VAR["app_root_dir"] = dirname(realpath(__file__))

    # Start the application
    from hac.core import main
    sys.exit(main())

