import os
import csv
from bobo.cache import Cache
from bobo.video import VideoCategoryStream
from bobo.util import remkdir, isexe, isvideo
import shutil

def videolist(viddir=None):
    return [os.path.join(viddir, filename) for filename in os.listdir(viddir) if isvideo(filename)]

def frames(viddir):
    for v in videolist(viddir):
        (outdir, ext) = os.path.splitext(v)
        cmd = 'ffmpeg  -r 25 -i \'%s\' -vf "scale=-1:240" %s/%%07d.jpg &> /dev/null' % (v, remkdir(outdir))        
        print '[bobo.viset.videodir]: exporting frames from "%s" to "%s"' % (v, outdir)
        os.system(cmd)

def clean(viddir):
    for v in videolist(viddir):
        (outdir, ext) = os.path.splitext(v)
        if os.path.isdir(outdir):
            print '[bobo.viset.videodir]: removing frame directory "%s"' % (outdir)            
            shutil.rmtree(outdir)
        
