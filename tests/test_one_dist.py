"""
Tests for the one_dist function
"""

import pytest
import numpy as np

from pyvisdmc.plots import plot_dist
from pyvisdmc.test_data import DATA_PATH

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

    dist = [0,1]

    plot_dist(DATA_PATH,molecule,sim_num,walkers,timesteps,start,stop,dist)

    return

def test_smoke_hist_false():
    """
    Simple smoke test to make sure function runs with histogram plotting off.
    """
    molecule = 'h2o'
    sim_num = 0
    walkers = 5000
    timesteps = 20000
    start = 5000
    stop = 20000

    dist = [0,1]

    plot_dist(DATA_PATH,molecule,sim_num,walkers,timesteps,start,stop,dist,hist=False)

    return

def test_smoke_line_false():
    """
    Simple smoke test to make sure function runs with line plotting off.
    """
    molecule = 'h2o'
    sim_num = 0
    walkers = 5000
    timesteps = 20000
    start = 5000
    stop = 20000

    dist = [0,1]

    plot_dist(DATA_PATH,molecule,sim_num,walkers,timesteps,start,stop,dist,line=False)

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

    dist = [0,1]

    plot_dist(DATA_PATH,molecule,sim_num,walkers,timesteps,start,stop,dist,exp=False)

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

        dist = [0,1]

        plot_dist(DATA_PATH,molecule,sim_num,walkers,timesteps,start,stop,dist)

    return 

def test_stop_value():
    """
    Edge test for stop value exeeding length of simulation
    """
    with pytest.raises(
        ValueError, match="Stopping point exceeds length of simulation"
    ):
        molecule = 'h2o'
        sim_num = 0
        walkers = 5000
        timesteps = 20000
        start = 5000
        stop = 30000

        dist = [0,1]

        plot_dist(DATA_PATH,molecule,sim_num,walkers,timesteps,start,stop,dist)

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

        dist = [0,4]

        plot_dist(DATA_PATH,molecule,sim_num,walkers,timesteps,start,stop,dist)

    return 

