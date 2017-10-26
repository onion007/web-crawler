#!/usr/bin/python
# -*- coding:utf-8 -*-

import urllib
import re
import json

######
# url:
#   1. http://wanimal1983.org
#   2. http://wanimal1983.org/page/xx
#   3. http://wanimal1983.org/archive
#   4. http://wanimal1983.org/archive?before_time=xxxxxxxxx
#
# next:
#   page    --> href="page/2" id="next">Next
#   archive --> href="/archive?before_time=1507775206">Next
#

WANIMALURL = "http://wanimal1983.org"
index = 0
gList = []


def getHtml(url):
    print "Start to get ... >>> %s" % url
    return urllib.urlopen(url).read()


def getJpgList(html):
    global index, gList
    reg = r'(?:src|imageurl)="(http://78\.media\.tumblr\.com[^"]+?\.jpg)"'
    jpgre = re.compile(reg)
    jpgList = re.findall(jpgre, html)
    for jpglink in jpgList:
        match = re.match(r'.*tumblr.com/(.*)/tumblr.*', jpglink)
        if match and jpglink not in gList:
            index += 1
            gList.append(jpglink)
            print(index)
    #        filename = 'jpg/%s_%s.jpg' % (match.group(1), index)
    #        urllib.urlretrieve(jpglink, filename)
    #        index += 1


def getNext(html):
    global gList
    nextfound = re.findall(r'href="(.+?)"[^>]*>Next', html)
    for next in nextfound:
        nexturl = WANIMALURL + next
        import time
        time.sleep(1)
        doGet(nexturl)


def doGet(url):
    readData()
    #html = getPageExample()
    #html = getArchiveExample()
    html = getHtml(url)
    getJpgList(html)
    getNext(html)
    saveData()


def readData(filename='wanimal.txt'):
    global gList
    try:
        with open(filename, 'r') as f:
            data = f.read()
        gList = json.loads(data)
    except IOError:
        pass
    return


def saveData(filename='wanimal.txt'):
    global gList
    with open(filename, 'w') as f:
        f.write(json.dumps(gList))


if __name__ == "__main__":
    urls = [WANIMALURL,
            WANIMALURL+'/archive']
    for url in urls:
        doGet(url)

