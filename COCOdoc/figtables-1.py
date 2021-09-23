import urllib
import tarfile
import glob
from pylab import *

import bbob_pproc as bb

# Collect and unarchive data (3.4MB)
dataurl = 'http://coco.lri.fr/BBOB2009/pythondata/BIPOP-CMA-ES.tar.gz'
filename, headers = urllib.urlretrieve(dataurl)
archivefile = tarfile.open(filename)
archivefile.extractall()

# Scaling figure
ds = bb.load(glob.glob('BBOB2009pythondata/BIPOP-CMA-ES/ppdata_f002_*.pickle'))
figure()
bb.ppfigdim.plot(ds)
bb.ppfigdim.beautify()
bb.ppfigdim.plot_previous_algorithms(2) # plot BBOB 2009 best algorithm on fun 2