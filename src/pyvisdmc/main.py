import argparse
import yaml
from pyvisdmc.utils.data_loader import load_data
from pyvisdmc.plots.eref  import plot_eref

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('config', help='path to the YAML configuration file.')
    return parser.parse_args()

def main():
    args = parse_args()
    with open(args.config, 'r') as file:
        config = yaml.safe_load(file)

    molecule = config.get('molecule')
    sim_num = config.get('sim_num')
    walkers = config.get('walkers')
    timesteps = config.get('timesteps')
    start = config.get ('start')
    stop = config.get('stop')
   
    plots = config.get('plots', [])
    
    if 'eref' in plots:
        plot_eref(molecule,sim_num,walkers,timesteps,start,stop)
    if 'one_dist' in plots:
        plot_dist(molecule,sim_num,walkers,timesteps,start,stop)

if __name__ == '__main__':
    main()
