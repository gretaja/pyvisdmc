import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import h5py
import pandas as pd

import pyvibdmc as pv

sns.set_style("white")

def plot_dist(data_path,molecule,sim_num,walkers,timesteps,start,stop,dist,hist=True,line=True,exp=True):
    """Saves a .png of a histogram and/or line plot of a given distribtion of geometries
      over a specified start and stopping point in the DMC simulation"""
    if molecule == 'h5o3':
        name = 'H5O3'
        num_atoms = 8

    elif molecule == 'h2o':
        name = 'H2O'
        num_atoms = 3

    else:
        raise ValueError('Not a valid molecule name')
    
    if stop > timesteps:
        raise ValueError('Stopping point exceeds length of simulation')
    else:
        pass

    for ind in dist:
        if ind > num_atoms - 1:
            raise ValueError('Atom index exceeds number of atoms in this molecule')
        
        else:
            pass

    path_to_data = f'{data_path}/{molecule}_example_data/1.0w_{walkers}_walkers_{timesteps}t_1dt' #path to the folder containing the simulation data

    sim_data = pv.SimInfo(f'{path_to_data}/{name}_{sim_num}_sim_info.hdf5') #name of the simulation summary file
    snapshots = np.arange(start,stop,1000) #pull data every 1000 time steps from 10,000 to 50,000

    coords, weights = sim_data.get_wfns(snapshots) #load in the molecule geometries (coords) and their associated weights
    coords = pv.Constants.convert(coords,'angstroms',to_AU=False) # conversion of coordinates from atomic units to Angstroms (more common in chemistry)

    analyzer = pv.AnalyzeWfn(coords)

    #df = pd.DataFrame({'weights': dws})

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
    plt.savefig('test_dist.png')
