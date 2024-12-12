"""
Tests for the mult_dist function
"""

import pytest
import numpy as np

import pyvibdmc as pv
from pyvisdmc.plots import plot_dists


def test_smoke_default():
    """
    Simple smoke test to make sure function runs with
    default Boolean parameters.
    """
    molecule = 'h2o'
    sim_num = 0
    dists = [[0, 1], [0, 2]]
    h2o_cds = np.load('src/pyvisdmc/test_data/h2o_cds.npy')
    weights = np.load('src/pyvisdmc/test_data/h2o_dws.npy')
    analyzer = pv.AnalyzeWfn(h2o_cds)

    plot_dists(molecule, sim_num, analyzer, weights, dists)


def test_smoke_hist_false():
    """
    Simple smoke test to make sure function runs with histogram plotting off.
    """
    molecule = 'h2o'
    sim_num = 0
    dists = [[0, 1], [0, 2]]
    h2o_cds = np.load('src/pyvisdmc/test_data/h2o_cds.npy')
    weights = np.load('src/pyvisdmc/test_data/h2o_dws.npy')
    analyzer = pv.AnalyzeWfn(h2o_cds)

    plot_dists(molecule, sim_num, analyzer, weights, dists, hist=False)


def test_smoke_line_false():
    """
    Simple smoke test to make sure function runs with line plotting off.
    """
    molecule = 'h2o'
    sim_num = 0
    dists = [[0, 1], [0, 2]]
    h2o_cds = np.load('src/pyvisdmc/test_data/h2o_cds.npy')
    weights = np.load('src/pyvisdmc/test_data/h2o_dws.npy')
    analyzer = pv.AnalyzeWfn(h2o_cds)

    plot_dists(molecule, sim_num, analyzer, weights, dists, line=False)


def test_smoke_exp_false():
    """
    Simple smoke test to make sure function runs with
    expectation value plotting off.
    """
    molecule = 'h2o'
    sim_num = 0
    dists = [[0, 1], [0, 2]]
    h2o_cds = np.load('src/pyvisdmc/test_data/h2o_cds.npy')
    weights = np.load('src/pyvisdmc/test_data/h2o_dws.npy')
    analyzer = pv.AnalyzeWfn(h2o_cds)

    plot_dists(molecule, sim_num, analyzer, weights, dists, exp=False)


def test_atom_indices():
    """
    Edge test for selected atom indices exceeding the number
    of atoms in the molecule
    """
    with pytest.raises(
        ValueError, match="Atom index exceeds number of atoms in this molecule"
    ):
        molecule = 'h2o'
        sim_num = 0
        dists = [[0, 4], [0, 2]]
        h2o_cds = np.load('src/pyvisdmc/test_data/h2o_cds.npy')
        weights = np.load('src/pyvisdmc/test_data/h2o_dws.npy')
        analyzer = pv.AnalyzeWfn(h2o_cds)

        plot_dists(molecule, sim_num, analyzer, weights, dists)
