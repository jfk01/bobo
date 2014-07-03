"""Annotation tools for downloading videos from youtube"""

from bobo.annotation import common_user_agents
import os
import urllib2
import re
import random
from bobo.util import tofilename, remkdir

def youtube(tag, n_pages=1, outdir=None):
    url = 'https://www.youtube.com/results?search_query=%s&page=%d'
    vidlist = []
    for k in range(0, n_pages):
        user_agent = random.choice(common_user_agents)
        headers = {'User-Agent':user_agent}
                     
        search_request = urllib2.Request(url % (tag.replace(' ','+'), k+1), None, headers)
        search_results = urllib2.urlopen(search_request)
        search_data = search_results.read()

        datalist = search_data.split('href="/watch?')
        vidlist.extend(['https://www.youtube.com/watch?%s' % vid.split('"')[0] for vid in datalist if 'DOCTYPE' not in vid.split('"')[0]])
    vidlist = list(set(vidlist))  # unique

    if outdir is not None:
        download(vidlist, os.path.join(remkdir(outdir), 'youtube_'+tofilename(tag)+'_%04d.mp4')) 
    return(vidlist)

def liveleak(tag, n_pages=1, outdir=None):
    url = 'http://www.liveleak.com/browse?q=%s&page=%d'
    vidlist = []
    for k in range(0, n_pages):
        user_agent = random.choice(common_user_agents)
        headers = {'User-Agent':user_agent}
                     
        search_request = urllib2.Request(url % (tag.replace(' ','+'), k+1), None, headers)
        search_results = urllib2.urlopen(search_request)
        search_data = search_results.read()

        datalist = search_data.split('href="http://www.liveleak.com/view?')
        vidlist.extend(['http://www.liveleak.com/view?%s' % vid.split('"')[0].split('&')[0] for vid in datalist if 'DOCTYPE' not in vid.split('"')[0]])
    vidlist = list(set(vidlist))  # unique

    if outdir is not None:
        download(vidlist, os.path.join(remkdir(outdir), 'liveleak_'+tofilename(tag)+'_%04d.mp4')) 
    return(vidlist)
    

def download(vidlist, outfile):
    """Use youtube-dl to download videos from url"""
    for (k,v) in enumerate(vidlist):
        try:
            print '[bobo.youtube.download]: exporting "%s" to "%s"' % (v, outfile % k)
            os.system('youtube-dl "%s" -o %s' % (v, outfile % k))  # must be on path
        except:
            print '[bobo.youtube.download]: download failed - skipping'

