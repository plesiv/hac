# -*- coding: utf-8 -*-
"""Common utilities.
"""

import sys

# Printing to STDERR
def error(msg):
    sys.stderr.write("ERROR: " + msg + "\n")

