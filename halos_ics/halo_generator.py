# Hacked version of NFW halo generation code from:
# https://github.com/poveda-ruiz/HaloGenerator/blob/master/src/new/main.py
"""
Code to generate ICs of the *positions* of various halo profiles.


usage: python3 halos_ics.py n_particles r_scale rvir file_name

dependencies: numpy, sys, emcee

author: Nico Garavito 
github: jngaravitoc

"""


import numpy as np
import emcee 
import sys

# Input paramters:

n = int(sys.argv[1])
a = int(sys.argv[2])
rcut = int(sys.argv[3])
M = float(sys.argv[4])
filename = sys.argv[5]

def lnprob_nfw(r,a):
    # a is concentration here
    if 1 > r > 0:
        return np.log(r/((1+r*a)*(1+r*a)))
    return -np.inf


def lnprob_hern(r,a):
    if 1 > r > 0:
        return np.log(1/(r*(1+r/a)**3))
    return -np.inf


ndim, nwalkers = 1, 2
p0 = [[0.01],[0.09]]

sampler = emcee.EnsembleSampler(nwalkers, ndim, lnprob_hern, args=[a])
# n/2 in the "burn-in"

sampler.run_mcmc(p0, n/2)
#sampler.reset()


r = np.concatenate((sampler.chain[0],sampler.chain[1]))
print(len(r))
#r = np.sort(r)
r = [x[0] for x in r]


theta = np.arccos(2*np.random.random(n)-1)
phi =  2.0 * np.pi * np.random.random(n)

x = r * np.sin(theta) * np.cos(phi) * rcut
y = r * np.sin(theta) * np.sin(phi) * rcut
z = r * np.cos(theta) * rcut

m_part = np.ones(len(x))*M/len(x)

f = open(filename, 'w')
for i in range(len(x)):
    f.write('%f \t %f \t %f \t %f \n'%(x[i], y[i], z[i], m_part[i]))
f.close()

print("Mean acceptance fraction: {0:.3f}".format(np.mean(sampler.acceptance_fraction)))
#if __name__ == "__main__":

