# -*- coding: utf-8 -*-
"""Utilities for application plugin-system.

NOTE: for simplicity, language and runner templates are referred to as plug-ins
      in this file (along with site plug-ins).
"""
import imp
import os
import sys
import re
import requests
from string import Template

if sys.version_info.major == 2:
    from urlparse import urlparse
else:
    from urllib.parse import urlparse

import hac
from hac import DataType
from hac.data import ISiteRegistry
from hac.util_common import indent_distribute


_plugin_fname_regex = {
    DataType.LANG: r"^(?P<temp>[^.]+)\.(?P<prio>[^.]+)\.(?P<ext>[^.]+)$",
    DataType.RUNNER: {
        'temp': r"^(?P<temp>[^.]+)\.(?P<prio>[^.]+)\.(?P<ext>[^.]+)$",
        'part_u': r"^(?P<lang>[^.]+)\.(?P<part>[^.]+)\.{prio}\.{ext}$",
    }
}

# -- Languages ----------------------------------------------------------------
def _plugin_discover_langs(dirs):
    """Discovers all available programming language templates in a given list
    of directories.

    Programming language template file-names are expected to be in the format:

        <PLUGIN_TEMP>.<PRIORITY>.<LANGUAGE-EXTENSION>

    Where:

        * <PLUGIN_TEMP> is application constant setting (from SETTINGS_CONST).
        * <PRIORITY> is the integer higher or equal to zero. Lower <PRIORITY>
            number indicates higher priority,
        * <LANGUAGE-EXTENSION> denotes the programming language of the
        template.

    For example, highest priority Python programming language template would
    have fname:

        temp.0.py

    Returns dictionary mapping "<LANGUAGE-EXTENSION>.<PRIORITY>" to the
    contents of the given programming language template file.
    """
    fname_pat = re.compile(_plugin_fname_regex[DataType.LANG])
    sep_l = hac.SETTINGS_CONST['plugin_temp_sep'][DataType.LANG]

    langs = {}
    for cdir in dirs:
        if os.path.isdir(cdir):
            for fname in os.listdir(cdir):
                token = fname_pat.search(fname)
                if token:
                    # Filename matches specified regular expression.
                    key = token.group("ext") + sep_l + token.group("prio")
                    if (key not in langs):
                        with open(os.path.join(cdir, fname), 'r') as f:
                            contents = f.read()
                        langs[key] = contents
    return langs


