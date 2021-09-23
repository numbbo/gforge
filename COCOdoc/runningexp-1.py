import os
import fgeneric as fg
import scipy.optimize as so
import numpy as np
datapath = 'data0'
while os.path.exists(datapath):
    datapath = datapath[:4] + str(int(datapath[4:]) + 1)
f = lambda x: sum(i**2 for i in x) # function definition
e = fg.LoggingFunction(datapath=datapath, algid='Nelder-Mead simplex',
              comments='x0 uniformly sampled in [0, 1]^2, '
                       'default settings')
for i in range(15): # 15 repetitions
    e.setfun(fun=f, fopt=0., funId='sphere', iinstance='0')
    so.fmin(e.evalfun, x0=np.random.rand(2)) # algorithm call
    e.finalizerun()
# Display convergence graphs
import bbob_pproc as bb
dsl = bb.load(datapath)
for ds in dsl: ds.plot()