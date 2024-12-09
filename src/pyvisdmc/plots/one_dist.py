import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("white")

def plot_dist(molecule,analyzer,weights,dist,hist=True,line=True,exp=True):
    """Saves a .png of a histogram and/or line plot of a given distribtion of geometries
      over a specified start and stopping point in the DMC simulation"""
    if molecule == 'h5o3':
        num_atoms = 8

    elif molecule == 'h2o':
        num_atoms = 3

    else:
        raise ValueError('Not a valid molecule name')

    for ind in dist:
        if ind > num_atoms - 1:
            raise ValueError('Atom index exceeds number of atoms in this molecule')
        
        else:
            pass
    
    print(f"Creating plot one_dist for dist {dist} for {molecule}...")
    
    distance = analyzer.bond_length(dist[0],dist[1]) #calculates the distance between the first two atoms in the coordinates array, which correspond to the hydroxide ion

    exp_val = analyzer.exp_val(distance,weights) #calculates the expectation value (average) of the quantity

    if hist==True:
        if line==True:
            sns.histplot(distance, kde=True, bins=50,label=f'{dist[0]}{dist[1]}') #normalizes the distribution so the total probability is 1
        else:
            sns.histplot(distance, kde=False, bins=50,label=f'{dist[0]}{dist[1]}')

    else:
        sns.kdeplot(distance,label=f'{dist[0]}{dist[1]}')

    #plot a vertical line where the average value is
    if exp==True:
        plt.vlines(exp_val,0,6,label=rf'$\langle${dist[0]}{dist[1]}$\rangle$ = {exp_val:.4f} $\AA$')
    else:
        pass

    plt.xlabel(r'Bond Length ($\AA$)')
    plt.ylabel('Probability Amplitude')
    plt.savefig(f'{molecule}_{dist[0]}{dist[1]}_dist.png',bbox_inches='tight')

    plt.clf()
