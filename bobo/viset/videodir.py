import os
import csv
from bobo.cache import Cache
from bobo.video import VideoCategoryStream
from bobo.util import remkdir, isexe, isvideo


def videolist(viddir=None):
    return [os.path.join(viddir, filename) for filename in os.listdir(viddir) if isvideo(filename)]

def frames(viddir):
    for v in videolist(viddir):
        (outdir, ext) = os.path.splitext(v)
        cmd = "ffmpeg -i \'%s\' %s/%%08d.png &> /dev/null" % (v, remkdir(outdir))
        print '[bobo.viset.videodir]: exporting frames from "%s" to "%s"' % (v, outdir)
        os.system(cmd)
