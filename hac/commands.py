# -*- coding: utf-8 -*-
"""Commands implementation.
"""
#conf_global
#conf_user
#conf_all
#sites
#site_obj
#contest_obj
#problems_objs

def _command_prep():
    print ("Command: prep")

def _command_show():
    print ("Command: show")

# Application commands collected in dictionary
app_commands = { "prep": _command_prep,
                 "show": _command_show }

