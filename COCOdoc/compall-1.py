import urllib
import tarfile
import glob
from pylab import *
import pickle
import bbob_pproc as bb
import bbob_pproc.compall.ppperfprof
import bbob_pproc.bestalg

# Collect and unarchive data
dsets = {}
for alg in bb.compall.ppperfprof.best:
    for date in ('2010', '2009'):
        try:
            dataurl = 'http://coco.lri.fr/BBOB'+date+'/pythondata/' + alg + '.tar.gz'
            filename, headers = urllib.urlretrieve(dataurl)
            archivefile = tarfile.open(filename)
            archivefile.extractall()  # write to disc
            dsets[alg] = bb.load(glob.glob('BBOB'+date+'pythondata/' + alg + '/ppdata_f0*_20.pickle'))
        except:
            pass

# plot the profiles
figure()
# bb.compall.ppperfprof.plotmultiple(dsets, dsref=bb.bestalg.bestalgentries2009)