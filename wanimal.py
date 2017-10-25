#!/usr/bin/python
# -*- coding:utf-8 -*-

import urllib
import re
import time

WANIMALURL = "http://wanimal1983.org"
index = 0

def getHtml(url):
    print "Getting... %s" % url
    return urllib.urlopen(url).read()

def getJpgList(html):
    global index
    reg = r'src="(http://78.media.tumblr.com.+?\.jpg)'
    jpgre = re.compile(reg)
    jpgList = re.findall(jpgre, html)
    for jpglink in jpgList:
        print "     -> %s" % jpglink
        match = re.match(r'.*tumblr.com/(.*)/tumblr.*', jpglink)
        if match:
            filename = 'jpg/%s_%s' % (match.group(1), index)
            urllib.urlretrieve(jpglink, filename)
            index += 1

def getNext(html):
    nextfound = re.findall(r'href="(.+?)" id="next">Next', html)
    for next in nextfound:
        nexturl = WANIMALURL + next;
        time.sleep(3)
        doGet(nexturl)

def doGet(url):
    html = getHtml(url)
    getJpgList(html)
    getNext(html)


if __name__ == "__main__":
    #url = "http://wanimal1983.org"
    doGet(WANIMALURL)

