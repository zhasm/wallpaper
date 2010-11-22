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

def getTotal(content):
    '''Get the total page number and total wallpaper number'''  
    #<b style="color: #bb2f0e;">page 2 of 226</b>
    wps=0
    pages=0
    try:
        wps=re.search(r'''(?<=<b style="color: #bb2f0e;">)\b(\d+)\b(?=</b>)''', content)
        if wps:
            wps=wps.group(1)
    except:
        wps=-1
    
    try:
        pages=re.search(r'''#bb2f0e;">page \d+ of (\d+)''', content)
        if pages:
            pages=pages.group(1)
    except:
        pages=-1
    return (wps, pages)
    
    #get parameter from url:
def get_V(p, regex=None):
    """return cgi GET parameter; strip white spaces at both ends if any; 
    if verify pattern provided, do match test; only return matched values.
    Note: it uses re.match to check , not re.search.
    """
    import cgi
    form = cgi.FieldStorage()
    value= form.getfirst(p)

    if not value:
        return None
    value=value.strip()


    if regex is not None:
        import re
        if re.match(regex+"$",value):
            return value
        else:
            return None
    else:
         return value

def main():
    pageNo=get_V("page");
    if not pageNo:
        pageNo="1";
    url="http://interfacelift.com/wallpaper_beta/downloads/date/any/index%s.html" % pageNo
    
    page=online_open(url)
    imgs=getPreviewImgs(page)
    (wps, pages) = getTotal(page)
    print "content-type: application/json\n"

    print json.dumps({"imgs": imgs, 'wallpapers':wps, 'pages':pages})
    
    
main() 
