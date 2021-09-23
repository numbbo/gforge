#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import tarfile
from pylab import *
ion() # may be needed for figures to be shown when executing the script

import bbob_pproc as bb

# Collect and unarchive data (3.4MB)
dataurl = 'http://coco.lri.fr/BBOB2009/pythondata/BIPOP-CMA-ES.tar.gz'
filename, headers = urllib.urlretrieve(dataurl)
archivefile = tarfile.open(filename)
archivefile.extractall()

ds = bb.load('BBOB2009pythondata/BIPOP-CMA-ES/ppdata_f002_20.pickle')
d = ds[0] # store the first element of ds in d for convenience

# Plot function evaluations versus target precision
targets = d.evals[:, 0]
evals =  d.evals[:, 1:]
nbrows, nbruns = evals.shape
for i in range(0, nbruns):
    loglog(targets, evals[:, i])
grid()
xlabel('Targets')
ylabel('Function Evaluations')
loglog(d.target[d.target>=1e-8], d.ert[d.target>=1e-8], lw=3,
       color='r', label='ert')
gca().invert_xaxis() # xaxis from the easiest to the hardest
legend() # this operation updates the figure with the inverse axis.
