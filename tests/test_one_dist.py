"""
Tests for the one_dist function
"""

import pytest
import numpy as np

import pyvibdmc as pv
from pyvisdmc.plots import plot_dist

def test_smoke_default():
    """
    Simple smoke test to make sure function runs with default Boolean parameters.
    """
    molecule = 'h2o'
    dist = [0,1]
    h2o_cds = np.load('src/pyvisdmc/test_data/h2o_cds.npy')
    weights = np.load('src/pyvisdmc/test_data/h2o_dws.npy')
    analyzer = pv.AnalyzeWfn(h2o_cds)

    plot_dist(molecule,analyzer,weights,dist)

def test_smoke_hist_false():
    """
    Simple smoke test to make sure function runs with histogram plotting off.
    """
    molecule = 'h2o'
    dist = [0,1]
    h2o_cds = np.load('src/pyvisdmc/test_data/h2o_cds.npy')
    weights = np.load('src/pyvisdmc/test_data/h2o_dws.npy')
    analyzer = pv.AnalyzeWfn(h2o_cds)

    plot_dist(molecule,analyzer,weights,dist,hist=False)

def test_smoke_line_false():
    """
    Simple smoke test to make sure function runs with line plotting off.
    """
    molecule = 'h2o'
    dist = [0,1]
    h2o_cds = np.load('src/pyvisdmc/test_data/h2o_cds.npy')
    weights = np.load('src/pyvisdmc/test_data/h2o_dws.npy')
    analyzer = pv.AnalyzeWfn(h2o_cds)

    plot_dist(molecule,analyzer,weights,dist,line=False)

def test_smoke_exp_false():
    """
    Simple smoke test to make sure function runs with expectation value plotting off.
    """
    molecule = 'h2o'
    dist = [0,1]
    h2o_cds = np.load('src/pyvisdmc/test_data/h2o_cds.npy')
    weights = np.load('src/pyvisdmc/test_data/h2o_dws.npy')
    analyzer = pv.AnalyzeWfn(h2o_cds)

    plot_dist(molecule,analyzer,weights,dist,exp=False)

def test_atom_indices():
    """
    Edge test for selected atom indices exceeding the number of atoms in the molecule
    """
    with pytest.raises(
        ValueError, match="Atom index exceeds number of atoms in this molecule"
    ):
        molecule = 'h2o'
        dist = [0,4]
        h2o_cds = np.load('src/pyvisdmc/test_data/h2o_cds.npy')
        weights = np.load('src/pyvisdmc/test_data/h2o_dws.npy')
        analyzer = pv.AnalyzeWfn(h2o_cds)

        plot_dist(molecule,analyzer,weights,dist)
