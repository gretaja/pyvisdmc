**Notes**  
PyVisDMC requires Python 3.8 or above.
Dependencies: h5py, matplotlib, numpy, pandas, pyvibdmc, PyYAML, seaborn

---

This program was created at the University of Washington in fall 2024 as a final project for the course Software Development for Data Scientists (CSE 583). Team members on this project are acknowledged for their contributions below:

* Greta Jacobson  
* Lauren Dressler  
* Ramses Llobet

---

**PyVisDMC** is a Python-based visualization tool designed to read simulation data produced by [**PyVibDMC**](https://pyvibdmc.readthedocs.io/en/latest/) and generate a variety of informative plots relevant for data analysis. We hope PyVisDMC can be a useful tool for students, researchers, and anyone needing to quickly visualize simulation outputs without writing extensive plotting code.

## **Features**

* **Integration with PyVibDMC**:  
  Reads `.hdf5` files generated by PyVibDMC to produce various plots without code recompilation.  
* **Plot selection via configuration file**:  
  Specify the types of plots (e.g., energy convergence, bond length distributions) directly in a YAML config file without modifying code.  
* **Set of Built-in Plot Types**:  
  * Average energy of the ensemble over time, including calculation of the zero point energy (ZPE) over specified start and stop points, called `eref`  
  * Probability distribution of bond lengths 
  * …others?  
* **Command-Line Usability**:  
  * Run `pyvisdmc config.yaml` from the command line to generate all requested plots at once  
  * Quickly switch between different simulation data by editing the config.yml file  
  * No need to re-compile any code for new datasets  
* **PNG Output Format**:  
  * Plots saved as a PNG by default  
  * Maybe we can add other options for output formats eventually  
* **Built-In Logging**:  
  * Automatically includes simulation parameters (number of walkers, timesteps, etc.) in plot annotations and PNG names  
  * Easily trace which plots correspond to which PyVibDMC runs  
* **Adaptable**:  
  * Users can add custom plot functions with minimal code changes

---
## **Installation**

To install the most recent version of PyVisDMC, run the following from the command line: 

```bash
pip install git+https://github.com/gretaja/pyvisdmc.git
```


## **Usage**

1. **Generate Data Using PyVibDMC**:  
   PyVibDMC produces the `.hdf5` file(s) to be analyzed.  
2. **Prepare a config.yaml File**:  
   Specify the path to your data folder, the name of the simulated molecule, the number of walkers, the number of timesteps, the start/stop indices for analysis, and the list of plots to be made (e.g., `eref`, ...).
3. **Run PyVisDMC in the command line**:  
```bash   
pyvisdmc config.yaml
```
4. PyVisDMC will find the desired PyVibDMC output file, create the requested plots, and save them in the current directory (maybe we can have a user-specified output path as an alternative here).

---

## **Example Configuration File (config.yaml)**

```yaml
molecule: h2o 
sim_num: 0  
walkers: 5000 
timesteps: 20000  
start: 5000  
stop: 20000

plots:  
  - eref  
```
---

## **How to Contribute**

**Fork the PyVisDMC Repository** on GitHub:

```bash
git clone git@github.com:yourGitHubUsername/pyvisdmc.git # creates forked repository 
git remote add upstream git@github.com:gretaja/pyvisdmc.git # address of original repository  
git remote -v # runs a check
```

**Stay Updated**:

To remain up to date with the latest changes to PyVisDMC, run the following:

```bash  
git fetch upstream 
git merge upstream/master
```

If the merge is successful, run `git push` to update your forked repository.

**Open a Pull Request** on GitHub if you’d like your changes to be included in the main PyVisDMC repository.
