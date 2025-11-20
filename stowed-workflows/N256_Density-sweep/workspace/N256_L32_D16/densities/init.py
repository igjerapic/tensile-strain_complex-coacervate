import os

import signac
import numpy as np

project = signac.init_project() # initializes project in current working dir

# simulation parameters
poly_length =  32
n_polymers = 256
slab_thickness = 16 

# parameter space
epsilon_PS = [0.5, 1.0, 2.0, 3.0]
min_density = 0.84
max_density = 1.2
density_step = 0.02

n_densities = int((max_density - min_density)/density_step) + 1
densities = list(np.linspace(min_density, max_density, n_densities, dtype = float))
slab_density = [round(rho, 2) for rho in densities]

for rho in slab_density:
    for epsilon in epsilon_PS:
        sp = {'rho': rho , 'epLJ': epsilon, 'N': poly_length, 'D' : slab_thickness, 'T': 1.0, 'N_polymers': n_polymers, 
              'label': f'N{poly_length}_rho{rho}-epLJ{epsilon}'}
        job = project.open_job(sp).init()
 
