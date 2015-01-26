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
        print("Codeforces:match_contest");
        pass

    def get_contest(self, url):
        print("Codeforces:get_contest");
        pass

    def match_problem(self, conf):
        print("Codeforces:match_problem");
        pass

    def get_problem(self, url):
        print("Codeforces:get_problem");
        pass

