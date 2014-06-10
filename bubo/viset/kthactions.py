import os
import csv
from bubo.cache import Cache
from bubo.video import VideoCategoryStream
from bubo.util import remkdir

URLS = ['http://www.nada.kth.se/cvap/actions/walking.zip',
        'http://www.nada.kth.se/cvap/actions/jogging.zip',
        'http://www.nada.kth.se/cvap/actions/running.zip',
        'http://www.nada.kth.se/cvap/actions/boxing.zip',
        'http://www.nada.kth.se/cvap/actions/handwaving.zip',
        'http://www.nada.kth.se/cvap/actions/handclapping.zip']
SHA1 = ['a3e81537271a0ab4576591774baa38c2d97b7e3a',
        '21943bdbcef9dad106db0d74661e49eaeaa15a25',
        'da83bb313edfd4455fffdda6263696fa10d43c6f',
        'adb36ed9c29c846d44d2ba15f348bd115c951bbd',
        '0792f7cd69f7f895a205c08ac212ddaa7177e370',
        'd3b81261aa822ef63d0d1523f945bfaff27814d2']
LABELS = ['walking','jogging','running','boxing','handwaving','handclapping']
VISET = 'kthactions'

cache = Cache(subdir=VISET)

    


def export_videolist(outdir):
    vidlist = []
    for (idx_category, category) in enumerate(os.listdir(indir)):
        if os.path.isdir(os.path.join(indir, category)):
            for (idx_video, filename) in enumerate(os.listdir(os.path.join(indir, category))):    
                [avibase,ext] = os.path.splitext(filename)
                if ext == '.avi':
                    vidlist.append( (os.path.join(category, filename), category) )
    return vidlist


def export(outdir=None, clean=False):
    # Unpack dataset
    if outdir is not None:
        cache.setroot(outdir)
    if clean:
        cache.clean()
                        
    print '[bubo.viset.kthactions][WARNING]: downloads will not show percent progress since content length is unknown'
    for (url, label, sha1) in zip(URLS, LABELS, SHA1):
        cache.unpack(cache.get(url, sha1), cache.abspath(label), cleanup=False)

    # Check for frame export utility
    if not bubo.util.isexe('ffmpeg'):
        raise IOError('[bubo.viset.kthactions]: ffmpeg not found on path')
                    
    # Video list
    outfile = cache.abspath('%s.csv' % VISET)        
    with open(outfile, 'wb') as csvfile:
        f = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)                   
        for (idx_category, category) in enumerate(os.listdir(cache.root())):
            if os.path.isdir(os.path.join(cache.root(), category)):
                for (idx_video, filename) in enumerate(os.listdir(os.path.join(cache.root(), category))):    
                    [avibase,ext] = os.path.splitext(filename)
                    if ext == '.avi':
                        imdir = cache.abspath(os.path.join(category, avibase))                        
                        print '[bubo.viset.kthactions]: exporting "%s" to "%s"' % (filename, imdir)
                        f.writerow([os.path.join(category, avibase, 'im_%08d.png'), category]);                                        
                        cmd = "ffmpeg -i \'%s\' %s/im_%%08d.png &> /dev/null" % (os.path.join(cache.root(), category, filename), imdir)
                        remkdir(imdir)                        
                        if os.system(cmd) != 0:
                            raise IOError('Error running ffmpeg')
    return outfile

def stream(outdir=None):
    if outdir is not None:
        cache.setroot(outdir)
    csvfile = os.path.join(cache.root(), '%s.csv' % VISET)            
    if not os.path.isfile(csvfile):
        csvfile = export()        
    return VIdeoCategoryStream(csvfile, cache=cache)
        

