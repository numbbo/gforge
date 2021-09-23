import fgeneric
import scipy.optimize as so
import numpy as np
import os
datapath = 'ellipsoid0'
while os.path.exists(datapath):
    datapath = datapath[:9] + str(int(datapath[9:]) + 1) 
fun = fgeneric.LoggingFunction(datapath=datapath, algid='BFGS',
              comments='x0 uniformly sampled in [0, 1]^5, default settings')
cond_num = 10 ** np.arange(0, 7)
for c in cond_num:
    f = lambda x: np.sum(c ** np.linspace(0, 1, len(x)) * x ** 2)
    # function definition: these are term-by-term operations
    for i in range(5): # 5 repetitions
        fun.setfun(fun=f, fopt=0., funId='ellipsoid', iinstance=0,
                 condnum=c)
        so.fmin_bfgs(fun.evalfun, x0=np.random.rand(5)) # algorithm call
        fun.finalizerun()
import bbob_pproc as bb
import bbob_pproc.ppfigparam
ds = bb.load(datapath)
bb.ppfigparam.plot(ds, param='condnum')
bb.ppfigparam.beautify()
import matplotlib.pyplot as plt
plt.xlabel('Condition Number')
