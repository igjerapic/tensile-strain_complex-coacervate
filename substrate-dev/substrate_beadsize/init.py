import signac

project = signac.get_project() 

# simulation parameters
poly_length =  32
n_polymers = 512
slab_thickness = 16 
epsilon_PS = 3.0

# parameter space
sub_beadsize = [0.8, 1.0]
sub_n_layers = [1, 2]

for layers in sub_n_layers:
    for sigma in sub_beadsize:
        sp = {'epLJ': epsilon_PS, 'L': poly_length, 'D' : slab_thickness, 'T': 1.0, 'N': n_polymers, 
              'subSigma': sigma, 'subLayers': layers , 
              'label': f'N{n_polymers}_L{poly_length}_epLJ{epsilon_PS}'}
        
        job = project.open_job(sp).init()
 
