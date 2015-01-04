#!/usr/bin/env python
# coding=utf-8
#
# cftest - CLI tool for testing solutions to problems from http://www.codeforces.com
# Copyright (C) 2014-2015  Zoran Plesivčak <zplesiv@gmail.com>
# This software is distributed under the terms of the MIT License.
#

import sys
import argparse
import re
import os
import shutil

# Python2 and Python3 compatibility
try:
    from urllib2 import urlopen
    from HTMLParser import HTMLParser
except:
    from urllib.request import urlopen
    from html.parser import HTMLParser

# Default configuration
DEFAULT_LANGUAGES = ["cpp"]
PREFIX_CONTEST_DIR = ""
PREFIX_INPUT_FILES = 'input'
PREFIX_OUTPUT_FILES = 'output'

# -----------------------------------------------------------------------------

# Construct parser
parser = argparse.ArgumentParser(
    description=
        """Select contest (number) and optionally problems (letters) for which
        to prepare testing environment in current directory.
        """,
    epilog="Examples..."
)
parser.add_argument("CONTEST", help="Codeforces contest number")
parser.add_argument("PROBLEMS", action="append", type=str, nargs="*",
    help="Problems' letters (Defaults to all problems)")
parser.add_argument(
    "-f", "--force", action="store_true",
    help=
        """Overwrite existing directories (Not enabled by default,
        DANGEROUS!!!)"""
)
parser.add_argument(
    "-d", "--create-subdirs", type=int, choices=[0, 1, 2], default=1,
    help=
        """Levels of directories to create (Defaults to 1, e.g. create
        directories for problems in current directory)"""
)
parser.add_argument(
    "-l", "--lang", action="append", choices=["py", "cpp"], default=[],
    help="Languages for which test environment will be prepared (Default is " +
        str(DEFAULT_LANGUAGES) + ")"
)

# -----------------------------------------------------------------------------

# Problems parser class
class CodeforcesProblemParser(HTMLParser):

    def __init__(self, folder):
        HTMLParser.__init__(self)
        self.folder = folder
        self.num_tests = 0
        self.testcase = None
        self.start_copy = False

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            if attrs == [('class', 'input')]:
                self.num_tests += 1
                self.testcase = open(
                    '%s/%s%d' % (self.folder, PREFIX_INPUT_FILES, self.num_tests), 'w')
            elif attrs == [('class', 'output')]:
                self.testcase = open(
                    '%s/%s%d' % (self.folder, PREFIX_OUTPUT_FILES, self.num_tests), 'w')
        elif tag == 'pre':
            if self.testcase != None:
                self.start_copy = True

    def handle_endtag(self, tag):
        if tag == 'br':
            if self.start_copy:
                self.testcase.write('\n')
                self.end_line = True
        if tag == 'pre':
            if self.start_copy:
                if not self.end_line:
                    self.testcase.write('\n')
                self.testcase.close()
                self.testcase = None
                self.start_copy = False

    def handle_entityref(self, name):
        if self.start_copy:
            self.testcase.write(self.unescape(('&%s;' % name)))

    def handle_data(self, data):
        if self.start_copy:
            self.testcase.write(data)
            self.end_line = False

# Contest parser class
class CodeforcesContestParser(HTMLParser):

    def __init__(self, contest):
        HTMLParser.__init__(self)
        self.contest = contest
        self.start_contest = False
        self.start_problem = False
        self.name = ''
        self.problems = []
        self.problem_names = []

    def handle_starttag(self, tag, attrs):
        if self.name == '' and attrs == [('style', 'color: black'), ('href', '/contest/%s' % (self.contest))]:
                self.start_contest = True
        elif tag == 'option':
            if len(attrs) == 1:
                regexp = re.compile(r"'[A-Z]'")
                string = str(attrs[0])
                search = regexp.search(string)
                if search is not None:
                    self.problems.append(search.group(0).split("'")[-2])
                    self.start_problem = True

    def handle_endtag(self, tag):
        if tag == 'a' and self.start_contest:
            self.start_contest = False
        elif self.start_problem:
            self.start_problem = False

    def handle_data(self, data):
        if self.start_contest:
            self.name = data
        elif self.start_problem:
            self.problem_names.append(data)

