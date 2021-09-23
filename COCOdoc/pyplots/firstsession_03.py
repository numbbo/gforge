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

# Plot target precision versus function evaluations with error bars
targets = d.evals[:, 0]
evals =  d.evals[:, 1:]
from bbob_pproc.toolsstats import prctile
q = array(list(prctile(i, [25, 50, 75]) for i in evals))
xmed = q[:, 1]
xlow = xmed - q[:, 0]
xhig = q[:, 2] - xmed
xerr = vstack((xlow, xhig))
errorbar(xmed, targets, xerr=xerr, color='r', label='Median')
xscale('log')
yscale('log')
xlabel('Function Evaluations')
ylabel('Targets')
grid()
legend()
