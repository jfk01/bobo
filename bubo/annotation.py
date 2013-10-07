"""Annotation tools for ground truthing vision datasets"""

import flickrapi
import flickrapi.shorturl
import urllib
from nltk.corpus import wordnet 


flickr_api_key = os.environ.get('FLICKR_API_KEY')


def search(searchtag):
    flickr = flickrapi.FlickrAPI(flickr_api_key)
    photos = flickr.walk(text=searchtag,per_page='500')  
    return photos

def download(tag='owl'):
    photos = search(tag)
    for img in photos:
        print ET.tostring(img)
        id = img.get('id')
        info = flickr.photos_getInfo(id)    
        url = 'http://farm'+img.get('farm')+'.staticflickr.com/'+img.get('server')+'/'+img.get('id')+'_'+img.get('secret')+'_n.jpg'
        urllib.urlretrieve(url, "/tmp/"+tag+"_"+id+".jpg")

    
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

  
