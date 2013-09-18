import flickrapi
import flickrapi.shorturl
import xml.etree.ElementTree as ET
import urllib
from nltk.corpus import wordnet 


flickr_api_key = '4cec3869bc47a39f049ee19628824e18'  # jebyrne

def search(searchtag):
  flickr = flickrapi.FlickrAPI(flickr_api_key)
  photos = flickr.walk(text=searchtag,per_page='500')  
  return photos

def test_flickr_download():
  tag = 'bumblebee'
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
    
if __name__ == '__main__':
  basic_level_categories()
  

# http://stuvel.eu/media/flickrapi-docs/documentation/
# pip-2.7 install flickrapi
# http://www.flickr.com/services/api/misc.urls.html
# http://www.flickr.com/services/developer/api/
# 3600 queries per hour per key
# http://www.flickr.com/services/api/flickr.photos.search.html
# http://wordnet.princeton.edu/man/lexnames.5WN.html
# freebase.com
# https://pypi.python.org/pypi/pyimgur/0.3.2

  
