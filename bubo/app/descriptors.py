import shapely
from bubo.show import impolygon
from bubo.geometry import apply_homography

def vgg_affine(hstream):
    for (imfrom, imto, H) in hstream:
        pfrom = np.mat([ [100, imfrom.shape[1]-100, imfrom.shape[1]-100, 100], [100 100 imfrom.shape[0]-100 imfrom.shape[0]-100] ])
        pto = apply_homography(H, pfrom)
        impolygon(imto, p)
        pass


http://toblerity.org/shapely/manual.html
http://pythonhosted.org/planar/index.html  (NO)
http://www.cmake.org/Wiki/VTK/Examples/Cxx ?
http://www.boost.org/doc/libs/1_54_0/libs/polygon/doc/index.htm ?
http://rk700.github.io/python-fitz/rect.html
python cgal

use shapely (geos) with pairwise computation and kdtree and range search
(or exhaustive)


    
