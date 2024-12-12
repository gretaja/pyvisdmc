"""
Tests for the data_loader module
"""
import pytest

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
    data_path = 'src/pyvisdmc/test_data'

    load_data(data_path, molecule, sim_num, walkers, timesteps)


def test_smoke_sim_info():
    """
    Simple smoke test to make sure sim_info runs.
    """
    start = 5000
    stop = 20000
    sim_data = pv.SimInfo(
        'src/pyvisdmc/test_data/h2o_example_data/'
        '1.0w_5000_walkers_20000t_1dt/H2O_0_sim_info.hdf5')

    sim_info(sim_data, start, stop)


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
        load_data(DATA_PATH, molecule, sim_num, walkers, timesteps)


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
        load_data(DATA_PATH, molecule, sim_num, walkers, timesteps)


def test_num_walkers():
    """
    Edge test for non-existing number of walkers
    """
    molecule = 'h2o'
    sim_num = 0
    walkers = 10000
    timesteps = 20000

    with pytest.raises(
        ValueError, match=
        f'Simulation of size {walkers} walkers does not exist for this system'
    ):
        load_data(DATA_PATH, molecule, sim_num, walkers, timesteps)


def test_num_timesteps():
    """
    Edge test for non-existing simulation length
    """
    molecule = 'h2o'
    sim_num = 0
    walkers = 5000
    timesteps = 30000

    with pytest.raises(
        ValueError, match=
        f'Simulation of length {timesteps} timesteps does not exist for this system'
    ):
        load_data(DATA_PATH, molecule, sim_num, walkers, timesteps)
