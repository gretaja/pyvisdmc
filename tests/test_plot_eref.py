"""
Tests for the plot_eref function
"""
import sys

#sys.path.insert(0, '~/CSE583/pyvisdmc/src/pyvisdmc')

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

#test_smoke()
