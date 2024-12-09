"""
mult_dist.py

This module provides a function to generate and save histograms and/or density plots
for multiple bond length distributions from a molecular Diffusion Monte Carlo (DMC) 
simulation. It calculates the expectation value (average) of each bond length and 
overlays it on the plot.

Functions:
- plot_dists: Creates and saves plots for multiple bond length distributions.

Dependencies:
- numpy, matplotlib, seaborn
"""

import numpy as np # unused import, shall we delete?
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

# Use a non-interactive backend
matplotlib.use('Agg')
# Set seaborn style
sns.set_style("white")

def plot_dists(molecule,sim_num,analyzer,weights,dists,hist=True,line=True,exp=True):
    """
    Generate and save plots of multiple bond length distributions from a molecular 
    DMC simulation. The function can plot histograms, density plots, and overlay 
    expectation values on the plot.

    Parameters:
    - molecule: The molecule being analyzed (e.g., 'h5o3', 'h2o').
    - sim_num: The simulation number.
    - analyzer: An instance of pyvibdmc's AnalyzeWfn class, used to analyze wavefunctions.
    - weights: Weights associated with the molecular geometries.
    - dists: List of pairs of atom indices representing bonds (e.g., [[0, 1], [2, 3]]).
    - hist: If True, generate a histogram.
    - line: If True, overlay a KDE (Kernel Density Estimate) line on the histogram.
    - exp: If True, include vertical lines for the expectation values.

    Raises:
    - ValueError: If the molecule name is invalid or any atom index in `dists` 
      exceeds the number of atoms in the molecule.

    Saves:
    - A .png file with the bond length distribution plots, named according to 
      the molecule and simulation number (e.g., 'h5o3_sim_0_mult_dists.png').
    """
    # Validate the molecule and assign the number of atoms
    if molecule == 'h5o3':
        num_atoms = 8
    elif molecule == 'h2o':
        num_atoms = 3
    else:
        raise ValueError('Not a valid molecule name')
    # Validate the atom indices for each bond in dists
    for dist in dists:
        for ind in dist:
            if ind > num_atoms - 1:
                raise ValueError('Atom index exceeds number of atoms in this molecule')
    print(f"Creating plot mult_dist for dists {dists} for {molecule}...")

    dist_vals = []
    exp_vals = []

    for dist in dists:
        # Calculates the distance between the first two atoms in the coordinates array
        distance = analyzer.bond_length(dist[0],dist[1])
        dist_vals.append(distance)
        # Calculates the expectation value (average) of the quantity
        exp_val = analyzer.exp_val(distance,weights)
        exp_vals.append(exp_val)
    # If hist is true, generate histograms or density plots
    if hist:
        if line:
            for i in range(len(dist_vals)):
                # Normalizes the distribution so the total probability is 1
                sns.histplot(dist_vals[i], kde=True, bins=50,label=f'{dists[i][0]}{dists[i][1]}')
        else:
            for i in range(len(dist_vals)):
                sns.histplot(dist_vals[i], kde=False, bins=50,label=f'{dists[i][0]}{dists[i][1]}')
    else:
        for i in range(len(dist_vals)):
            sns.kdeplot(dist_vals[i],label=f'{dists[i][0]}{dists[i][1]}')
    # If exp is true, plot vertical lines for expectation values
    if exp:
        for i in range(len(exp_vals)):
            plt.vlines(exp_vals[i], 0, 6,
                       label=rf'$\langle${dists[i][0]}{dists[i][1]}$\rangle$='
                       f'{exp_vals[i]:.4f}$\\AA$')
    else:
        pass
    # Add legend, axis labels, and save the plot
    plt.legend()
    plt.xlabel(r'Bond Length ($\AA$)')
    plt.ylabel('Probability Amplitude')
    plt.savefig(f'{molecule}_sim_{sim_num}_mult_dists.png',bbox_inches='tight')

    # Clear the current figure to avoid plot overlap
    plt.clf()
