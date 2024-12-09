import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("white")

def plot_2d(molecule,sim_num,analyzer,weights,dists,exp=True):
    """Saves a .png of a 2D histogram of a given distribtion of geometries
      over a specified start and stopping point in the DMC simulation"""
    if molecule == 'h5o3':
        num_atoms = 8

    elif molecule == 'h2o':
        num_atoms = 3

    else:
        raise ValueError('Not a valid molecule name')
    
    for d in range(len(dists)):
        for ind in dists[d]:
            if ind > num_atoms - 1:
                raise ValueError('Atom index exceeds number of atoms in this molecule')
        
            else:
                pass

    if len(dists) != 2:
        raise ValueError('"dists" must be a list of two pairs of atom indices')
    else:
        pass

    print(f"Creating plot two_d_dist for dists {dists} for {molecule}...")

    dist_vals = []
    exp_vals = []
    for dist in dists:
        distance = analyzer.bond_length(dist[0],dist[1]) #calculates the distance between the first two atoms in the coordinates array, which correspond to the hydroxide ion
        dist_vals.append(distance)

        exp_val = analyzer.exp_val(distance,weights) #calculates the expectation value (average) of the quantity
        exp_vals.append(exp_val)

    
    sns.histplot(x=dist_vals[0], y=dist_vals[1],cbar=True) #normalizes the distribution so the total probability is 1

    #plot a point corresponding to the 2 expectation values
    if exp==True:
        plt.scatter(exp_vals[0],exp_vals[1],label='Exp. Vals.')
        plt.legend()
    else:
        pass

    plt.xlabel(rf'{dists[0][0]}{dists[0][1]} Distance ($\AA$)')
    plt.ylabel(rf'{dists[1][0]}{dists[1][1]} Distance ($\AA$)')
    plt.savefig(f'{molecule}_sim_{sim_num}_2d.png',bbox_inches='tight')

    plt.clf()
