#!/usr/bin/python
# -*- coding:utf-8 -*-

import urllib
import re


class Crawler:
    start = ''
    target_str = ''
    next_page_str = ''
    _domain = ''
    _url = ''
    _html = ''
    result = {}

    def __init__(self, start, target, next_page=''):
        self.start = start
        self.target_str = target
        self.next_page_str = next_page
        self._url = start
        self._target_reg = re.compile(self.target_str)
        if '' == next_page:
            self._next_page_reg = None
        else:
            self._next_page_reg = re.compile(self.next_page_str)
        m = re.match(r'(http://[^/]+)', start)
        if m:
            self._domain = m.group(1)

    def _gethtml(self):
        self._html = urllib.urlopen(self._url).read()

    def _crawl(self):
        if '' == self._html:
            self._gethtml()
        self.result[self._url] = re.findall(self._target_reg, self._html)

    def next_page(self):
        if '' == self._html:
            self._gethtml()
        if self._next_page_reg is not None:
            # TODO: use another method to do.
            next_pages = re.findall(self._next_page_reg, self._html)
            for n in next_pages:
                # To fix the error link likes '/archive' => 'http://x.x.x/archive'
                if n.startswith('http://'):
                    self._url = n
                else:
                    self._url = self._domain + n
                self._html = ''
        else:
            self._url = ''

    def run(self):
        self._gethtml()
        while '' == self._html:
            self._crawl()
            self.next_page()
            self._gethtml()
