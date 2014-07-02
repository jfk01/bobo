"""Annotation tools for downloading videos from youtube"""

from bobo.annotation import common_user_agents
import os
import urllib2
import re
import random

def search(tag, n_vids=19):
    url = 'https://www.youtube.com/results?search_query=%s&page=%d'
    vidlist = []
    for k in range(1, int(n_vids/20)+2):
        user_agent = random.choice(common_user_agents)
        headers = {'User-Agent':user_agent}
                     
        search_request = urllib2.Request(url % (tag.replace(' ','+'), k), None, headers)
        search_results = urllib2.urlopen(search_request)
        search_data = search_results.read()

        datalist = search_data.split('href="/watch?')
        vidlist.extend(['https://www.youtube.com/watch?%s' % vid.split('"')[0] for vid in datalist if 'DOCTYPE' not in vid.split('"')[0]])
    return vidlist


def download(vidlist):
    pass

def scrape(tag, n_videos):
    pass

