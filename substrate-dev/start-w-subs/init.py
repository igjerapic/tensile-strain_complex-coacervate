import signac

project = signac.get_project() 

# simulation parameters
tempFinal = 1.0
poly_length =  32
n_polymers = 512
bulk_density = 0.9 
n_subLayers = 1

# parameter space
epsilon_PS = [1.0, 2.0, 3.0]
subSigmas = [0.8, 1.0]
charged = ["charged", "neutral"]

# epsilon = 3.0
# subSigma = 0.8
# chargeLabel = "charged"
# sp = {'subSigma': subSigma, 'epLJ': epsilon, 'subLayers': n_subLayers, 
#       'L': poly_length, 'rho_bulk': bulk_density, 'T': tempFinal, 'N': n_polymers, "charge": chargeLabel,
#       'label': f'L{poly_length}_subSigma{subSigma}_{chargeLabel}_epLJ{epsilon}'}
# job = project.open_job(sp).init()
for epsilon in epsilon_PS:
    for chargeLabel in charged:
            for subSigma in subSigmas:
                sp = {'subSigma': subSigma, 'epLJ': epsilon, 'subLayers': n_subLayers, 
                      'L': poly_length, 'rho_bulk': bulk_density, 'T': tempFinal, 'N': n_polymers, "charge": chargeLabel,
                      'label': f'L{poly_length}_subSigma{subSigma}_{chargeLabel}_epLJ{epsilon}'}
                job = project.open_job(sp).init()
 
