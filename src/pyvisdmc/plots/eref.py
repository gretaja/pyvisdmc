import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import h5py
import pandas as pd

import pyvibdmc as pv

sns.set_style("white")

def plot_eref(data_path,molecule,sim_num,walkers,timesteps,start,stop):
    """Saves a .png of a line plot of the average enesemble energy with a simulation,
    calculates the zero point energy (ZPE) over a specified start and stopping point"""
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
    plt.savefig(f'{molecule}_sim_{sim_num}_zpe.png',bbox_inches='tight')

    plt.clf()
