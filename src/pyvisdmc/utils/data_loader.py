"""Module for loading in data for all the plotting functions"""

import numpy as np

import pyvibdmc as pv


def load_data(data_path, molecule, sim_num, walkers, timesteps):

    if molecule == 'h5o3':
        name = 'H5O3'

    elif molecule == 'h2o':
        name = 'H2O'

    else:
        raise ValueError('Not a valid molecule name')
    if sim_num != 0:
        raise ValueError(
            f'Simulation {sim_num} does not exist for this system')
    else:
        pass

    if walkers != 5000:
        raise ValueError(
            f'Simulation of size {walkers} walkers does not exist for this system')
    else:
        pass

    if timesteps != 20000:
        raise ValueError(
            f'Simulation of length {timesteps} timesteps does not exist for this system')
    else:
        pass

    # path to the folder containing the simulation data
    path_to_data = f'{data_path}/{molecule}_example_data/1.0w_{walkers}_walkers_{timesteps}t_1dt'
    # name of the simulation summary file
    sim_data = pv.SimInfo(f'{path_to_data}/{name}_{sim_num}_sim_info.hdf5')

    return sim_data


def sim_info(sim_data, start, stop):
    snapshots = np.arange(start, stop, 1000)
    # load in the molecule geometries (coords) and their associated weights
    coords, weights = sim_data.get_wfns(snapshots)
    # conversion of coordinates from atomic units to Angstroms
    coords = pv.Constants.convert(coords, 'angstroms', to_AU=False)
    analyzer = pv.AnalyzeWfn(coords)

    return analyzer, weights
