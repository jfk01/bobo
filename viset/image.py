from viset.cache import CachedObject


class AnnotatedImage(CachedObject):
    _category = None
    _bbox = None

    def annotation(self, category, bbox=None):
        self._category = category
        self._bbox = bbox
        return self
    
    def __repr__(self):
        return str('<viset.image: category=\'' + str(self._category) + '\', cached=' + str(self._cache.iscached(self._url)) + ', URL=\'' + str(self._url) + '\'>')        


