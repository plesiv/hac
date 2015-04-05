# -*- coding: utf-8 -*-

import re
import sys
import requests
from lxml import html

if sys.version_info.major == 2:
    from urlparse import urlparse
else:
    from urllib.parse import urlparse

from hac.data import ISite, Contest, Problem
from hac.util_common import warn
from hac.util_data import RequestsCache


class SiteCodeforces(ISite):
    """Codeforces site processor.
    """

    # URL templates.
    url_temp_cont = "http://codeforces.com/contest/{0}"
    url_temp_s_prob = "/problem/{0}"

    # Regex patterns.
    patt_cont = re.compile(r"/(contest/)?(?P<CONT>[^/]*)?(/(problem/)?(?P<PROB>[^/]*))?")
    patt_prob = re.compile(r"[^/]+")

    # Xpath selectors.
    xpath_cont_name = '//*[@id="sidebar"]//a[contains(@href, "contest")]/text()'
    xpath_probs_IDs = '//*[@id="content"]//*[@class="id"]//a/text()'

    # Proxy for HTTP requests (handles request caching).
    proxy = RequestsCache()

    # Helper methods
    @staticmethod
    def ID_prob_encode(id_in):
        """Codeforces problems are encoded with uppercase latin letters. This
        function handles conversion from:

            - lowercase latin letters,
            - numbers.

        >>> SiteCodeforces.ID_prob_encode('A')
        'A'

        >>> SiteCodeforces.ID_prob_encode('z')
        'Z'

        >>> SiteCodeforces.ID_prob_encode('3')
        'C'

        >>> SiteCodeforces.ID_prob_encode('.') is None
        True
        """
        if isinstance(id_in, str):

            if id_in.isalpha() and len(id_in) == 1:
                return id_in.upper()

            if id_in.isdigit():
                id_out = chr(ord('A') + int(id_in) - 1)
                if id_out.isalpha():
                    return id_out

        return None


    def __init__(self):
        self.url = "http://codeforces.com/"
        self.name = "Codeforces"
        self.ID = "codeforces"
        self.time_limit_ms = None
        self.memory_limit_kbyte = None
        self.source_limit_kbyte = 64


    def match_contest(self, conf):
        """Extracts contest data from conf and generates canonic URL
        identifying that contest.
        """
        loc_path = urlparse(conf['location']).path or '/'
        tokens = SiteCodeforces.patt_cont.search(loc_path)
        ID_cont = tokens.group('CONT') or 'contest'
        return SiteCodeforces.url_temp_cont.format(ID_cont)


    def get_contest(self, url):
        """Fetches data from the contest URL and creates contest object
        identified by that URL.
        """
        url_path = urlparse(url).path
        assert url_path
        cont = Contest()
        cont.url = url
        tokens = SiteCodeforces.patt_cont.search(url_path)
        cont.ID = tokens.group('CONT')

        # Data from web:
        #   - contest name.
        page = SiteCodeforces.proxy.get(url)
        tree = html.fromstring(page.text)
        extr = tree.xpath(SiteCodeforces.xpath_cont_name)
        cont.name = (extr and str(extr[0])) or "< no name >"

        return cont


    def match_problems(self, conf):
        """Extracts problems data from conf and generates list of canonic URLs
        identifying those problems.
        """
        url_cont = self.match_contest(conf)
        url_temp_prob = url_cont + SiteCodeforces.url_temp_s_prob

        # Data from web:
        #   - available problem IDs.
        page = SiteCodeforces.proxy.get(url_cont)
        tree = html.fromstring(page.text)
        extr = tree.xpath(SiteCodeforces.xpath_probs_IDs)
        IDs_available = [ str(e.strip()) for e in extr ]

        IDs = []
        # Match single problem from 'location'.
        loc_path = urlparse(conf['location']).path or '/'
        tokens = SiteCodeforces.patt_cont.search(loc_path)
        ID_raw = tokens.group('PROB')
        ID_prob = SiteCodeforces.ID_prob_encode(ID_raw)
        if ID_prob:
            IDs.append(ID_prob)

        # Match potentially multiple problems from 'problems'.
        for prob in conf['problems']:
            tokens = SiteCodeforces.patt_prob.findall(prob)
            ID_raw = tokens and tokens[-1]
            ID_prob = SiteCodeforces.ID_prob_encode(ID_raw)
            if ID_prob:
                IDs.append(ID_prob)

        # Notify about selected but non-existant problems.
        urls = []
        for ID in IDs:
            if ID in IDs_available:
                urls.append(url_temp_prob.format(ID))
            else:
                warn('Problem "' + ID + '" does not exist!')

        return urls


    def get_problems(self, url):
        return "Codeforces:get_problems"

