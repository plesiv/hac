# -*- coding: utf-8 -*-

import re
import sys
from hac.data import ISite, Contest, Problem

if sys.version_info.major == 2:
    from urlparse import urlparse
else:
    from urllib.parse import urlparse

from lxml import html
import requests


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

        # Fetch data from web.
        page = requests.get(url)
        tree = html.fromstring(page.text)
        extr = tree.xpath(SiteCodeforces.xpath_cont_name)
        cont.name = (extr and str(extr[0])) or "< no name >"

        return cont


    def match_problems(self, conf):
        problem_url_template = self.match_contest(conf) + "/problem/{0}"
        rx1= r".*([A-Za-z])"
        rx2= r".*\D+(\d+)"
        problems = []
        for pid in [conf["location"]] + conf["problems"]:
            mt1 = re.search(rx1, pid)
            prob = mt1 and mt1.group(1)
            if not mt1:
                mt2 = re.search(rx2, pid)
                prob = mt2 and mt2.group(1)
            if prob:
                problems.append(problem_url_template.format(prob))
        return problems

    def get_problems(self, url):
        return "Codeforces:get_problems"

