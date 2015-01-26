# -*- coding: utf-8 -*-

from hac.data import ISite, Contest, Problem

class SiteCodechef(ISite):
    """
    """
    def __init__(self):
        self.url = "http://www.codechef.com/"
        self.name = "CodeChef"
        self.ID = "codechef"
        self.time_limit_ms = None
        self.memory_limit_kbyte = None
        self.source_limit_kbyte = 48

    def match_contest(self, conf):
        return "CodeChef:match_contest"

    def get_contest(self, url):
        return "CodeChef:get_contest"

    def match_problems(self, conf):
        return "CodeChef:match_problems"

    def get_problems(self, urls):
        return "CodeChef:get_problems"

