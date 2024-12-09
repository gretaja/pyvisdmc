import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("white")

def plot_eref(molecule,sim_num,sim_data,start,stop):
    """Saves a .png of a line plot of the average enesemble energy with a simulation,
    calculates the zero point energy (ZPE) over a specified start and stopping point"""
    
    print(f"Creating eref plot from time {start} to time {stop} for {molecule}...")

    vref = sim_data.get_vref(ret_cm=True) #generates an array of the timesteps and the average energy of the ensemble at that step
    ZPE = np.mean(vref[start:stop][:,1]) #calculate the average energy in the relevant range of time steps (while the energy is stable)

    plt.plot(vref[:,0],vref[:,1])
    #sns.lineplot(data=vref[:,1])

    plt.hlines(y= ZPE,xmin = start,xmax= stop, color = 'tab:orange', label='ZPE: {0:.2f}'.format(ZPE))
    plt.legend()

    plt.ylabel('Eref (cm$^{-1}$)')
    plt.xlabel('Timestep (1 a.u.)')
    plt.savefig(f'{molecule}_sim_{sim_num}_zpe.png',bbox_inches='tight')

    plt.clf()
