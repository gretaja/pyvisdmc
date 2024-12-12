"""
Tests for the data_loader module 
"""
import pytest
import numpy as np

import pyvibdmc as pv
from pyvisdmc.utils import load_data, sim_info
from pyvisdmc.test_data import DATA_PATH

def test_smoke_load_data():
    """
    Simple smoke test to make sure load_data runs.
    """
    molecule = 'h2o'
    sim_num = 0
    walkers = 5000
    timesteps = 20000

    load_data(DATA_PATH,molecule,sim_num,walkers,timesteps)

    return

def test_smoke_sim_info():
    """
    Simple smoke test to make sure sim_info runs.
    """
    molecule = 'h2o'
    sim_num = 0
    walkers = 5000
    timesteps = 20000
    start = 5000
    stop = 20000
    
    sim_data = load_data(DATA_PATH,molecule,sim_num,walkers,timesteps)

    sim_info(sim_data,start,stop)

    return

def test_molecule_name():
    """
    Edge test for non-existing molecule name
    """
    molecule = 'h3o'
    sim_num = 0
    walkers = 5000
    timesteps = 20000

    with pytest.raises(
        ValueError, match='Not a valid molecule name'
    ):
        load_data(DATA_PATH,molecule,sim_num,walkers,timesteps)

    return 

def test_sim_num():
    """
    Edge test for non-existing simulation number
    """
    molecule = 'h2o'
    sim_num = 5
    walkers = 5000
    timesteps = 20000

    with pytest.raises(
        ValueError, match=f'Simulation {sim_num} does not exist for this system'
    ):
        load_data(DATA_PATH,molecule,sim_num,walkers,timesteps)

    return 

def test_num_walkers():
    """
    Edge test for non-existing number of walkers
    """
    molecule = 'h2o'
    sim_num = 0
    walkers = 10000
    timesteps = 20000

    with pytest.raises(
        ValueError, match=f'Simulation of size {walkers} walkers does not exist for this system'
    ):
        load_data(DATA_PATH,molecule,sim_num,walkers,timesteps)

    return 

def test_num_timesteps():
    """
    Edge test for non-existing simulation length
    """
    molecule = 'h2o'
    sim_num = 0
    walkers = 5000
    timesteps = 30000

    with pytest.raises(
        ValueError, match=f'Simulation of length {timesteps} timesteps does not exist for this system'
    ):
        load_data(DATA_PATH,molecule,sim_num,walkers,timesteps)

    return 

