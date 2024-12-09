"""
Plotting functions for DMC analysis

This module provides plotting functions for Diffusion Monte Carlo (DMC) analysis of 
molecular simulations. It includes functions to visualize ensemble energy, bond length 
distributions, and other properties of molecules like H5O3 and H2O.

Functions:
- plot_eref: Generate a plot of ensemble energy and calculate the zero-point energy (ZPE).
- plot_dist: Create a histogram or density plot for a specific bond length.
- plot_dists: Generate density plots for multiple bond lengths.

Dependencies:
- numpy, matplotlib, seaborn, h5py, pandas, pyvibdmc
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import h5py
import pandas as pd
import pyvibdmc as pv

# Use a non-interactive backend
matplotlib.use('Agg')

# Set seaborn style
sns.set_style("white")

#path to the folder containing the simulation data
#path_to_data = '../data/h5o3_example_data/1.0w_50000_walkers_50000t_1dt'

def plot_eref(data_path,molecule,sim_num,walkers,timesteps,start,stop):
    """
    Generate a plot of ensemble energy for a molecular simulation and calculate 
    zero-point energy (ZPE).

    Parameters:
    - data_path (str): Path to the directory containing simulation data.
    - molecule (str): The molecule being analyzed ('h5o3' or 'h2o').
    - sim_num (int): Simulation number.
    - walkers (int): Number of walkers in the simulation.
    - timesteps (int): Total number of timesteps in the simulation.
    - start (int): Starting timestep for ZPE calculation.
    - stop (int): Ending timestep for ZPE calculation.

    Raises:
    - ValueError: If the molecule name is invalid or the stopping point exceeds 
    the simulation length.

    Saves:
    - A .png file with the plot, named based on the molecule and simulation number.
    """
    if molecule == 'h5o3':
        name = 'H5O3'
    elif molecule == 'h2o':
        name = 'H2O'
    else:
        raise ValueError('Not a valid molecule name')
    if stop > timesteps:
        raise ValueError('Stopping point exceeds length of simulation')
    else:
        pass
    # path to the folder containing the simulation data
    path_to_data = (
        f'{data_path}/{molecule}_example_data/1.0w_{walkers}_walkers_{timesteps}t_1dt'
    )

    # name of the simulation summary file
    sim_data = pv.SimInfo(
        f'{path_to_data}/{name}_{sim_num}_sim_info.hdf5'
    )

    # start = 10000 #where we want to start averaging the energy from
    # stop = 50000 #where we want to average until

    # generates an array of the timesteps and the average energy of the ensemble at that step
    vref = sim_data.get_vref(ret_cm=True)
    # calculate the average energy in the relevant range of time steps (while the energy is stable)
    ZPE = np.mean(vref[start:stop][:,1])

    plt.plot(vref[:,0],vref[:,1])
    #sns.lineplot(data=vref[:,1])

    plt.hlines(y= ZPE,
               xmin = start,
               xmax= stop,
               color = 'tab:orange',
               label='ZPE: {0:.2f}'.format(ZPE))
    plt.legend()
    plt.ylabel('Eref (cm$^{-1}$)')
    plt.xlabel('Timestep (1 a.u.)')
    #plt.ylim(7000,15000)
    plt.savefig(f'{molecule}_sim_{sim_num}_zpe.png')

def plot_dist(dist, hist=True,line=True,exp=True):
    """
    Generate a histogram or density plot for a specific bond length in a molecular simulation.

    Parameters:
    - dist (list[int]): Indices of the two atoms forming the bond (e.g., [0, 1]).
    - hist (bool, optional): If True, generate a histogram; if False, skip the histogram. 
    Defaults to True.
    - line (bool, optional): If True, overlay a KDE (Kernel Density Estimate) line on the 
    histogram. Defaults to True.
    - exp (bool, optional): If True, include a vertical line for the expectation value. 
    Defaults to True.

    Saves:
    - A .png file with the bond length distribution plot.
    """
    # pull data every 1000 time steps from 10,000 to 50,000
    snapshots = np.arange(10000,50000,1000)

    # name of the simulation summary file
    sim_data = pv.SimInfo(f'{path_to_data}/H5O3_0_sim_info.hdf5')

    # load in the molecule geometries (coords) and their associated weights
    coords, weights = sim_data.get_wfns(snapshots)
    # conversion of coordinates from atomic units to Angstroms (more common in chemistry)
    coords = pv.Constants.convert(coords,'angstroms',to_AU=False)

    analyzer = pv.AnalyzeWfn(coords)
    #df = pd.DataFrame({'weights': dws})

    # calculates the distance between the first two atoms in the coordinates array,
    # which correspond to the hydroxide ion
    distance = analyzer.bond_length(dist[0],dist[1])
    # calculates the expectation value (average) of the quantity
    exp_val = analyzer.exp_val(distance,weights)

    if hist==True:
        if line==True:
            # normalizes the distribution so the total probability is 1
            sns.histplot(distance,
                         kde=True,
                         bins=50,
                         label=f'{dist[0]}{dist[1]}')
        else:
            sns.histplot(distance,
                         kde=False,
                         bins=50,
                         label=f'{dist[0]}{dist[1]}')
    else:
        sns.kdeplot(distance,
                    label=f'{dist[0]}{dist[1]}')
    # plot a vertical line where the average value is
    if exp==True:
        plt.vlines(exp_val,0,6,
                   label=rf'$\langle${dist[0]}{dist[1]}$\rangle$ = {exp_val:.4f} $\AA$')
    else:
        pass
    plt.xlabel(r'Bond Length ($\AA$)')
    plt.ylabel('Probability Amplitude')
    plt.savefig('test_oh.png')

def plot_dists(dists):
    """
    Generate density plots for multiple bond lengths in a molecular simulation.

    Parameters:
    - dists (list[list[int]]): List of pairs of atom indices representing bonds (e.g., [[0, 1],
      [2, 3]]).

    Saves:
    - A .png file with the density plots for all specified bond lengths.
    """
    # pull data every 1000 time steps from 10,000 to 50,000
    snapshots = np.arange(10000,50000,1000)
    # name of the simulation summary file
    sim_data = pv.SimInfo(
        f'{path_to_data}/H5O3_0_sim_info.hdf5'
    )
    # load in the molecule geometries (coords) and their associated weights
    coords, weights = sim_data.get_wfns(snapshots)
    # conversion of coordinates from atomic units to Angstroms (more common in chemistry)
    coords = pv.Constants.convert(coords,'angstroms',to_AU=False)

    analyzer = pv.AnalyzeWfn(coords)

    #df = pd.DataFrame({'weights': dws})

    for d in range(len(dists)):
        # calculates the distance between the first two atoms in the coordinates array, which
        # correspond to the hydroxide ion
        distance = analyzer.bond_length(dists[d][0],dists[d][1])
        # xp_val = analyzer.exp_val(distance,weights)

        # calculates the expectation value (average) of the quantity
        sns.kdeplot(distance,label=f'{dists[d][0]}{dists[d][1]}')
    plt.legend()
    plt.xlabel(r'Bond Length ($\AA$)')
    plt.ylabel('Probability Amplitude')
    plt.savefig('test_dists.png')
    