import shapely
from bubo.show import impolygon
from bubo.geometry import apply_homography, bbox_jaccard_overlap
import numpy as np
from time import sleep

def show_homography(hstream):
    for (imfrom, imto, H) in hstream:
        pfrom = np.mat([ [100, imfrom.shape[1]-100, imfrom.shape[1]-100, 100], [100, 100, imfrom.shape[0]-100, imfrom.shape[0]-100] ])
        p = apply_homography(H, pfrom)
        impolygon(imto, np.int32(p.transpose()))
        sleep(1)

def repeatability(imfrom, imto, H, algo):
    """VGG-Affine definition of repeatability given homography"""
    # Measurement
    (fr_ref, d_ref) = algo.descriptors(imfrom)
    (fr_obs, d_obs) = algo.descriptors(imto)        
    k_asgn = algo.assignment(d_ref, d_obs)  # greedy_bipartite_matching(sqdist(d_ref, d_obs))
        
    # Ground truth
    bbox_gt = [apply_homography(H, x) for x in frame_to_bbox(fr_ref)]
    bbox_obs = frame_to_bbox(fr_obs)
    C = bbox_jaccard_overlap(bbox_gt, bbox_obs)

    # Repeatability score
    isvalid = point_in_image(pts, imto)
                
    r = 0
    repeatability.append(r)
    
def virtualworld_benchmark():
    # get range stream
    try:
        db = Viset('iccv11_virtualworld.h5', verbose=True)
    except:
        db = Viset(ICCV11VirtualWorld(verbose=True).export())

    # 
        
    
    
def vggaffine_repeatability_benchmark(vggstreamset, algorithmset, outdir):
    """VGG-Affine repeatability benchmark"""
    for stream in vggstreamset:
        # Repeatability score 
        R = [repeatability(imfrom, imto, H, algo) for (imfrom,imto,H) in stream for algo in algorithmset]

        # Plot repeatability vs. deformation

        # Save results 
