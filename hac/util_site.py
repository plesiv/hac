# -*- coding: utf-8 -*-
"""Utilities relating to sites.
"""

import sys

if sys.version_info.major == 2:
    from urlparse import urlparse
else:
    from urllib.parse import urlparse


# TODO crowd-source writing of this function
def match_site(sites, conf): #very-stupid matching now
    for site in sites:
        hostname = urlparse(conf['location']).hostname.lower()
        if(hostname in site.name.lower() or hostname in site.ID.lower()):
            return site.url
    return sites[0].url

# Exactracting site with exact url
def get_site(sites, url):
    for site in sites:
        if(url == site.url):
            return site
    return None

