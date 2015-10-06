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


class SiteRosalind(ISite):
    """Rosalind site processor.

    >>> path1 = "/problems/rsub"
    >>> SiteRosalind.pattern_contest.search(path1).group("PROBLEM")
    'rsub'

    >>> path2 = "/wfmd/"
    >>> SiteRosalind.pattern_contest.search(path2).group("PROBLEM")
    'wfmd'

    >>> path3 = ""
    >>> SiteRosalind.pattern_contest.search(path3) is None
    True

    >>> path4 = "/"
    >>> SiteRosalind.pattern_contest.search(path4) is None
    True
    """

    # Regex patterns.
    pattern_contest = re.compile(
        r"(/problems)?/(?P<PROBLEM>[a-zA-Z]+)"    # (mandatory) problem identifier
        r"(/)?"                                      # (optional) slash
    )
    pattern_problem = re.compile(r"[a-zA-Z]+")

    # URL templates.
    url_contest = "http://rosalind.info"
    url_template_suffix_problem = "/problems/{0}/"

    # Xpath selectors.
    xpath_problem_name = '//h1/text()'
    xpath_problem_ins = '//*[@id="sample-dataset"]/following::div[1]//pre/text()'
    xpath_problem_outs = '//*[@id="sample-output"]/following::div[1]//pre/text()'

    # Proxy for HTTP requests (handles request caching during single run of the program).
    _proxy = RequestsCache()


    def __init__(self):
        self.url = "rosalind.info"
        self.name = "Rosalind"
        self.id = "rosalind"
        self.time_limit_ms = None
        self.memory_limit_kbyte = None
        self.source_limit_kbyte = None

        self._info = None


    def match_contest(self, conf):
        """Overridden.
        """
        return SiteRosalind.url_contest


    def get_contest(self, url):
        """Overridden.
        """
        contest = Contest()
        contest.url = url
        contest.id = "rosalind-problems"
        contest.name = "Rosalind problems archive"
        return contest


    def match_problems(self, conf):
        """Overridden.
        """
        url_template_problem = (SiteRosalind.url_contest +
                                SiteRosalind.url_template_suffix_problem)

        ids = []
        # Match single problem from 'location'.
        location = urlparse(conf['location']).path or '/'
        tokens = SiteRosalind.pattern_contest.search(location)
        if tokens is not None:
            id_raw = tokens.group('PROBLEM')
            if id_raw:
                ids.append(id_raw.lower())

        # Match potentially multiple problems from 'problems'.
        for problem in conf['problems']:
            tokens = SiteRosalind.pattern_problem.findall(problem)
            id_raw = tokens and tokens[-1]
            if id_raw:
                ids.append(id_raw.lower())

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
            tokens = SiteRosalind.pattern_contest.search(url_path)
            problem.id = tokens.group('PROBLEM')
            assert problem.id

            page = SiteRosalind._proxy.get(url)

            # Data from web (for each problem):
            if page.status_code == 200:
                t = html.fromstring(page.text)
                #   - problem name,
                e = t.xpath(SiteRosalind.xpath_problem_name)
                problem.name = (e and str(e[0]).strip()) or None
                #   - test input, (single fetched)
                e = t.xpath(SiteRosalind.xpath_problem_ins)
                problem.inputs = e and [str(e[0]).strip()]
                #   - test outputs, (single fetched)
                e = t.xpath(SiteRosalind.xpath_problem_outs)
                problem.outputs = e and [str(e[0]).strip()]

                if (problem.name and
                    problem.inputs and
                    problem.outputs):
                        problems.append(problem)
            else:
                warn('Problem "' + problem.id + '" does not exist on Rosalind!')

        return problems
