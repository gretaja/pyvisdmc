"""
Tests for the plot_eref function
"""

import pytest
import numpy as np

from pyvisdmc.plots import plot_eref
from pyvisdmc.test_data import DATA_PATH

def test_smoke():
    """
    Simple smoke test to make sure function runs.
    """
    molecule = 'h2o'
    sim_num = 0
    walkers = 5000
    timesteps = 20000
    start = 5000
    stop = 20000

    plot_eref(DATA_PATH,molecule,sim_num,walkers,timesteps,start,stop)

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

        plot_eref(DATA_PATH,molecule,sim_num,walkers,timesteps,start,stop)

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

        plot_eref(DATA_PATH,molecule,sim_num,walkers,timesteps,start,stop)

    return 