# -- Runners ------------------------------------------------------------------
def _plugin_discover_runners(dirs):
    """In a given list of directories discovers all available:

        * runner templates and
        * runner templating parts.

    Generates runners' contents by applying templating parts to the templates.
    Each template must have at least one templating part for each corresponding
    programming language.

    Runner template file-names are expected to be in the format:

        <PLUGIN_TEMP>.<PRIORITY>.<RUNNER-EXTENSION>

    Where:

        * <PLUGIN_TEMP> is application constant setting (from SETTINGS_CONST).
        * <PRIORITY> is the integer higher or equal to zero. Lower <PRIORITY>
            number indicates higher priority,
        * <RUNNER-EXTENSION> denotes runner file-type of the template.

    For example, highest priority shell runner template would have filename:

        temp.0.sh

    Runner template part file-names are expected to be in the format:

        <LANGUAGE-EXTENSION>.<PART>.<PRIORITY>.<RUNNER-EXTENSION>

    Where:

        * <LANGUAGE-EXTENSION> denotes which programming language is this
            runner template part for,
        * <PART> is the name of the runner template part,
        * <PRIORITY>.<RUNNER-EXTENSION> should correspond to the end of some
            existing <PLUGIN_TEMP>.<PRIORITY>.<RUNNER-EXTENSION> template.
            Matching to the appropriate template is done according to this
            part.

    For example, parts "compile" and "execute" for Python programming language
    and temp.0.sh template would be:

        py.compile.0.sh
        py.execute.0.sh

    Returns dictionary mapping "<RUNNER-EXTENSION>.<PRIORITY>" to the
    corresponding runner dictionaries. Each runner dictionary maps from
    "LANGUAGE-EXTENSION" to the contents of the prepared for that programming
    language.
    """
    ftemp_pat = re.compile(_plugin_fname_regex[DataType.RUNNER]['temp'])
    fpart_regex_u =_plugin_fname_regex[DataType.RUNNER]['part_u']
    sep_r = hac.SETTINGS_CONST['plugin_temp_sep'][DataType.RUNNER]
    pref_r = hac.SETTINGS_CONST['plugin_temp_part_prefix'][DataType.RUNNER]

    runners = {}
    for cdir_r in dirs:
        if os.path.isdir(cdir_r):
            for fname_r in os.listdir(cdir_r):

                # Is filename in proper runner-template format?
                tok_r = ftemp_pat.search(fname_r)
                if tok_r:
                    ext = tok_r.group("ext")
                    prio = tok_r.group("prio")

                    key_r = ext + sep_r + prio
                    fpart_regex = fpart_regex_u.format(ext=ext, prio=prio)
                    fpart_pat = re.compile(fpart_regex)
                    fpath_r = os.path.join(cdir_r, fname_r)
                    with open(fpath_r, 'r') as f:
                        contents_r = f.read()

                    # Take first occurrence of runner template.
                    if key_r not in runners:

                        # Get available parts (get the first occurence).
                        parts = {}
                        for cdir_p in dirs:
                            if os.path.isdir(cdir_p):
                                for fname_p in os.listdir(cdir_p):
                                    # Is filename in proper part format?
                                    tok_p = fpart_pat.search(fname_p)
                                    if tok_p:
                                        lang = tok_p.group("lang")
                                        part = tok_p.group("part")
                                        fpath_p = os.path.join(cdir_p, fname_p)
                                        with open(fpath_p, 'r') as f:
                                            contents_p = f.read()

                                        if lang not in parts:
                                            parts[lang] = {}

                                        if part not in parts[lang]:
                                            parts[lang][part] = contents_p

                        # Do the templating.
                        langs = {}
                        for lang in parts:
                            rtemp, rparts = indent_distribute(contents_r,
                                                              parts[lang],
                                                              pref_r)
                            template = Template(rtemp)
                            rendered = template.safe_substitute(rparts)

                            if lang not in langs:
                                langs[lang] = rendered

                        runners[key_r] = langs
    return runners


# -- Sites --------------------------------------------------------------------
def _plugin_discover_sites(dirs):
    """Dynamically discovers all web-site processors in a given list of
    directories.

    Returns list of site-processor objects. Site processors occurring in a
    directories earlier in the input list have a higher priority. All
    discovered classes are instantiated with empty constructor.
    """
    for cdir in dirs:
        if os.path.isdir(cdir):
            for filename in os.listdir(cdir):
                froot, fext = os.path.splitext(filename)
                if fext == ".py":
                    fname, fpath, fdescr = imp.find_module(froot, [cdir])
                    if fname:
                        # Register discovered site-processor module in
                        # ISiteRegistry.sites
                        mod = imp.load_module(froot, fname, fpath, fdescr)
    return [ site() for site in ISiteRegistry.sites ]


# TODO crowd-source writing of this function
def plugin_match_site(sites, conf): #very-stupid matching now
    """Must return a site. Reasonable default site if can't match any site
    explicitly.
    """
    for site in sites:
        hostname = urlparse(conf['location']).hostname.lower()
        if(hostname in site.name.lower() or hostname in site.ID.lower()):
            return site.url
    return sites[0].url


# -- Common data utilities ----------------------------------------------------
_plugin_discover_funcs = {
    DataType.LANG: _plugin_discover_langs,
    DataType.RUNNER: _plugin_discover_runners,
    DataType.SITE: _plugin_discover_sites,
}


def plugin_collect(data_type):
    """Retrieves application default and user-specified plug-ins.

    User-specified plug-ins of the same name override application default
    plug-ins.
    """
    plugin_path = hac.SETTINGS_CONST["plugin_path"][data_type]
    plugin_discover = _plugin_discover_funcs[data_type]

    return plugin_discover([
        os.path.join(hac.SETTINGS_CONST["config_user_path"],
                     plugin_path),
        os.path.join(hac.SETTINGS_VAR["app_root_dir"],
                     hac.SETTINGS_CONST["config_app_path"],
                     plugin_path),
    ])


# -- Web-data utilities -------------------------------------------------------
class RequestsCache(object):

    def __init__(self):
        self._store = {}

    def get(self, url):
        if url not in self._store:
            self._store[url] = requests.get(url)
        return self._store[url]
