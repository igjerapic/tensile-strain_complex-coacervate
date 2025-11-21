import signac

project = signac.get_project() 

# simulation parameters
poly_length =  32
n_polymers = 512
slab_thickness = 16 

# parameter space
epsilon_PS = 3.0

sp = {'epLJ': epsilon_PS, 'L': poly_length, 'D' : slab_thickness, 'T': 1.0, 'N': n_polymers, 
      'label': f'N{n_polymers}_L{poly_length}_epLJ{epsilon_PS}'}

job = project.open_job(sp).init()
 
