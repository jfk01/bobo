from pyspark import SparkContext
import argparse
import csv
import numpy as np
import math
import matplotlib.pyplot as plt

class CutoffDensity:
    cutoffdist = 0
    def __init__(self,dc):
        self.cutoffdist = dc

    def density(self,dist):
        # initialize to -1 to account for self-distance of 0
        rho = int(-1)
        for d in dist:
            if d<self.cutoffdist:
                rho += 1
        return rho

    def densityParallelized(self,rdd):
        return rdd.map(self.density)

class GaussianDensity:
    cutoffdist = 0
    def __init__(self,dc):
        self.cutoffdist = dc

    def density(self,dist):
        # initialize to exp(0) to account for self-distance of 0
        rho = float(1)
        for d in dist:
            rho += math.exp(-(d*d)/(cutoffdist*cutoffdist))
        return rho

    def densityParallelized(self,rdd):
        return rdd.map(self.density)

# Command line options
parser = argparse.ArgumentParser(description='Cluster data points')
parser.add_argument('--dataset', type=str, help='Dataset for clustering', default='data.csv')
parser.add_argument('--cutoffpercent', type=int, help='Average percentage of data points within cutoff', default=2)
parser.add_argument('--centerthresh', type=int, help='Factor above average distance*density product to choose cluster centers', default=20)
parser.add_argument('--kernel', choices=['gaussian','cutoff'])
parser.add_argument('--output', type=str, help='Output cluster assignment file', default='assignments.csv')

args = parser.parse_args()
print args

cutoffpercent = max(0,min(100,args.cutoffpercent))

# rows are stored as i,j,dist_ij with i/j zero-indexed
# require that only the upper triangular entries in the distance matrix
# are represented in the data file, i.e. there are N(N-1)/2 entries for an NxN
# distance matrix, i.e. len(reader) = N(N-1)/2, solve for N as
# aN^2 + bN + (-2*len(reader)) = 0 with
# a = 1, b = -1, c = -2*len(reader) and N = [-b +/- sqrt(b^2-4ac)]/2a
nrows = 0
N = 0
dist_vec = None
dist_mat = None
with open(args.dataset,'rb') as f:
    reader = csv.reader(f)
    rows = list()
    for row in reader:
        nrows += 1
        rows.append(row)

    N = int((1+math.sqrt(1+8*nrows))/2)

    row_idx = 0
    dist_mat = np.zeros((N,N))
    dist_vec = np.zeros(nrows)
    for row in rows:
        i = int(row[0])
        j = int(row[1])
        dist_ij = float(row[2])
        dist_vec[row_idx] = dist_ij
        dist_mat[i][j] = dist_ij
        dist_mat[j][i] = dist_ij
        row_idx += 1

# sort the distances to find the cutoffdist value
dist_sorted = np.sort(dist_vec)
pos = round(nrows*cutoffpercent/100)
cutoffdist = dist_sorted[pos]

if 'sc' not in locals():
    sc = SparkContext("local[8]", appName='Clustering by fast search and find of density peaks')

# create the RDD
dist_rdd = sc.parallelize(dist_mat)

# map the distances to local densities
if args.kernel=='cutoff' or args.kernel==None:
    print 'Using Cutoff density kernel'
    cutoff_density = CutoffDensity(cutoffdist)
    rho_rdd = cutoff_density.densityParallelized(dist_rdd)
elif args.kernel=='gaussian':
    print 'Using Gaussian density kernel'
    gaussian_density = GaussianDensity(cutoffdist)
    rho_rdd = gaussian_density.densityParallelized(dist_rdd)

rho = np.array(rho_rdd.collect())
ordrho = np.argsort(rho)[::-1]
maxd = dist_sorted[-1]

def calc_delta(item):
    (maxd,ii,ordrho,dist) = item
    min_delta = maxd
    idx_of_min_delta = 0
    iidx = ordrho[ii]
    for jj in range(0,ii):
        jidx = ordrho[jj]
        if dist[jidx] < min_delta:
            min_delta = dist[jidx]
            idx_of_min_delta = jidx

    return min_delta,idx_of_min_delta

items = list()
for idx in range(N):
    items.append((maxd,idx,ordrho,dist_mat[ordrho[idx],:]))

delta_nneigh = sc.parallelize(items).map(calc_delta).collect()

(delta,nneigh) = zip(*delta_nneigh)
delta = np.array(delta) # delta is indexed the same as ordrho
nneigh = np.array(nneigh)
delta[0] = max(delta)
nneigh[0] = 0

plt.plot(rho[ordrho],delta,'ro')
plt.show()

# compute the rho*delta product, so we can pick cluster centers
# compute the threshold for selecting cluster centers as a scaling of the mean
# rho*delta product
gamma = rho[ordrho]*delta
threshold = args.centerthresh*np.mean(gamma)

# select cluster centers as those points whose product is greater than threshold
cluster_centers = list()
cluster_assignments = np.zeros(N)
cluster_id = 0
for i in range(N):
    cluster_assignments[ordrho[i]] = -1
    if gamma[i]>threshold:
        cluster_id += 1
        cluster_centers.append(ordrho[i])
        cluster_assignments[ordrho[i]] = cluster_id

print 'Cluster centers: ' + str(cluster_centers)

# perform the assignment
for i in range(N):
  if cluster_assignments[ordrho[i]] == -1:
      cluster_assignments[ordrho[i]] = cluster_assignments[nneigh[i]]

with open (args.output,'w') as f:
    for i in range(N):
        f.write(str(i) + ',' + str(cluster_assignments[i]) + '\n')

f.close()

