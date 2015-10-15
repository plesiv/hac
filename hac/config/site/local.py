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

    >>> path1 = "/new-contest 43 3 5"
    >>> SiteLocal.pattern_contest.search(path1).group("PROBLEM") is None
    True

    >>> path2 = "/old-contest/52 24 2 2"
    >>> SiteLocal.pattern_contest.search(path2).group("CONTEST")
    'old-contest'

    >>> path3 = ""
    >>> SiteLocal.pattern_contest.search(path3) is None
    True

    >>> path4 = "/"
    >>> SiteLocal.pattern_contest.search(path4) is None
    True
    """

    # Regex patterns.
    pattern_contest = re.compile(
        r"/(?P<CONTEST>[^/]+)"      # (effectively optional) contest identifier
        r"(/(?P<PROBLEM>[^/]+))?"   # (optional) problem identifier
    )
    pattern_problem = re.compile(r"[^/]+")

    # URL templates.
    url_template_contest = "http://localhost/{0}"
    url_template_suffix_problem = "/{0}"


    def __init__(self):
        self.url = "localhost"
        self.name = "Local"
        self.id = "local"
        self.time_limit_ms = None
        self.memory_limit_kbyte = None
        self.source_limit_kbyte = None

        self._info = None


    def match_contest(self, conf):
        """Overridden.
        """
        location = urlparse(conf['location']).path or '/'
        tokens = SiteLocal.pattern_contest.search(location)
        contest_id = 'local-contest' if tokens is None else tokens.group('CONTEST')
        return SiteLocal.url_template_contest.format(contest_id)


    def get_contest(self, url):
        """Overridden.
        """
        url_path = urlparse(url).path
        assert url_path
        contest = Contest()
        contest.url = url
        tokens = SiteLocal.pattern_contest.search(url_path)
        contest.id = tokens.group('CONTEST')
        assert contest.id
        contest.name = contest.id
        return contest


    def match_problems(self, conf):
        """Overridden.
        """
        url_contest = self.match_contest(conf)
        url_template_problem = url_contest + SiteLocal.url_template_suffix_problem

        urls = []
        # Match single problem from 'location'.
        location = urlparse(conf['location']).path or '/'
        tokens = SiteLocal.pattern_contest.search(location)
        problem_id = tokens and tokens.group('PROBLEM')
        if problem_id:
            urls.append(url_template_problem.format(problem_id))

        # Match potentially multiple problems from 'problems'.
        for problem in conf['problems']:
            tokens = SiteLocal.pattern_problem.findall(problem)
            problem_id = tokens and tokens[-1]
            if problem_id:
                urls.append(url_template_problem.format(problem_id))

        return urls


    def get_problems(self, urls):
        """Overridden.
        """
        problems = []
        for url in urls:
            problem = Problem()
            problem.url = url
            url_path = urlparse(url).path
            assert url_path
            tokens = SiteLocal.pattern_contest.search(url_path)
            problem.id = tokens.group('PROBLEM')
            assert problem.id
            problem.name = problem.id
            problem.time_limit_ms = self.time_limit_ms
            problem.memory_limit_kbyte = self.memory_limit_kbyte
            problem.source_limit_kbyte = self.source_limit_kbyte
            problems.append(problem)
        return problems
