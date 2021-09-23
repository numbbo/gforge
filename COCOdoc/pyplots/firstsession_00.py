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
budgets = d.funvals[:, 0] # stores first column in budgets
funvals = d.funvals[:, 1:] # stores all other columns in funvals

nbrows, nbruns = funvals.shape
for i in range(0, nbruns):
    loglog(budgets, funvals[:, i])
grid()
xlabel('Budgets')
ylabel('Best Function Values')
loglog(budgets, median(funvals, axis=1), linewidth=3, color='r',
       label='median')
legend() # display legend

dataurl = 'http://coco.lri.fr/BBOB2009/pythondata/NEWUOA.tar.gz'
filename, headers = urllib.urlretrieve(dataurl)
archivefile = tarfile.open(filename)
archivefile.extractall()

ds1 = bb.load('BBOB2009pythondata/NEWUOA/ppdata_f002_20.pickle')
d1 = ds1[0]
budgets1 = d1.funvals[:, 0]
funvals1 = d1.funvals[:, 1:]
for i in range(0, funvals1.shape[1]):
    loglog(budgets1, funvals1[:, i], linestyle='--')
loglog(budgets1, median(funvals1, axis=1), linewidth=3, color='g',
       label='median NEWUOA')
legend() # updates legend
