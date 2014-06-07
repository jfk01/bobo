"""Annotation tools for ground truthing vision datasets"""

import flickrapi
import flickrapi.shorturl
import urllib
from nltk.corpus import wordnet 
import os
import urllib2
import re
import random
import math

flickr_api_key = os.environ.get('FLICKR_API_KEY')
#flickr = flickrapi.FlickrAPI(flickrapikey, flickrapisecret)

common_user_agents = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.73.11 (KHTML, like Gecko) Version/7.0.1 Safari/537.73.11',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.76 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:26.0) Gecko/20100101 Firefox/26.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.102 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.102 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11B554a Safari/9537.53',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:26.0) Gecko/20100101 Firefox/26.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:26.0) Gecko/20100101 Firefox/26.0',
    'Mozilla/5.0 (iPad; CPU OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11B554a Safari/9537.53',
    'Mozilla/5.0 (Windows NT 6.1; rv:26.0) Gecko/20100101 Firefox/26.0',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.76 Safari/537.36'
]


def basicgooglesearch(tag, n_imgs):
    url = 'https://www.google.com/search?q=%s&safe=off&sout=1&tbm=isch&start=%d&sa=N' 
    fulllist = []
    for k in range(20, int(n_imgs), 20):
        user_agent = random.choice(common_user_agents)
        headers = {'User-Agent':user_agent}
                     
        search_request = urllib2.Request(url % (tag.replace(' ','+'), k), None, headers)
        search_results = urllib2.urlopen(search_request)
        search_data = search_results.read()

        # FIXME: use gstatic.com URLs instead of .jpg
        datalist = search_data.split('http');
        imlist = [re.findall("^http[s]?://.*\.(?:jpg|gif|png)", 'http'+d) for d in datalist]
        imlist = [im[0] for im in imlist if len(im) > 0]
        imlist_clean = [im for im in imlist if im.find('File:') == -1]
        fulllist.append(imlist_clean)
    return fulllist
    
def googlesearch(tag):
    url = 'https://www.google.com/search?tbm=isch&q=%s' % tag.replace(' ','+')
    user_agent = random.choice(common_user_agents)
    headers = {'User-Agent':user_agent}
    search_request = urllib2.Request(url,None,headers)
    search_results = urllib2.urlopen(search_request)
    search_data = search_results.read()

    # FIXME: support for gstatic.com URLs
    datalist = search_data.split('http');
    imlist = [re.findall("^http[s]?://.*\.(?:jpg|gif|png)", 'http'+d) for d in datalist]
    imlist = [im[0] for im in imlist if len(im) > 0]
    imlist_clean = [im for im in imlist if im.find('File:') == -1]

    imlist = [re.findall(ur'^http[s]?://.*gstatic.*?"[ ,]', ('http'+d).decode('utf-8'), re.UNICODE) for d in datalist]  # unicode double quote?
    imlist = [im[0][:-2] for im in imlist if len(im) > 0]
    imlist2_clean = [im for im in imlist if im.find('File:') == -1]    
    return imlist_clean + imlist2_clean

def search(searchtag):
    flickr = flickrapi.FlickrAPI(flickr_api_key)
    photos = flickr.walk(text=searchtag,per_page='500')  
    return (photos, flickr)

def download(tag='owl'):
    (photos, flickr) = search(tag)
    for img in photos:        
        id = img.get('id')
        info = flickr.photos_getInfo(photo_id=id)    
        url = 'http://farm'+img.get('farm')+'.staticflickr.com/'+img.get('server')+'/'+img.get('id')+'_'+img.get('secret')+'_n.jpg'
        imfile = "/tmp/"+tag.replace(',','_')+"_"+id+".jpg"
        urllib.urlretrieve(url, imfile)
        
    
def basic_level_categories():
    # nltk.download(), install wordnet in /Users/jebyrne/.nltk, 
    # set NLTK_DATA environment variable to /Users/jebyrne/.nltk
    nouns = []
    allowed_lexnames = ['noun.animal', 'noun.artifact', 'noun.body', 'noun.food', 'noun.object', 'noun.plant']
    for synset in list(wordnet.all_synsets('n')):
        if synset.lexname in allowed_lexnames:
            nouns.append(synset.lemmas[0].name)  
            #print synset.lemma_names  # synonyms
            #nouns.append(synset.name)      
    nouns.sort()
    print nouns
    print len(nouns)


# A synset is a synonym set for cognitively equivalent words
# A synset is uniquely identified by a part of speech and an offset
# wordnet._synset_from_pos_and_offset('n', 2115096)
# wordnet.synset('dog.n.01')
# the synset is identified by name.part_of_speech.sense_index

# image-net popularity percentile is based on google searches and frequency in british national corpus

  

# http://stuvel.eu/media/flickrapi-docs/documentation/
# pip-2.7 install flickrapi
# http://www.flickr.com/services/api/misc.urls.html
# http://www.flickr.com/services/developer/api/
# 3600 queries per hour per key
# http://www.flickr.com/services/api/flickr.photos.search.html
# http://wordnet.princeton.edu/man/lexnames.5WN.html
# freebase.com
# https://pypi.python.org/pypi/pyimgur/0.3.2

# pylabelme

  
