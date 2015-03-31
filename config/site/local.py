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
    template_task_suburl = "/{0}"

    # Regex patterns
    pattern_contest = re.compile(r"/(?P<contest>[^/]*)?(/(?P<task>[^/]*))?")
    pattern_task = re.compile(r"[^/]+")
    # -> Path has to start with '/'

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
        cont_dict['ID'] = tokens.group('contest')
        assert cont_dict['ID']
        cont_dict['name'] = cont_dict['ID']
        return Contest(**cont_dict)

    def match_problems(self, conf):
        contest_url = self.match_contest(conf)
        template_task_url = contest_url + SiteLocal.template_task_suburl

        urls = []
        # Match single problem from location member
        url_path = urlparse(conf['location']).path or '/'
        tokens = SiteLocal.pattern_contest.search(url_path)
        task_ID = tokens.group('task')
        if task_ID:
            urls.append(template_task_url.format(task_ID))

        # Match potentially multiple problems from problems member
        from pudb import set_trace; set_trace()
        #TODO match last alphanum after any '/': sensible default
        return "Local:match_contest"

    def get_problems(self, url):
        #TODO populate DS
        return "Local:get_problems"

