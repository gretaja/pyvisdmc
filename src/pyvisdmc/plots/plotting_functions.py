"""Plotting functions for DMC analysis"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import h5py
import pandas as pd

import pyvibdmc as pv

sns.set_style("white")

#path_to_data = '../data/h5o3_example_data/1.0w_50000_walkers_50000t_1dt' #path to the folder containing the simulation data

def plot_eref(data_path,molecule,sim_num,walkers,timesteps,start,stop):
    if molecule == 'h5o3':
        name = 'H5O3'

    elif molecule == 'h2o':
        name = 'H2O'

    path_to_data = f'{data_path}/{molecule}_example_data/1.0w_{walkers}_walkers_{timesteps}t_1dt' #path to the folder containing the simulation data

    sim_data = pv.SimInfo(f'{path_to_data}/{name}_{sim_num}_sim_info.hdf5') #name of the simulation summary file

    #start = 10000 #where we want to start averaging the energy from
    #stop = 50000 #where we want to average until

    vref = sim_data.get_vref(ret_cm=True) #generates an array of the timesteps and the average energy of the ensemble at that step
    ZPE = np.mean(vref[start:stop][:,1]) #calculate the average energy in the relevant range of time steps (while the energy is stable)

    plt.plot(vref[:,0],vref[:,1])
    #sns.lineplot(data=vref[:,1])

    plt.hlines(y= ZPE,xmin = start,xmax= stop, color = 'tab:orange', label='ZPE: {0:.2f}'.format(ZPE))
    plt.legend()

    plt.ylabel('Eref (cm$^{-1}$)')
    plt.xlabel('Timestep (1 a.u.)')
    #plt.ylim(7000,15000)
    plt.savefig(f'{molecule}_sim_{sim_num}_zpe.png')

def plot_dist(dist, hist=True,line=True,exp=True):
    snapshots = np.arange(10000,50000,1000) #pull data every 1000 time steps from 10,000 to 50,000

    sim_data = pv.SimInfo(f'{path_to_data}/H5O3_0_sim_info.hdf5') #name of the simulation summary file
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
    plt.savefig('test_oh.png')

def plot_dists(dists):
    snapshots = np.arange(10000,50000,1000) #pull data every 1000 time steps from 10,000 to 50,000

    sim_data = pv.SimInfo(f'{path_to_data}/H5O3_0_sim_info.hdf5') #name of the simulation summary file
    coords, weights = sim_data.get_wfns(snapshots) #load in the molecule geometries (coords) and their associated weights
    coords = pv.Constants.convert(coords,'angstroms',to_AU=False) # conversion of coordinates from atomic units to Angstroms (more common in chemistry)

    analyzer = pv.AnalyzeWfn(coords)

    #df = pd.DataFrame({'weights': dws})

    for d in range(len(dists)):
        distance = analyzer.bond_length(dists[d][0],dists[d][1]) #calculates the distance between the first two atoms in the coordinates array, which correspond to the hydroxide ion

        #exp_val = analyzer.exp_val(distance,weights) #calculates the expectation value (average) of the quantity
        sns.kdeplot(distance,label=f'{dists[d][0]}{dists[d][1]}')

    plt.legend()
    plt.xlabel(r'Bond Length ($\AA$)')
    plt.ylabel('Probability Amplitude')
    plt.savefig('test_dists.png')




