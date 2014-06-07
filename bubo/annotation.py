"""Annotation tools for ground truthing vision datasets"""

import flickrapi
import flickrapi.shorturl
import urllib
from nltk.corpus import wordnet 
import os
import urllib2
import re

flickr_api_key = os.environ.get('FLICKR_API_KEY')
#flickr = flickrapi.FlickrAPI(flickrapikey, flickrapisecret)

def googlebasicsearch(tag):
    # https://www.google.com/search?q=mortars&safe=off&sout=1&tbm=isch&start=60&sa=N
    pass

    
def googlesearch(tag):

    ##  # Several different User-Agents to diversify the requests.
    ## # Keep the User-Agents updated. Last update: 17th february 14
    ## # Get them here: http://techblog.willshouse.com/2012/01/03/most-common-user-agents/
    ## _UAS = [
    ##     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.73.11 (KHTML, like Gecko) Version/7.0.1 Safari/537.73.11',
    ##     'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.76 Safari/537.36',
    ##     'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:26.0) Gecko/20100101 Firefox/26.0',
    ##     'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36',
    ##     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36',
    ##     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36',
    ##     'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.102 Safari/537.36',
    ##     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.102 Safari/537.36',
    ##     'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11B554a Safari/9537.53',
    ##     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:26.0) Gecko/20100101 Firefox/26.0',
    ##     'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:26.0) Gecko/20100101 Firefox/26.0',
    ##     'Mozilla/5.0 (iPad; CPU OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11B554a Safari/9537.53',
    ##     'Mozilla/5.0 (Windows NT 6.1; rv:26.0) Gecko/20100101 Firefox/26.0',
    ##     'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.76 Safari/537.36'
    ## ]

    ##     Large images: tbs=isz:l
    ## Medium images: tbs=isz:m
    ## Icon sized images: tba=isz:i
    ## Image size larger than 400×300: tbs=isz:lt,islt:qsvga
    ## Image size larger than 640×480: tbs=isz:lt,islt:vga
    ## Image size larger than 800×600: tbs=isz:lt,islt:svga
    ## Image size larger than 1024×768: tbs=isz:lt,islt:xga
    ## Image size larger than 1600×1200: tbs=isz:lt,islt:2mp
    ## Image size larger than 2272×1704: tbs=isz:lt,islt:4mp
    ## Image sized exactly 1000×1000: tbs=isz:ex,iszw:1000,iszh:1000
    ##  Images in full color: tbs=ic:color
    ## Images in black and white: tbs=ic:gray
    ## Images that are red: tbs=ic:specific,isc:red [orange, yellow, green, teal, blue, purple, pink, white, gray, black, brown]
    ## Image type Face: tbs=itp:face
    ## Image type Photo: tbs=itp:photo
    ## Image type Clipart: tbs=itp:clipart
    ## Image type Line drawing: tbs=itp:lineart
    ## Group images by subject: tbs=isg:to
    ## Show image sizes in search results: tbs=imgo:1

    url = 'https://www.google.com/search?tbm=isch&q=%s' % tag.replace(' ','+')
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.49 Safari/537.36'
    headers = {'User-Agent':user_agent,}
    search_request = urllib2.Request(url,None,headers)
    search_results = urllib2.urlopen(search_request)
    search_data = search_results.read()

    datalist = search_data.split('http');
    imlist = [re.findall("^http[s]?://.*\.(?:jpg|gif|png)", 'http'+d) for d in datalist]
    imlist = [im[0] for im in imlist if len(im) > 0]
    imlist_clean = [im for im in imlist if im.find('File:') == -1]
    return imlist_clean

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
        print imfile
        
    
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

  
