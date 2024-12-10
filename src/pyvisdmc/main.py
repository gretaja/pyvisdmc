import argparse
import yaml
from importlib.metadata import metadata, version
from pyvisdmc.plots.eref  import plot_eref
from pyvisdmc.plots.one_dist import plot_dist
from pyvisdmc.plots.mult_dist import plot_dists
from pyvisdmc.plots.two_d_dist import plot_2d
    
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('config', help='path to the YAML configuration file.')
    return parser.parse_args()

def main():     
    # loding package metadata
    pkg_name = "PyVisDMC"  
    pkg_meta = metadata(pkg_name)
    pkg_version = version(pkg_name)
    pkg_description = pkg_meta.get('Summary', 'No description available.')

    pyvisdmc_art = r"""

    O--O       O   O       O--O   O     O    O--O 
    |   |      |   | o     |   \  |\   / |  /    
    H--O  o  o O   O | o-o |    H | \ /  | H     
    |     |  |  \ /  |  \  |   /  |  H   |  \    
    O     o--H   H   | o-o O--O   O      O   O--O 
             |                               
          o--o                              

    """
    
    # print the startup message
    print(pyvisdmc_art)
    print(pkg_description)
    print(f"Version {pkg_version}")
    
    args = parse_args()
    with open(args.config, 'r') as file:
        config = yaml.safe_load(file)

    data_path = config.get('data_path')
    molecule = config.get('molecule')
    sim_num = config.get('sim_num')
    walkers = config.get('walkers')
    timesteps = config.get('timesteps')
    start = config.get ('start')
    stop = config.get('stop')
    plots = config.get('plots', [])

    print("")
    print(f"Molecule: {molecule}")
    print(f"Analyzing {walkers} walkers over {timesteps} timesteps...")
    print("")
   
    if 'eref' in plots:
        plot_eref(data_path,molecule,sim_num,walkers,timesteps,start,stop)
        print(f"Eref plot saved as {molecule}_sim_{sim_num}_zpe.png")
        print("")
    if 'one_dist' in plots:
        dist = config.get('dist')
        plot_dist(data_path,molecule,sim_num,walkers,timesteps,start,stop,dist)
        print(f"one_dist plot saved as {molecule}_sim_{sim_num}_distribution.png")
        print("")
    if 'mult_dist' in plots:
        dists = config.get('dists')
        plot_dists(data_path,molecule,sim_num,walkers,timesteps,start,stop,dists)
        print(f"mult_dist plot saved as {molecule}_sim_{sim_num}_mult_dists.png")
        print("")
    if 'two_d_dist' in plots:
        dists = config.get('dists')
        plot_2d(data_path,molecule,sim_num,walkers,timesteps,start,stop,dists)
        print(f"two_d_dist plot saved as {molecule}_sim_{sim_num}_2d.png")
        print("")

if __name__ == '__main__':
    main()
