
###
### This file implements the "Hessian Estimation Evolution Strategy".
### The code is provided under the following license (MIT license):
###
### Copyright 2019-2020 (C) by Tobias Glasmachers.
###
### Permission is hereby granted, free of charge, to any person obtaining a
### copy of this software and associated documentation files (the
### "Software"), to deal in the Software without restriction, including
### without limitation the rights to use, copy, modify, merge, publish,
### distribute, sublicense, and/or sell copies of the Software, and to
### permit persons to whom the Software is furnished to do so, subject to
### the following conditions:
###
### The above copyright notice and this permission notice shall be included
### in all copies or substantial portions of the Software.
###
### THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
### OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
### MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
### IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
### CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
### TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
### SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
###


import numpy as np


def sphere(x):
	return np.dot(x, x);

def ellipsoid(x):
	return np.dot((np.power(1e6, np.linspace(0.0, 1.0, len(x))) * x), x)

def rastrigin(x):
	return 10 * len(x) + np.dot(x, x) - 10 * np.sum(np.cos(2 * np.pi * x))


# Hessian Estimation Evolution Strategy
class HE_ES:
	def __init__(self, fitness, m0, sigma0, pairs = None, lr = 0.5):
		self.fitness = fitness
		self.dim = len(m0)
		self.m = np.copy(m0)
		self.fm = fitness(m0)
		self.best_point = self.m
		self.best_fitness = self.fm
		self.sigma = sigma0
		self.A = np.eye(self.dim)
		self.pairs = pairs if pairs != None else int(2 + 1.5 * np.log(self.dim))
		self.batches = int(np.ceil(float(self.pairs) / float(self.dim)))
		self.vectors = self.batches * self.dim
		self.w = np.linspace(1, 2*self.pairs, 2*self.pairs)
		self.w = np.log(self.pairs + 0.5) - np.log(np.clip(self.w, None, self.pairs + 0.5))
		self.w /= np.sum(self.w)
		self.muEff = 1.0 / np.sum(self.w**2)
		self.symmMuEff = 1.0 / (1.0 / self.muEff - 1.0 / (2.0 * self.pairs - 1.0) * (1.0 - 1.0 / self.muEff))
		self.cs = (self.symmMuEff + 2.0) / (self.dim + self.symmMuEff + 3.0)
		self.ds = 1 + self.cs + 2 * max([0, ((self.muEff - 1) / (self.dim + 1.0))**0.5 - 1])
		self.chi = self.dim**0.5 * (1.0 - 1.0 / (4.0 * self.dim) + 1.0 / (21.0 * self.dim**2))
		self.gs = 0.0
		self.ps = np.zeros(self.dim)
		self.lr_A = lr                   # learning rate for A
		self.maxupdate = 3.0             # update "trust region"
		self.evaluations = 1;
		self.f_spread = np.inf

	def step(self):
		# sample directions
		b = np.random.randn(self.vectors, self.dim)
		norm = np.linalg.norm(b, axis=1)
		for j in range(self.batches):
			# random orthogonal Gaussian vectors
			for i in range(self.dim):
				for u in range(i):
					b[self.dim*j+i] -= np.dot(b[self.dim*j+u], b[self.dim*j+i]) * b[self.dim*j+u]
				b[self.dim*j+i] /= np.linalg.norm(b[self.dim*j+i])
		for k in range(self.vectors):
			b[k] *= norm[k]

		# create offspring
		z = np.append(-b[:self.pairs], b[:self.pairs], axis=0)

		x = self.m + self.sigma * np.transpose(np.dot(self.A, np.transpose(z)))

		# evaluate and rank offspring
		fx = [self.fitness(x[i]) for i in range(2 * self.pairs)]
		self.evaluations += 2 * self.pairs;
		index = np.argsort(fx)
		rank = np.argsort(index)
		if fx[index[0]] < self.best_fitness:
			self.best_fitness = fx[index[0]]
			self.best_point = x[index[0]]
		self.f_spread = np.std(fx)

		# estimate parabolas, update the transformation A (covariance update)
		hess = np.asarray([(fx[self.pairs + i] + fx[i] - 2 * self.fm) / norm[i]**2 for i in range(self.pairs)])
		max_h = np.max(hess)
		if max_h > 0:
			cutoff = max_h / self.maxupdate
			hess = np.maximum(hess, cutoff)
			q = np.log(hess)
			q -= np.mean(q)              # keep unit determinant
			q *= self.lr_A               # apply learning rate
			q *= -0.5                    # inverse square root, since we update A, not H
			eigval = np.exp(q)
			if self.pairs < self.vectors:
				eigval = np.append(eigval, np.ones(self.vectors - self.pairs))
			G = np.zeros((self.dim, self.dim))
			for i in range(self.vectors):
				G += eigval[i] / norm[i]**2 / self.batches * np.outer(b[i], b[i])
			self.A = np.dot(self.A, G)

		# update the mean
		m_new = np.dot(self.w[rank], x)
		self.m = m_new
		self.fm = self.fitness(self.m)
		self.evaluations += 1;
		if self.fm < self.best_fitness:
			self.best_fitness = self.fm
			self.best_point = self.m

		# update the step size (CSA)
		delta_z = np.dot(self.w[rank], z)
		self.gs = (1 - self.cs)**2 * self.gs + self.cs * (2 - self.cs)
		self.ps = (1 - self.cs) * self.ps + np.sqrt(self.cs * (2 - self.cs) * self.symmMuEff) * delta_z
		s = np.sqrt(np.sum(self.ps**2)) / self.chi - np.sqrt(self.gs)
		self.sigma *= np.exp(self.cs / self.ds * s)

# fmin interface with IPOP restarts
def fmin(f, dim, maxevals, pairs = None):
	evals = 0
	best_x = None
	best_f = np.inf
	report = 100 * dim
	while evals < maxevals:
		sigma0 = 2
		opt = HE_ES(f, 6 * np.random.rand(dim) - 3, sigma0, pairs)
		while evals + opt.evaluations < maxevals:
			if evals + opt.evaluations >= report:
				print("  [" + str(report) + "] " + str(min(opt.best_fitness, best_f)))
				report += 100 * dim
			opt.step()
			if opt.f_spread < 1e-9: break
		pairs = 2 * opt.pairs
		if opt.best_fitness < best_f:
			best_x = opt.best_point
			best_f = opt.best_fitness
		evals += opt.evaluations
		if evals < maxevals:
			print("  [" + str(evals) + "] " + str(min(opt.best_fitness, best_f)) + "   -- restarting with " + str(pairs) + " pairs")
	print("  [" + str(report) + "] " + str(best_f))
	return (best_x, best_f)


# example invocation
dim = 10
f = rastrigin
maxevals = 10000 * dim
result = fmin(f, dim, maxevals)
print("best point:", result[0])
print("best function value:", result[1])
