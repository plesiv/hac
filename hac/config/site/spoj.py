# -*- coding: utf-8 -*-

import re
import sys
from lxml import html

if sys.version_info.major == 2:
    from urlparse import urlparse
else:
    from urllib.parse import urlparse

from hac.data import ISite, Contest, Problem
from hac.util_common import warn
from hac.util_data import RequestsCache


class SiteSpoj(ISite):
    """Spoj site processor.

    >>> path1 = "/problems/TEST"
    >>> SiteSpoj.pattern_contest.search(path1).group("PROBLEM")
    'TEST'

    >>> path2 = "/BOOKS1"
    >>> SiteSpoj.pattern_contest.search(path2).group("PROBLEM")
    'BOOKS1'

    >>> path3 = ""
    >>> SiteSpoj.pattern_contest.search(path3) is None
    True

    >>> path4 = "/"
    >>> SiteSpoj.pattern_contest.search(path4) is None
    True
    """

    # Regex patterns.
    pattern_contest = re.compile(
        r"(/problems)?/(?P<PROBLEM>[a-zA-Z0-9]+)"    # (mandatory) problem identifier
    )
    pattern_problem = re.compile(r"[a-zA-Z0-9]+")

    # URL templates.
    url_contest = "http://www.spoj.com"
    url_template_suffix_problem = "/problems/{0}"

    # Xpath selectors.
    xpath_problem_name = '//*[@id="problem-name"]/text()'
    xpath_problem_time = '//*[@id="problem-meta"]/tbody/tr[3]/td[2]/text()'
    xpath_problem_source = '//*[@id="problem-meta"]/tbody/tr[4]/td[2]/text()'
    xpath_problem_memory = '//*[@id="problem-meta"]/tbody/tr[5]/td[2]/text()'
    xpath_problem_ins_outs = '//*[@id="problem-body"]//pre/text()'

    # Proxy for HTTP requests (handles request caching during single run of the program).
    _proxy = RequestsCache()


    def __init__(self):
        self.url = "www.spoj.com"
        self.name = "Sphere online judge"
        self.id = "spoj"
        self.time_limit_ms = None
        self.memory_limit_kbyte = None
        self.source_limit_kbyte = None

        self._info = "[SiteSpoj] Fetching only a subset of problems is supported!"


    def match_contest(self, conf):
        """Overridden.
        """
        return SiteSpoj.url_contest


    def get_contest(self, url):
        """Overridden.
        """
        contest = Contest()
        contest.url = url
        contest.id = "spoj-problems"
        contest.name = "Spoj problems archive"
        return contest


    def match_problems(self, conf):
        """Overridden.
        """
        url_template_problem = SiteSpoj.url_contest + SiteSpoj.url_template_suffix_problem

        ids = []
        # Match single problem from 'location'.
        location = urlparse(conf['location']).path or '/'
        tokens = SiteSpoj.pattern_contest.search(location)
        if tokens is not None:
            id_raw = tokens.group('PROBLEM')
            if id_raw:
                ids.append(id_raw.upper())

        # Match potentially multiple problems from 'problems'.
        for problem in conf['problems']:
            tokens = SiteSpoj.pattern_problem.findall(problem)
            id_raw = tokens and tokens[-1]
            if id_raw:
                ids.append(id_raw.upper())

        # Notify about selected but non-available problems.
        urls = [url_template_problem.format(id) for id in ids]

        return sorted(urls)


    def get_problems(self, urls):
        """Overridden.
        """
        problems = []
        for url in urls:
            problem = Problem()
            problem.url = url
            url_path = urlparse(url).path
            assert url_path
            tokens = SiteSpoj.pattern_contest.search(url_path)
            problem.id = tokens.group('PROBLEM')
            assert problem.id

            page = SiteSpoj._proxy.get(url)

            # Data from web (for each problem):
            if page.status_code == 200:
                t = html.fromstring(page.text)
                #   - problem name,
                e = t.xpath(SiteSpoj.xpath_problem_name)
                problem.name = (e and str(e[0])) or None
                #   - problem time limit,
                e = t.xpath(SiteSpoj.xpath_problem_time)
                p = e and e[0].strip()[:-1] # remove whitespace characters and 's' at the end
                problem.time_limit_ms = p and float(p) * 1000
                #   - problem source limit,
                e = t.xpath(SiteSpoj.xpath_problem_source)
                p = e and e[0].strip()[:-1] # remove whitespace characters and 'B' at the end
                problem.source_limit_kbyte = p and float(p) / 1000
                #   - problem memory limit,
                e = t.xpath(SiteSpoj.xpath_problem_memory)
                p = e and e[0].strip()[:-2] # remove whitespace characters and 'MB' at the end
                problem.memory_limit_kbyte = p and float(p) * 2**10
                #   - test inputs and outputs.
                e = t.xpath(SiteSpoj.xpath_problem_ins_outs)
                problem.inputs = [i.strip() for i in e[0:][::2]]
                problem.outputs = [o.strip() for o in e[1:][::2]]

                if (problem.name and
                    problem.time_limit_ms and
                    problem.source_limit_kbyte and
                    problem.memory_limit_kbyte and
                    problem.inputs and
                    problem.outputs):
                        problems.append(problem)
                else:
                    warn('Problem "' + problem.id + '" not fetched successfully!')

            else:
                warn('Problem "' + problem.id + '" does not exist on Spoj!')

        return problems
