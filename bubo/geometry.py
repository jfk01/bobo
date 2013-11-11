import numpy as np
import cv2

def dehomogenize(p):
    return np.float32(p[0:-1, :]) / np.float32(p[-1,:])

def homogenize(p):
    return np.float32(np.vstack( (p, np.ones((1,p.shape[1]))) ))

def apply_homography(H,p):
    return dehomogenize(H*homogenize(p))

def similarity_imtransform(txy=(0,0), r=0, s=1):
    R = np.mat([[np.cos(r), -np.sin(r), 0], [np.sin(r), np.cos(r), 0], [0,0,1]])
    S = np.mat([[s,0,0], [0, s, 0], [0,0,1]])
    T = np.mat([[0,0,txy[0]], [0,0,txy[1]], [0,0,0]])
    return S*R + T  # composition

def affine_imtransform(txy=(0,0), r=0, sx=1, sy=1, kx=0, ky=0):
    R = np.mat([[np.cos(r), -np.sin(r), 0], [np.sin(r), np.cos(r), 0], [0,0,1]])
    S = np.mat([[sx,0,0], [0, sy, 0], [0,0,1]])
    K = np.mat([[1,ky,0], [kx,1,0], [0,0,1]])
    T = np.mat([[0,0,txy[0]], [0,0,txy[1]], [0,0,0]])
    return K*S*R + T  # composition

def random_affine_imtransform(txy=((0,0),(0,0)), r=(0,0), sx=(1,1), sy=(1,1), kx=(0,0), ky=(0,0)):
    return affine_imtransform(txy=(uniform_random_in_range(txy[0]), uniform_random_in_range(txy[1])),
                              r=uniform_random_in_range(r),
                              sx=uniform_random_in_range(sx),
                              sy=uniform_random_in_range(sy),
                              kx=uniform_random_in_range(kx),
                              ky=uniform_random_in_range(ky))

def imtransform(im, A):
    # cv2.warpPerspective(src, M, dsize[, dst[, flags[, borderMode[, borderValue]]]]) -> dst
    return cv2.warpPerspective(im, A, im.shape)
