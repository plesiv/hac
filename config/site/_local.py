# -*- coding: utf-8 -*-

import sys
import re
from hac.data import ISite, Contest, Problem

if sys.version_info.major == 2:
    from urlparse import urlparse
else:
    from urllib.parse import urlparse


class SiteLocal(ISite):
    """Local site.
    """
    # URL templates.
    url_temp_cont = "http://localhost/{0}"
    url_subtemp_prob = "/{0}"

    # Regex patterns.
    patt_contest = re.compile(r"/(?P<contest>[^/]*)?(/(?P<problem>[^/]*))?")
    patt_problem = re.compile(r"[^/]+")


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
        tokens = SiteLocal.patt_contest.search(loc_path)
        contest_ID = tokens.group('contest') or 'contest'
        return SiteLocal.url_temp_cont.format(contest_ID)


    def get_contest(self, url):
        """Creates contest object identified by the given URL.
        """
        url_path = urlparse(url).path
        assert url_path
        tokens = SiteLocal.patt_contest.search(url_path)
        cont_dict = {}
        cont_dict['url'] = url
        cont_dict['name'] = tokens.group('contest')
        assert cont_dict['name']
        cont_dict['ID'] = cont_dict['name']
        return Contest(**cont_dict)


    def match_problems(self, conf):
        """Extracts problems data from conf and generates list of canonic URLs
        identifying those problems.
        """
        url_cont = self.match_contest(conf)
        url_temp_prob = url_cont + SiteLocal.url_subtemp_prob

        urls = []
        # Match single problem from 'location'.
        loc_path = urlparse(conf['location']).path or '/'
        tokens = SiteLocal.patt_contest.search(loc_path)
        problem_ID = tokens.group('problem')
        if problem_ID:
            urls.append(url_temp_prob.format(problem_ID))

        # Match potentially multiple problems from 'problems'.
        for prob in conf['problems']:
            tokens = SiteLocal.patt_problem.findall(prob)
            prob_ID = tokens and tokens[-1]
            if prob_ID:
                urls.append(url_temp_prob.format(prob_ID))

        return urls


    def get_problems(self, urls):
        """Creates problems' objects identified by the provided list of URLs.
        """
        probs = []
        for url in urls:
            url_path = urlparse(url).path
            assert url_path
            tokens = SiteLocal.patt_contest.search(url_path)
            prob_dict = {}
            prob_dict['url'] = url
            prob_dict['name'] = tokens.group('problem')
            assert prob_dict['name']
            prob_dict['ID'] = prob_dict['name']
            prob_dict['time_limit_ms'] = self.time_limit_ms
            prob_dict['memory_limit_kbyte'] = self.memory_limit_kbyte
            prob_dict['source_limit_kbyte'] = self.source_limit_kbyte
            probs.append(Problem(**prob_dict))
        return probs

