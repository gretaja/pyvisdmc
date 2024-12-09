"""
Tests for the plot_eref function
"""

import pytest
import numpy as np

import pyvibdmc as pv
from pyvisdmc.plots import plot_eref

def test_smoke():
    """
    Simple smoke test to make sure function runs.
    """
    molecule = 'h2o'
    sim_num = 0
    start = 5000
    stop = 20000

    sim_data = pv.SimInfo('src/pyvisdmc/test_data/H2O_0_sim_info.hdf5')

    plot_eref(molecule,sim_num,sim_data,start,stop)

    return

def test_stop_value():
    """
    Edge test for stop value exeeding length of simulation
    """
    molecule = 'h2o'
    sim_num = 0
    start = 5000
    stop = 30000

    with pytest.raises(
        ValueError, match=f"The stop time {stop} exceeds the length of the available data"
    ):
        sim_data = pv.SimInfo('src/pyvisdmc/test_data/H2O_0_sim_info.hdf5')

        plot_eref(molecule,sim_num,sim_data,start,stop)

    return 

