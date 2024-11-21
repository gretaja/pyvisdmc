User Stories
1. Greta is a 3rd year researcher in the McCoy group.
She wants to analyze simulation data for multiple systems using the PyVibDMC software.
She wants to provide a folder/path to data that contains the simulations results from DMC, and would like to specify the exact type and quantity of figures generated from said simulation. Implied that PyVibDMC is already downloaded and installed.
She wants there to be a straightforward path from the data folder to the generated figures (without needing to move things around).
She has multiple years of python and DMC theory experience.

2. Roger is a 1st year rotating student in the group. Roger just wants to visualize simulation data to see how it works.
He wants there to be good documentation and very little room for error.
Roger has no Python experience and has heard a lecture on DMC theory.

3. Hope is a 2nd year researcher in the McCoy group. Hope wants to use visualizations of energies and geometries to check for inconsistencies between sets of converged simulation data as she introduces new guiding functions to the DMC code. Hope has a year of Python coding exerience and is familiar with multiple functionalities of matplotlib.A feature that would be particularly useful for her would be a tracker of the highest energy, lowest energy, and average energy of the ensemble at every step of the simulation so she can check for "holes" in the potential energy surface that the DMC simulation is being run with. 
 
4. Anne is the PI of the McCoy research group. She is very familiar with the theory and method of DMC and usually uses her own DMC code to run simulations, rather than PyVibDMC. Anne wants to be able to quickly visualize simulation data to pull the key quantities (zero point energies and expectation values) from DMC simulations without too much effort. Anne has decades of coding experience but only a couple years of Python specifically.

5. Mickey is a 4th year researcher in the McCoy group. Mickey is a contributor to the PyVibDMC code and is regularly updating this package to further his reserach and expand the capabilities of DMC. Mickey wants to be able to deeply analyze his DMC results to evaluate the performance of his new methods, as well as create polished figures for publications. Mickey has an undergraduate degree in computer science, is very familiar with python, and is the most senior member of the research group with the most experience with PyVibDMC.

6. Andrew is an undergraduate researcher in the McCoy group. Andrew is familiar with the theory of DMC as he has coded up his own version of it, and is just getting started with running full-scale simulations with the PyVibDMC package. Andrew is tasked with performing an exploratory analysis of a new, small system that has not been studied by the group yet, so he's not sure where to start looking in terms of converged simulation results. He would like to be able to easily plot a variety of different geometry distributions for this system so he can figure out what might be interesting to dig further into. He is famililar with Python but not as familiar with matplotlib.

7. Rose is a 3rd year researcher in the McCoy group who develops neural network potential energy surfaces for the systems of interest. She wants to evaluate the performance of her neural net potentials in small and large scale DMC simulations by visualizing the convergence of energies and geometries across various simulations. In particular, she wants to be able to quickly identify when and where simulations crashed, and what geometries/energies led to this crash. She has multiple years of python and matplotlib experience, and would like the option to create highly specified visualizations.

Example use case:
Greta provides a path to the data and details about the system.
PyVisDMC provides options for possible visualizations.
Greta specifies atom indices, ranges of simulation time steps, number of dimensions, etc.
PyVisDMC outputs a visualization.
