# Defining components for the project

## Data source (PyVibDMC output file)
### What it does
Provides a set of data to analyze.

### Inputs
n/a (we assume the data file we want to analyze already exists on the user's computer

### Outputs
hdf5 file for analysis

### Talks to
Data loader

## Data Loader 
### What it does
Allows user to select and load a .hdf5 file containing simulation data. Validates that file format is appropriate for data analysis.

### Inputs
File path: user inputs the path to the .hdf5 file they want to analyze (and configuration flags?)
Data type: string

### Outputs
Validation: indicates whether or not the file was successfully loaded.
Data type: Boolean (true/false), string for each true and false (success/error message). Depending on output, the user repeats use of this component or is sent to the main menu.

### Talks to
Data configuration component
Data processing/plot creation components
Main menu component

### Side effects
If validation is false, the file was not loaded successfully. An error message indicates to user that they have input either the wrong directory or an invalid file type. The user may try again (by entering a different path to data).
If validation is true, the user receives a message that their data was loaded successfully and is sent to the main menu.

## Data configuration (optional)
### What it does
Manages “settings” for the data that is analyzed.
Allows users to configure more advanced parameters for their analysis (for example, choose to only analyze a specific time range in the loaded data).

### Inputs
User settings for selected variables. (Perhaps these configurations can be chosen as flags on the end of path to data? Or maybe it would be better to shove these configurations as options later on in the analysis? I’m gonna run with the flags idea for now.)
Data types: various, we need to discuss if we want this component or what parameters the user would be able to restrict here more specifically

### Outputs
Configured parameters, what settings were applied that modified the data that was actually loaded for analysis. 
Data type: a dictionary might be good for this
Error message if user inputs and unrecognized flag
Data type: string

### Talks to
Data loader
Data processing/plot creation components

### Side effects
If user successfully configures advanced parameters, the load success message includes what parameters were restricted and how.
If the configuration is not valid, the user sees an error message that their configuration was not recognized.

## Data validation (I guess this is actually sub component of the data loader)
### What it does
Check integrity and completeness of loaded data.
Ensures that data contains the field necessary for selected analysis.

### Inputs
The selected .hdf5 file with any user specified configurations.

### Outputs
Validation status: indicates whether the file contains data that can be analyzed using this software.
Data type: Boolean
Error message detailing any issues found in the selected data
Data type: string

### Talks to
Main menu
Data loader
Data configuration
Data processing/plot creation compoents

### Side effects
Nothing if the data that the user selected is complete. The user moves to the main menu. 
If the user has successfully configured data, but the data is not appropriate for the selected analysis, the user receives an error message that tells them that their data cannot be properly analyzed and what the specific issue is.

## Interface for simple user navigation (we have decided this will be a user generated file of some sort
### What it does
Allows the user to specify which file to load, how to configure the data, which analysis branch to run, and which sub analyses
to perform.

### Inputs
Blank file for user to fill with pre-determined structure
Data type: list of strings 

### Outputs
File with desired user specifications.

### Talks to
Data loader
Analysis and sub analysis "menus"
Data processing/plot creation components

### Side effects
If user inputs all valid commands in the file, when the file is run, each line is validated and the analysis runs.
If user inputs an invalid command, they see an error message indicating which command was not recognized.

## “Main menu”
### What it does
Offers two main analysis options to the user: energies or geometries. 
User is directed to the appropriate submenu based on their selection.

### Inputs
Either “energies” or “geometries.” 
Data type: string.

### Outputs
Submenu for analysis of either energies or geometries (not seen by user, but documented).
Error message if user did not input “energies” or “geometries.”
Data type: string

### Talks to:
Energies analysis submenu
Geometries analysis submenu
Interface for user navigation

### Side effects
If user entered a valid string, when the program is run the user sees a message "analyzing (menu option)..."
If user entered an invalid string, a user friendly error message is displayed.

## Energies analysis “sub menu”
### What it does
Collects user’s selection(s) from list of energy related plots and analyses.

### Inputs
User selection of plots to visualize desired aspects of the data.
Data type: list of strings

### Outputs
Validation of whether or not the user’s list is allowed.
Data type: Boolean (true if all strings in list are submenu options)
Initiates data processing/plot creation components associated with each string.
Data type: funcion call? Tells computer to run functions/jupyter cells to make the plots that the user has specified

### Talks to
Energies data processing/plot creation components
Interface component
"Main menu" component

### Side effects
If user enters the names of the plots they want to create successfully, they are presented with the results display for their selected plots
If the user enters a list with one or more invalid strings, they receive an error message to check that their plot types are in the sub menu.

## Energies: data processing/plot creation (one component per sub menu item?)
### What it does
Processes the energy data from the specified .hdf5 file and configuration. Generates the desired energy plot. This will be a separate component for each plot we might want to create.

### Inputs
The loaded simulation data with any additional configurations.

### Outputs
One type of energy plot for each of these components. Output will look like the output of a single plot-generating cell in the example notebook pyvibdmc_plotting_examples-checkpoint.ipynb. (Maybe these files are sent to the results display component before the user sees them as an output. This would allow us to organize what the user actually sees in a nicer way).
Data type: same as data type of corresponding jupyter notebook cell output
Error message if code fails to run.
Data type: string

### Talks to
Data loader
Submenu for energies analysis
Results display

### Side effects
The plots specified in the energies submenu are sent to the results display component to be organized. 
If the code for a certain plot fails to run, the user sees an error message that tells them what plot failed.

## Geometries analysis “sub menu”
### What it does
Lists geometry related plots and analyses for the user to choose from.
Collects user’s selection(s) from these options.

### Inputs
User selection of plots to visualize desired aspects of the data.
Data type: list of strings

### Outputs
Validation of whether or not the user’s list is allowed.
Data type: Boolean (true if all strings in list are submenu options)
Initiates data processing/plot creation components associated with each string.
Data type: funcion call? Tells computer to run functions/jupyter cells to make the plots that the user has specified

### Talks to
Geometries data processing/plot creation components
Navigation component
Main menu component

### Side effects
If user enters the names of the plots they want to create successfully, they are presented with the results display for their selected plots
If the user enters a list with one or more invalid strings, they receive an error message to check that their plot types are in the sub menu.

## Geometries: data processing/plot creation (one component per sub menu item?)
### What it does
Processes the geometry data from the specified .hdf5 file and configuration. Generates the desired geometry plot. There will be a separate component for each plot we might want to create.

### Inputs
The loaded simulation data.

### Outputs
One type of geometry plot for each of these components. Output will look like the output of a single plot-generating cell in the example notebook pyvibdmc_plotting_examples-checkpoint.ipynb. (Maybe these files are sent to the results display component before the user sees them as an output. This would allow us to organize what the user actually sees in a nicer way).
Data type: same as data type of corresponding jupyter notebook cell output
Error message if code fails to run.
Data type: string

### Talks to
Data loader
Submenu for geometries analysis
Results display

### Side effects
The plots specified in the energies submenu are sent to the results display component to be organized. 
If the code for a certain plot fails to run, the user sees an error message that tells them what plot failed.

## Results display
### What it does
Organizes/presents plots and analysis results for the user. 
Gives the user the ability to save or export results if wanted.

### Inputs
Plots generated by the data processing components the user selected. 
Data type: ??? depends on how we choose to save the output of, for example, a single Jupyter cell. The input for this component will be a set of those data types. Might be best to discuss how to do this in a smart way that preserves all the data the user might want when saving results of their analysis.

### Outputs
Displays results of analysis as a plot or a set of plots. These could be displayed in a single window so that the user can see them side by side, or maybe they can be displayed so that the user can scroll through individual plots. We need to figure out how we actually want the end point to look like.
Data type: not sure, this will be some type of element in the user interface

### Talks to
Data processing/plot creation components that were run
Navigation component

### Side effects
The user sees the results of the analysis displayed on their screen. They can choose to export the plots if desired, or can navigate back to the main menu or submenus to create other plots using the same file



