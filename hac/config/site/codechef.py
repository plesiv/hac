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


class SiteCodeChef(ISite):
    """CodeChef site processor.

    >>> path1 = "/OCT15/problems/SUBINC"
    >>> SiteCodeChef.pattern_contest.search(path1).group("PROBLEM")
    'SUBINC'

    >>> path2 = "/OCT15"
    >>> SiteCodeChef.pattern_contest.search(path2).group("CONTEST")
    'OCT15'

    >>> path3 = ""
    >>> SiteCodeChef.pattern_contest.search(path3) is None
    True

    >>> path4 = "/"
    >>> SiteCodeChef.pattern_contest.search(path4) is None
    True
    """

    # Regex patterns.
    pattern_contest = re.compile(
        r"/(?P<CONTEST>[a-zA-Z0-9]+)"                # (mandatory) contest identifier
        r"(/(problems/)?(?P<PROBLEM>[a-zA-Z0-9]+))?" # (optional) problem identifier
    )

    pattern_problem = re.compile(r"[a-zA-Z0-9]+")

    # URL templates.
    url_template_contest = "https://www.codechef.com/{0}"
    url_template_suffix_problem = "/problems/{0}"

    # Xpath selectors.
    xpath_contest_name = '/html/head/title/text()'
    xpath_problem_ids = '//*[@class="problems"]//*[@class="problemrow"]//*[substring(@title,1,6) = "Submit"]/text()'
    xpath_problem_name = '//*[@id="pageContent"]//*[@class="header"]//*[@class="title"]/text()' #TODO fix
    xpath_problem_time = '//*[@id="pageContent"]//*[@class="time-limit"]/text()' #TODO fix
    xpath_problem_memory = '//*[@id="pageContent"]//*[@class="memory-limit"]/text()' #TODO fix
    xpath_problem_ins = '//*[@id="pageContent"]//*[@class="sample-tests"]//*[@class="input"]//pre' #TODO fix
    xpath_problem_outs = '//*[@id="pageContent"]//*[@class="sample-tests"]//*[@class="output"]//pre' #TODO fix

    # Proxy for HTTP requests (handles request caching during single run of the program).
    _proxy = RequestsCache()

    # Helper methods
    @staticmethod
    def get_problem_ids(ids, available_ids):
        """CodeChef problems are encoded with a sequences that are combinations
        of uppercase latin letters and digits. This function handles conversion
        from:

            - numbers,
            - single latin letters.

        >>> available_ids = ['SUBINC', 'WDTBAM', 'TIMEASR', 'KSPHERES', 'ADTRI']
        >>> SiteCodeChef.get_problem_ids([], available_ids)
        []

        >>> SiteCodeChef.get_problem_ids(['subinc', 'test', 'b', 'D', '5'], available_ids)
        ['ADTRI', 'KSPHERES', 'SUBINC', 'WDTBAM']
        """
        selected_ids = []

        if isinstance(ids, list):
            for id in ids:
                if id is not None:
                    idx = None

                    if id.isdigit():
                        idx = int(id) - 1

                    elif id.isalpha() and len(id) > 1:
                        id_upper = id.upper()
                        if id_upper in available_ids:
                            selected_ids.append(id_upper)
                        # idx not assigned

                    elif id.isalpha():
                        if id.islower():
                            idx = ord(id) - ord("a")
                        elif id.isupper():
                            idx = ord(id) - ord("A")

                    if idx is not None and idx < len(available_ids):
                        selected_ids.append(available_ids[idx])

        return sorted(set(selected_ids))


    def __init__(self):
        self.url = "www.codechef.com"
        self.name = "CodeChef"
        self.id = "codechef"
        self.time_limit_ms = None
        self.memory_limit_kbyte = 262144
        self.source_limit_kbyte = 50

        self._info = "[SiteCodeChef] Fetching test inputs/outputs not supported!"


    def match_contest(self, conf):
        """Overridden.
        """
        location = urlparse(conf["location"]).path or "/"
        tokens = SiteCodeChef.pattern_contest.search(location)
        contest_id = "404" if tokens is None else tokens.group("CONTEST")
        return SiteCodeChef.url_template_contest.format(contest_id.upper())


    def get_contest(self, url):
        """Overridden.
        """
        url_path = urlparse(url).path
        assert url_path
        contest = Contest()
        contest.url = url
        tokens = SiteCodeChef.pattern_contest.search(url_path)
        contest.id = tokens.group("CONTEST")

        page = SiteCodeChef._proxy.get(url)

        # Data from web:
        #   - contest name.
        if page.status_code == 200:
            t = html.fromstring(page.text)
            e = t.xpath(SiteCodeChef.xpath_contest_name)
            contest.name = (e and str(e[0])) or ""

        return contest


    def match_problems(self, conf):
        """Overridden.
        """
        url_contest = self.match_contest(conf)
        url_template_problem = url_contest + SiteCodeChef.url_template_suffix_problem

        page = SiteCodeChef._proxy.get(url_contest)

        # Data from web:
        #   - available problem ids.
        if page.status_code == 200:
            t = html.fromstring(page.text)
            e = t.xpath(SiteCodeChef.xpath_problem_ids)
            ids_available = [str(e.strip()) for e in e]
        else:
            warn('Unable to fetch: ' + url_contest)
            return []

        ids_selected = []
        # Match single problem from 'location'.
        location = urlparse(conf["location"]).path or "/"
        tokens = SiteCodeChef.pattern_contest.search(location)
        if tokens is not None:
            problem = tokens.group("PROBLEM")
            if problem is not None:
                ids_selected.append(problem)

        # Match potentially multiple problems from 'problems'.
        for problem in conf["problems"]:
            tokens = SiteCodeChef.pattern_problem.findall(problem)
            ids_selected.extend(tokens)

        # If no problems are successfully manually selected, select them all.
        if not ids_selected:
            ids = ids_available
        else:
            ids = SiteCodeChef.get_problem_ids(ids_selected, ids_available)

        return [url_template_problem.format(id) for id in ids]


    def get_problems(self, urls):
        """Overridden.
        """
        problems = []
        for url in urls:
            problem = Problem()
            problem.url = url
            url_path = urlparse(url).path
            assert url_path
            tokens = SiteCodeChef.pattern_contest.search(url_path)
            problem.id = tokens.group("PROBLEM")
            assert problem.id
            problem.source_limit_kbyte = self.source_limit_kbyte

            page = SiteCodeChef._proxy.get(url)

            #TODO Implement the rest from here...
            # Data from web (for each problem):
            if page.status_code == 200:
                t = html.fromstring(page.text)
                #   - problem name,
                e = t.xpath(SiteCodeChef.xpath_problem_name)
                problem.name = (e and str(e[0])) or None
                #   - problem time limit,
                e = t.xpath(SiteCodeChef.xpath_problem_time)
                limit = e and float(e[0].split()[0]) * 1000
                problem.time_limit_ms = limit or self.time_limit_ms
                #   - problem memory limit,
                e = t.xpath(SiteCodeChef.xpath_problem_memory)
                limit = e and float(e[0].split()[0]) * 2**10
                problem.memory_limit_kbyte = limit or self.memory_limit_kbyte
                #   - test inputs,
                e = t.xpath(SiteCodeChef.xpath_problem_ins)
                problem.inputs = [os.linesep.join(inp.itertext()) for inp in e]
                #   - test outputs.
                e = t.xpath(SiteCodeChef.xpath_problem_outs)
                problem.outputs = [os.linesep.join(out.itertext()) for out in e]

                problems.append(problem)
        return problems
