# -*- coding: utf-8 -*-
"""Useful miscellaneous functionality.
"""

# TODO crowd-source writing of this function
def match_site(sites, conf): #very-stupid matching now
    for s in sites:
        if(conf['location'].lower() in s.url.lower()):
            return s.url
    return sites[0].url

# Exactracting site with exact url
def get_site(sites, url):
    for s in sites:
        if(url == s.url):
            return s
    return None

