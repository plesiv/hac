# -*- coding: utf-8 -*-

from hac.data import ISite, Contest, Problem

class SiteCodeforces(ISite):
    """
    """
    def __init__(self):
        self.url = "http://codeforces.com/"
        self.name = "Codeforces"
        self.ID = "codeforces"
        self.time_limit_ms = None
        self.memory_limit_kbyte = None
        self.source_limit_kbyte = 64

    def match_contest(self, conf):
        return "Codeforces:match_contest"

    def get_contest(self, url):
        return "Codeforces:get_contest"

    def match_problems(self, conf):
        return "Codeforces:match_problems"

    def get_problems(self, url):
        return "Codeforces:get_problems"

