# -*- coding: utf-8 -*-

import re
import sys

if sys.version_info.major == 2:
    from urlparse import urlparse
else:
    from urllib.parse import urlparse

from hac.data import ISite, Contest, Problem


class SiteLocal(ISite):
    """Local site processor.
    """

    # URL templates.
    url_temp_cont = "http://localhost/{0}"
    url_temp_s_prob = "/{0}"

    # Regex patterns.
    patt_cont = re.compile(r"/(?P<CONT>[^/]*)?(/(?P<PROB>[^/]*))?")
    patt_prob = re.compile(r"[^/]+")


    def __init__(self):
        self.url = "localhost"
        self.name = "Local"
        self.ID = "local"
        self.time_limit_ms = None
        self.memory_limit_kbyte = None
        self.source_limit_kbyte = None


    def match_contest(self, conf):
        """Extracts contest data from conf and generates canonic URL
        identifying that contest.
        """
        loc_path = urlparse(conf['location']).path or '/'
        tokens = SiteLocal.patt_cont.search(loc_path)
        ID_cont = tokens.group('CONT') or 'contest'
        return SiteLocal.url_temp_cont.format(ID_cont)


    def get_contest(self, url):
        """Creates contest object identified by the given URL.
        """
        url_path = urlparse(url).path
        assert url_path
        cont = Contest()
        cont.url = url
        tokens = SiteLocal.patt_cont.search(url_path)
        cont.ID = tokens.group('CONT')
        assert cont.ID
        cont.name = cont.ID
        return cont


    def match_problems(self, conf):
        """Extracts problems data from conf and generates list of canonic URLs
        identifying those problems.
        """
        url_cont = self.match_contest(conf)
        url_temp_prob = url_cont + SiteLocal.url_temp_s_prob

        urls = []
        # Match single problem from 'location'.
        loc_path = urlparse(conf['location']).path or '/'
        tokens = SiteLocal.patt_cont.search(loc_path)
        ID_prob = tokens.group('PROB')
        if ID_prob:
            urls.append(url_temp_prob.format(ID_prob))

        # Match potentially multiple problems from 'problems'.
        for prob in conf['problems']:
            tokens = SiteLocal.patt_prob.findall(prob)
            ID_prob = tokens and tokens[-1]
            if ID_prob:
                urls.append(url_temp_prob.format(ID_prob))

        return urls


    def get_problems(self, urls):
        """Creates problems' objects identified by the provided list of URLs.
        """
        probs = []
        for url in urls:
            prob = Problem()
            prob.url = url
            url_path = urlparse(url).path
            assert url_path
            tokens = SiteLocal.patt_cont.search(url_path)
            prob.ID = tokens.group('PROB')
            assert prob.ID
            prob.name = prob.ID
            prob.time_limit_ms = self.time_limit_ms
            prob.memory_limit_kbyte = self.memory_limit_kbyte
            prob.source_limit_kbyte = self.source_limit_kbyte
            probs.append(prob)
        return probs

