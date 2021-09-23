import urllib
import tarfile
import glob
from pylab import *
import pickle
import bbob_pproc as bb
import bbob_pproc.compall.pprldmany
import bbob_pproc.algportfolio

# Collect and unarchive data
dsets = {}
for alg in ('BIPOP-CMA-ES', 'NEWUOA'):
    dataurl = 'http://coco.lri.fr/BBOB2009/pythondata/' + alg + '.tar.gz'
    filename, headers = urllib.urlretrieve(dataurl)
    archivefile = tarfile.open(filename)
    archivefile.extractall()  # write to disc
    dsets[alg] = bb.load(glob.glob('BBOB2009pythondata/' + alg + '/ppdata_f0*_20.pickle'))

# Generate the algorithm portfolio
dspf = bb.algportfolio.build(dsets)
dsets['Portfolio'] = dspf # store the portfolio in dsets

# plot the run lengths distribution functions
figure()
for algname, ds in dsets.iteritems():
    bb.compall.pprldmany.plot(ds, label=algname)
bb.compall.pprldmany.beautify()
legend(loc='best') # Display legend