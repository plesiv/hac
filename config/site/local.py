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
    # URL templates
    template_contest_url = "http://localhost/{0}"
    template_problem_suburl = "/{0}"

    # Regex patterns
    pattern_contest = re.compile(r"/(?P<contest>[^/]*)?(/(?P<problem>[^/]*))?")
    #   -> contest string has to start with '/'
    pattern_problem = re.compile(r"[^/]+")

    def __init__(self):
        self.url = "localhost"
        self.name = "Local"
        self.ID = "-"
        self.time_limit_ms = None
        self.memory_limit_kbyte = None
        self.source_limit_kbyte = None

    def match_contest(self, conf):
        url_path = urlparse(conf['location']).path or '/'
        tokens = SiteLocal.pattern_contest.search(url_path)
        contest_ID = tokens.group('contest') or 'contest'
        return SiteLocal.template_contest_url.format(contest_ID)

    def get_contest(self, url):
        url_path = urlparse(url).path
        assert url_path
        tokens = SiteLocal.pattern_contest.search(urlparse(url).path)
        cont_dict = {}
        cont_dict['url'] = url
        cont_dict['name'] = tokens.group('contest')
        assert cont_dict['name']
        cont_dict['ID'] = cont_dict['name']
        return Contest(**cont_dict)

    def match_problems(self, conf):
        contest_url = self.match_contest(conf)
        template_problem_url = contest_url + SiteLocal.template_problem_suburl

        urls = []
        # Match single problem from location member
        url_path = urlparse(conf['location']).path or '/'
        tokens = SiteLocal.pattern_contest.search(url_path)
        problem_ID = tokens.group('problem')
        if problem_ID:
            urls.append(template_problem_url.format(problem_ID))

        # Match potentially multiple problems from problems member
        for prob in conf['problems']:
            tokens = SiteLocal.pattern_problem.findall(prob)
            prob_ID = tokens and tokens[-1]
            if prob_ID:
                urls.append(template_problem_url.format(prob_ID))

        return urls

    def get_problems(self, urls):
        probs = []
        for url in urls:
            url_path = urlparse(url).path
            assert url_path
            tokens = SiteLocal.pattern_contest.search(urlparse(url).path)
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

