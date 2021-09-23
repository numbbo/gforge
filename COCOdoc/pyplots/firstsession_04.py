#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import tarfile
import glob
from pylab import *
ion() # may be needed for figures to be shown when executing the script

import bbob_pproc as bb

# Collect and unarchive data (3.4MB)
dataurl = 'http://coco.lri.fr/BBOB2009/pythondata/BIPOP-CMA-ES.tar.gz'
filename, headers = urllib.urlretrieve(dataurl)
archivefile = tarfile.open(filename)
archivefile.extractall()

# Empirical cumulative distribution function figure
from bbob_pproc import pprldistr
ds = bb.load(glob.glob('BBOB2009pythondata/BIPOP-CMA-ES/ppdata_f0*_20.pickle'))
figure()
pprldistr.plot(ds)
pprldistr.beautify() # resize the window to view whole figure
