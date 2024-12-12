"""
two_d_dist.py

This module provides a function to generate and save a 2D histogram for two
bond length distributions from a molecular Diffusion Monte Carlo (DMC)
simulation. It calculates the expectation value (average) of each bond length
and overlays it on the plot as a point.

Functions:
- plot_2d: Creates and saves a 2D histogram for two bond length distributions.

Dependencies:
- matplotlib, seaborn
"""
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

# Use a non-interactive backend
matplotlib.use('Agg')
# Set seaborn style
sns.set_style("white")


def plot_2d(molecule, sim_num, analyzer, weights, dists, exp=True):
    """
    Generate and save a 2D histogram of two bond length distributions from a
    molecular DMC simulation. The function calculates the expectation value
    (average) of each bond length and plots it as a point on the histogram.

    Parameters:
    - molecule: The molecule being analyzed (e.g., 'h5o3', 'h2o').
    - sim_num: The simulation number.
    - analyzer: An instance of pyvibdmc's AnalyzeWfn class, used to analyze
    wavefunctions.
    - weights: Weights associated with the molecular geometries.
    - dists: List of two pairs of atom indices representing bonds (e.g.,
    [[0, 1], [2, 3]]).
    - exp: If True, plot the expectation value (average) of each bond length
    on the 2D histogram.

    Raises:
    - ValueError: If the molecule name is invalid, the atom indices exceed
      the number of atoms in the molecule, or if the `dists` list does not
      contain exactly two pairs of indices.

    Saves:
    - A .png file with the 2D bond length distribution plot, named according
      to the molecule and simulation number (e.g., 'h5o3_sim_0_2d.png').
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
                raise ValueError(
                    'Atom index exceeds number of atoms in this molecule')
    # Ensure that 'dists' contains exactly two pairs of atom indices
    if len(dists) != 2:
        raise ValueError('"dists" must be a list of two pairs of atom indices')
    print(f"Creating plot two_d_dist for dists {dists} for {molecule}...")

    dist_vals = []
    exp_vals = []

    # Calculate distances between atoms and their expected values
    for dist in dists:
        # Calculates the distance between the first two atoms
        # in the coordinates array
        distance = analyzer.bond_length(dist[0], dist[1])
        dist_vals.append(distance)

        # Calculates the expectation value (average) of the quantity
        exp_val = analyzer.exp_val(distance, weights)
        exp_vals.append(exp_val)

    # Create 2D histogram of bond distances
    sns.histplot(x=dist_vals[0], y=dist_vals[1], cbar=True)

    # Plot the expectation values as a point on the 2D plot
    if exp:
        plt.scatter(exp_vals[0], exp_vals[1],
                    color='red',
                    label='Exp. Vals.')
        plt.legend()
    else:
        pass

    # Add axis labels and save the plot
    plt.xlabel(rf'{dists[0][0]}{dists[0][1]} Distance ($\AA$)')
    plt.ylabel(rf'{dists[1][0]}{dists[1][1]} Distance ($\AA$)')
    plt.savefig(f'{molecule}_sim_{sim_num}_2d.png', bbox_inches='tight')
    # Clear the current figure to avoid plot overlap
    plt.clf()
