# -*- coding: utf-8 -*-

import os
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


class SiteCodeforces(ISite):
    """Codeforces site processor.

    >>> path1 = "/contest/512/problem/a"
    >>> SiteCodeforces.pattern_contest.search(path1).group("PROBLEM")
    'a'

    >>> path2 = "/425/problem/C"
    >>> SiteCodeforces.pattern_contest.search(path2).group("CONTEST")
    '425'

    >>> path3 = ""
    >>> SiteCodeforces.pattern_contest.search(path3) is None
    True

    >>> path4 = "/"
    >>> SiteCodeforces.pattern_contest.search(path4) is None
    True

    >>> path5 = "/425/C"
    >>> SiteCodeforces.pattern_contest.search(path5).group("PROBLEM")
    'C'
    """

    # Regex patterns.
    pattern_contest = re.compile(
        r"(/contest)?"                              # (optional) '/contest' prefix
        r"/(?P<CONTEST>[0-9]+)"                     # (mandatory) contest identifier
        r"((/problem)?/(?P<PROBLEM>[a-zA-Z0-9]+))?" # (optional) problem identifier
    )
    pattern_problem = re.compile(r"[a-zA-Z0-9]+")

    # URL templates.
    url_template_contest = "http://codeforces.com/contest/{0}"
    url_template_suffix_problem = "/problem/{0}"

    # Xpath selectors.
    xpath_contest_name = '//*[@id="sidebar"]//a[contains(@href, "contest")]/text()'
    xpath_problem_ids = '//*[@id="pageContent"]//*[@class="id"]//a/text()'
    xpath_problem_name = '//*[@id="pageContent"]//*[@class="header"]//*[@class="title"]/text()'
    xpath_problem_time = '//*[@id="pageContent"]//*[@class="time-limit"]/text()'
    xpath_problem_memory = '//*[@id="pageContent"]//*[@class="memory-limit"]/text()'
    xpath_problem_ins = '//*[@id="pageContent"]//*[@class="sample-tests"]//*[@class="input"]//pre'
    xpath_problem_outs = '//*[@id="pageContent"]//*[@class="sample-tests"]//*[@class="output"]//pre'

    # Proxy for HTTP requests (handles request caching during single run of the program).
    _proxy = RequestsCache()

    # Helper methods
    @staticmethod
    def resolve_problem_id(id_in):
        """Codeforces problems are encoded with uppercase latin letters. This
        function handles conversion from:

            - lowercase latin letters,
            - numbers.

        >>> SiteCodeforces.resolve_problem_id('A')
        'A'

        >>> SiteCodeforces.resolve_problem_id('z')
        'Z'

        >>> SiteCodeforces.resolve_problem_id('3')
        'C'

        >>> SiteCodeforces.resolve_problem_id('.') is None
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
        self.url = "codeforces.com"
        self.name = "Codeforces"
        self.id = "codeforces"
        self.time_limit_ms = None
        self.memory_limit_kbyte = None
        self.source_limit_kbyte = 64

        self._info = None


    def match_contest(self, conf):
        """Overridden.
        """
        location = urlparse(conf['location']).path or '/'
        tokens = SiteCodeforces.pattern_contest.search(location)
        contest_id = "999999" if tokens is None else tokens.group('CONTEST')
        return SiteCodeforces.url_template_contest.format(contest_id)


    def get_contest(self, url):
        """Overridden.
        """
        url_path = urlparse(url).path
        assert url_path
        contest = Contest()
        contest.url = url
        tokens = SiteCodeforces.pattern_contest.search(url_path)
        contest.id = tokens.group('CONTEST')

        page = SiteCodeforces._proxy.get(url)

        # Data from web:
        #   - contest name.
        if page.status_code == 200:
            t = html.fromstring(page.text)
            e = t.xpath(SiteCodeforces.xpath_contest_name)
            contest.name = (e and str(e[0])) or None

        return contest


    def match_problems(self, conf):
        """Overridden.
        """
        url_contest = self.match_contest(conf)
        url_template_problem = url_contest + SiteCodeforces.url_template_suffix_problem

        page = SiteCodeforces._proxy.get(url_contest)

        # Data from web:
        #   - available problem ids.
        if page.status_code == 200:
            t = html.fromstring(page.text)
            e = t.xpath(SiteCodeforces.xpath_problem_ids)
            ids_available = [str(e.strip()) for e in e]

        ids = []
        # Match single problem from 'location'.
        location = urlparse(conf['location']).path or '/'
        tokens = SiteCodeforces.pattern_contest.search(location)
        if tokens is not None:
            id_raw = tokens.group('PROBLEM')
            id_problem = SiteCodeforces.resolve_problem_id(id_raw)
            if id_problem:
                ids.append(id_problem)

        # Match potentially multiple problems from 'problems'.
        for problem in conf['problems']:
            tokens = SiteCodeforces.pattern_problem.findall(problem)
            id_raw = tokens and tokens[-1]
            id_problem = SiteCodeforces.resolve_problem_id(id_raw)
            if id_problem:
                ids.append(id_problem)

        # If no problems are successfully manually selected, select them all.
        if not ids:
            ids = ids_available

        # Notify about selected but non-available problems.
        urls = []
        for id in ids:
            if id in ids_available:
                urls.append(url_template_problem.format(id))
            else:
                warn('Problem "' + id + '" does not exist in ' + url_contest)

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
            tokens = SiteCodeforces.pattern_contest.search(url_path)
            problem.id = tokens.group('PROBLEM')
            assert problem.id
            problem.source_limit_kbyte = self.source_limit_kbyte

            page = SiteCodeforces._proxy.get(url)

            # Data from web (for each problem):
            if page.status_code == 200:
                t = html.fromstring(page.text)
                #   - problem name,
                e = t.xpath(SiteCodeforces.xpath_problem_name)
                problem.name = (e and str(e[0])) or None
                #   - problem time limit,
                e = t.xpath(SiteCodeforces.xpath_problem_time)
                limit = e and float(e[0].split()[0]) * 1000
                problem.time_limit_ms = limit or self.time_limit_ms
                #   - problem memory limit,
                e = t.xpath(SiteCodeforces.xpath_problem_memory)
                limit = e and float(e[0].split()[0]) * 2**10
                problem.memory_limit_kbyte = limit or self.memory_limit_kbyte
                #   - test inputs,
                e = t.xpath(SiteCodeforces.xpath_problem_ins)
                problem.inputs = [os.linesep.join(inp.itertext()) for inp in e]
                #   - test outputs.
                e = t.xpath(SiteCodeforces.xpath_problem_outs)
                problem.outputs = [os.linesep.join(out.itertext()) for out in e]

                problems.append(problem)
        return problems
