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

# Empirical cumulative distribution function figure
ds = bb.load(glob.glob('BBOB2009pythondata/BIPOP-CMA-ES/ppdata_f0*_20.pickle'))
figure()
bb.pprldistr.plot(ds)
bb.pprldistr.beautify() # resize the window to view whole figure