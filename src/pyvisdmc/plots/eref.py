"""
eref.py

This module provides a function to generate and save a plot of the reference energy (Eref) 
of a molecular Diffusion Monte Carlo (DMC) simulation. It calculates the zero-point energy 
(ZPE) over a specified time interval and visualizes the energy as a line plot.

Functions:
- plot_eref: Creates and saves a plot of the ensemble energy and calculates ZPE.

Dependencies:
- numpy, matplotlib, seaborn
"""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

# Use a non-interactive backend
matplotlib.use('Agg')

# Set seaborn style
sns.set_style("white")

def plot_eref(molecule,sim_num,sim_data,start,stop):
    """
    Generate and save a plot of the reference energy (Eref) for a molecular DMC simulation 
    and calculate the zero-point energy (ZPE) over a specified time range.

    Parameters:
    - molecule: The molecule being analyzed (e.g., 'h5o3', 'h2o').
    - sim_num: The simulation number.
    - sim_data: An instance of pyvibdmc's SimInfo class, which contains simulation data.
    - start: The starting timestep for calculating the ZPE.
    - stop: The stopping timestep for calculating the ZPE.

    Raises:
    - ValueError: If the start or stop values are invalid (e.g., start > stop, or indices 
      are out of range).

    Saves:
    - A .png file with the reference energy plot, named according to the molecule 
      and simulation number (e.g., 'h5o3_sim_0_zpe.png').
    """
    # Generate an array of timesteps and the average energy of the ensemble at that step
    vref = sim_data.get_vref(ret_cm=True)

    if stop > len(vref):
        raise ValueError(
            f"The stop time {stop} exceeds the length of the available data"
        )
    # Calculate the ZPE in the relevant range of time steps (while the energy is stable)
    zpe = np.mean(vref[start:stop][:, 1])

    # Plot the reference energy over time
    plt.plot(vref[:,0],vref[:,1], label="Eref")

    # Plot a horizontal line to indicate the calculated ZPE
    plt.hlines(y= zpe,
              xmin = start,
              xmax= stop,
              color = 'tab:orange',
              label = rf'ZPE: {zpe:.2f} cm$^-$$^1$') # changed to f-string format
    plt.legend()

    # Add axis labels
    plt.ylabel('Eref (cm$^{-1}$)')
    plt.xlabel('Timestep (1 a.u.)')
    # Save the plot as a .png file
    plt.savefig(f'{molecule}_sim_{sim_num}_zpe.png',bbox_inches='tight')
    # Clear the current figure to avoid plot overlap
    plt.clf()