# Parses the problem page
def parse_problem(folder, contest, problem):
    url = 'http://codeforces.com/contest/{0}/problem/{1}'.format(contest, problem)
    html = urlopen(url).read()
    parser = CodeforcesProblemParser(folder)
    parser.feed(html.decode('utf-8').encode('utf-8')) # Should fix special chars problems.
    return parser.num_tests

# Parses the contest page
def parse_contest(contest):
    url = 'http://codeforces.com/contest/{0}'.format(contest)
    html = urlopen(url).read()
    parser = CodeforcesContestParser(contest)
    parser.feed(html.decode('utf-8'))
    return parser

# Warnings
def warn(s): sys.stdout.write("WARNING: " + s + "\n")
def erro(s): sys.stderr.write("ERROR: " + s + "\n")

# Create directory-structure (return True if directory is empty)
def create_directory(path, force=False):
    if os.path.exists(path):
        if force:
            shutil.rmtree(path)
        else:
            warn('Directory "{0}" already exists{1}!'.format(
                os.path.relpath(path),
                " and it's NOT EMPTY" if os.listdir(path) else ""))

    os.makedirs(path)
    return not bool(os.listdir(path))

# -----------------------------------------------------------------------------

def main(args=sys.argv[1:]):
    # When no arguments given show Help
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    # Parse and normalize CLI arguments
    args = parser.parse_args()
    args.lang = sorted(set(args.lang)) if args.lang else DEFAULT_LANGUAGES
    args.PROBLEMS = sorted(set(''.join(args.PROBLEMS[0])))

    # Parse Codeforces.com for contest and problems
    content = parse_contest(args.CONTEST)

    # All problems if none explicitly chosen
    if len(args.PROBLEMS) == 0:
        problems = content.problems
    else:
        problems = sorted(set(content.problems) & set(args.PROBLEMS))

    if len(problems) == 0:
        erro("No eligible problems chosen...")
        erro("Problems available in contest {0}: {1}.".
            format(args.CONTEST, str(content.problems or "[<no problems>]")))
        sys.exit(2)

    # Create contest directory starting from current directory (if needed)
    contest_path = os.curdir
    if args.create_subdirs == 2:
        contest_path = os.path.join(contest_path,
            PREFIX_CONTEST_DIR + str(args.CONTEST))
        create_directory(contest_path, False)

    for idx, prb in enumerate(problems):
        if args.create_subdirs >= 1:
            problem_path = os.path.join(contest_path, prb)
        dir_empty = create_directory(problem_path, args.force)

        ### TODO
        if dir_empty:
            num_tests = parse_problem(problem_path, args.CONTEST, prb)
            print(idx,prb,num_tests)

        #try:
            #os.makedirs(problem_path)
        #except:
            #print('WARNING: Directory "{0}" already exists!'.
                #format(os.path.normpath(contest_path)))



        #folder = '%s/%s/' % (contest, problem)
        #call(['mkdir', '-p', folder])
        #call(['cp', '-n', TEMPLATE, '%s/%s/%s.cc' % (contest, problem, problem)])
        #num_tests = parse_problem(folder, contest, problem)
        #print('%d sample test(s) found.' % num_tests)
        #generate_test_script(folder, num_tests, problem)
        #print ('========================================')

    #print(args.create_subdirs)
    print(args.force)
    #print(args.lang)
    #print(args.CONTEST)
    #print(args.PROBLEMS)
    #print(content.contest)
    #print(content.start_contest)
    #print(content.start_problem)
    #print(content.name)
    #print(content.problems)
    #print(content.problem_names)
