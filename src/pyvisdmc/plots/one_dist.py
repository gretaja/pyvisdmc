"""
one_dist.py

This module provides a function to generate and save a histogram or density plot
for a specific bond length in a molecular Diffusion Monte Carlo (DMC) simulation.
It calculates the expectation value of the bond length and overlays it on the plot.

Functions:
- plot_dist: Creates and saves a plot for a single bond length distribution.

Dependencies:
- numpy, matplotlib, seaborn
"""

import numpy as np # unused import, should we delete it?
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

# Use a non-interactive backend
matplotlib.use('Agg')
# Set seaborn style
sns.set_style("white")

def plot_dist(molecule,analyzer,weights,dist,hist=True,line=True,exp=True):
    """
    Generate and save a plot of a bond length distribution from a molecular DMC simulation.

    Parameters:
    - molecule: The molecule being analyzed ('h5o3' or 'h2o').
    - analyzer: An instance of pyvibdmc's AnalyzeWfn class, used to analyze wavefunctions.
    - weights: Weights associated with the molecular geometries.
    - dist: Indices of the two atoms forming the bond (e.g., [0, 1]).
    - hist: If True, generate a histogram.
    - line: If True, overlay a KDE (Kernel Density Estimate) line on the histogram.
    - exp: If True, include a vertical line for the expectation value.

    Raises:
    - ValueError: If the molecule name is invalid or the atom indices exceed the number 
    of atoms.

    Saves:
    - A .png file with the bond length distribution plot, named based on the molecule 
    and bond indices.
    """
    # Validate the molecule and assign the number of atoms
    if molecule == 'h5o3':
        num_atoms = 8
    elif molecule == 'h2o':
        num_atoms = 3
    else:
        raise ValueError('Not a valid molecule name')
    # Validate the atom indices
    for ind in dist:
        if ind > num_atoms - 1:
            raise ValueError('Atom index exceeds number of atoms in this molecule')
    print(f"Creating plot one_dist for dist {dist} for {molecule}...")
    # Calculate the distance between the first two atoms in the coordinates array
    distance = analyzer.bond_length(dist[0],dist[1])
    # Calculates the expectation value (average) of the quantity
    exp_val = analyzer.exp_val(distance,weights)

    # Generate histogram or density plot
    if hist:
        if line:
            # Normalizes the distribution so the total probability is 1
            sns.histplot(distance, kde=True, bins=50,label=f'{dist[0]}{dist[1]}')
        else:
            sns.histplot(distance, kde=False, bins=50,label=f'{dist[0]}{dist[1]}')
    else:
        sns.kdeplot(distance,label=f'{dist[0]}{dist[1]}')

    # Plot the average value in a vertical line
    if exp:
        plt.vlines(
            exp_val, 0, 6,
            label=rf'$\langle${dist[0]}{dist[1]}$\rangle$ = {exp_val:.4f} $\AA$'
        )
    # Add labels and save the plot
    plt.xlabel(r'Bond Length ($\AA$)')
    plt.ylabel('Probability Amplitude')
    plt.legend()
    plt.savefig(f'{molecule}_{dist[0]}{dist[1]}_dist.png',bbox_inches='tight')
    # Clear the current figure to avoid overlapping plots
    plt.clf()
