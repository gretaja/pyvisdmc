"""
Tests for the two_d_dist function
"""

import pytest
import numpy as np

from pyvisdmc.plots import plot_2d
from pyvisdmc.test_data import DATA_PATH
from pyvisdmc.utils.data_loader import load_data, sim_info

def test_smoke_default():
    """
    Simple smoke test to make sure function runs with default Boolean parameters.
    """
    molecule = 'h2o'
    sim_num = 0
    walkers = 5000
    timesteps = 20000
    start = 5000
    stop = 20000

    dists = [[0,1],[0,2]]

    sim_data = load_data(DATA_PATH,molecule,sim_num,walkers,timesteps)

    analyzer, weights = sim_info(sim_data,start,stop)

    plot_2d(molecule,sim_num,analyzer,weights,dists,exp=True)

    return


def test_smoke_exp_false():
    """
    Simple smoke test to make sure function runs with expectation value plotting off.
    """
    molecule = 'h2o'
    sim_num = 0
    walkers = 5000
    timesteps = 20000
    start = 5000
    stop = 20000

    dists = [[0,1],[0,2]]

    sim_data = load_data(DATA_PATH,molecule,sim_num,walkers,timesteps)

    analyzer, weights = sim_info(sim_data,start,stop)

    plot_2d(molecule,sim_num,analyzer,weights,dists,exp=False)

    return

def test_molecule_name():
    """
    Edge test for invalid molecule name
    """
    with pytest.raises(
        ValueError, match="Not a valid molecule name"
    ):
        molecule = 'h3o'
        sim_num = 0
        walkers = 5000
        timesteps = 20000
        start = 5000
        stop = 20000

        dists = [[0,1],[0,2]]

        sim_data = load_data(DATA_PATH,molecule,sim_num,walkers,timesteps)

        analyzer, weights = sim_info(sim_data,start,stop)

        plot_2d(molecule,sim_num,analyzer,weights,dists)

    return 

def test_atom_indices():
    """
    Edge test for selected atom indices exceeding the number of atoms in the molecule
    """
    with pytest.raises(
        ValueError, match="Atom index exceeds number of atoms in this molecule"
    ):
        molecule = 'h2o'
        sim_num = 0
        walkers = 5000
        timesteps = 20000
        start = 5000
        stop = 20000

        dists = [[0,4],[0,2]]

        sim_data = load_data(DATA_PATH,molecule,sim_num,walkers,timesteps)

        analyzer, weights = sim_info(sim_data,start,stop)

        plot_2d(molecule,sim_num,analyzer,weights,dists)

    return 

def test_dists_shape():
    """
    Edge test for dists not being a list of size 2
    """
    with pytest.raises(
        ValueError, match='"dists" must be a list of two pairs of atom indices'
    ):
        molecule = 'h2o'
        sim_num = 0
        walkers = 5000
        timesteps = 20000
        start = 5000
        stop = 20000

        dists = [[0,1],[0,2],[1,2]]

        sim_data = load_data(DATA_PATH,molecule,sim_num,walkers,timesteps)

        analyzer, weights = sim_info(sim_data,start,stop)

        plot_2d(molecule,sim_num,analyzer,weights,dists)

    return

