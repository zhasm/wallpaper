#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#author:         rex
#blog:           http://iregex.org
#filename        iw.py
#created:        2010-11-21 08:58
import urllib2
import urllib
import re
import json

def getLengthOfUrlFile(fd):
    '''get the size of a file to be downloaded.'''
    x=fd.info()
    try:
        return int(x["content-length"])
    except:
        return 0
        
def online_open(url):
    '''ordinary way of open url and read content.'''
    fd=urllib2.urlopen(url)
    try:
        data=fd.read()
        fd.close()
        return data
    except:
        return None
def getPreviewImgs(content):
    '''parse preview IMG urls, and return a list'''
    #http://interfacelift.com/wallpaper_beta/previews/02432_elephantastic.jpg
    regex=re.compile(r"http://interfacelift.com/wallpaper_beta/previews/\w+\.jpg\b")
    result=regex.findall("".join(content))
    return result if result else [] 
            
def main():
    url="http://interfacelift.com/wallpaper_beta/downloads/date/any/"
    page=online_open(url)
    imgs=getPreviewImgs(page)
    print "content-type: application/json\n"
#    print "content-type: text/plain\n"
    x=json.dumps({"imgs": imgs})
    print x
    
main()

