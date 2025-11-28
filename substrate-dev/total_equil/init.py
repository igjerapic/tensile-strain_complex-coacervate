import signac

project = signac.get_project() 

# simulation parameters
tempFinal = 1.0
poly_length =  32
n_polymers = 512
slab_thickness = 16 
n_subLayers = 1

# parameter space
wallPots = ["LJ93", "LJ126", "LJ1043"]
epsilon_PS = [1.0, 2.0, 3.0]
subSigmas = [0.8, 1.0]
charged = ["True", "False"]

for epsilon in epsilon_PS:
    for chargeLabel in charged:
        for wallPot in wallPots:
            for subSigma in subSigmas:
                sp = {'wallPot': wallPot, 'subSigma': subSigma, 'epLJ': epsilon, 'subLayers': n_subLayers, 
                      'L': poly_length, 'D' : slab_thickness, 'T': tempFinal, 'N': n_polymers, "isCharged": chargeLabel,
                      'label': f'N{n_polymers}_L{poly_length}_epLJ{epsilon}'}

                job = project.open_job(sp).init()
 
