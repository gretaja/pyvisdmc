import argparse
import yaml
import os
from importlib.metadata import metadata, version
from pyvisdmc.plots.eref import plot_eref
from pyvisdmc.plots.one_dist import plot_dist
from pyvisdmc.plots.mult_dist import plot_dists
from pyvisdmc.plots.two_d_dist import plot_2d
from pyvisdmc.utils.data_loader import load_data, sim_info

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('config', help='path to the YAML configuration file.')
    return parser.parse_args()

def main():
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

    print(pyvisdmc_art)
    print(pkg_description)
    print(f"Version {pkg_version}")

    args = parse_args()
    with open(args.config, 'r') as file:
        config = yaml.safe_load(file)

    # Validate required keys
    required_keys = ['data_path', 'molecule', 'sim_num', 'walkers', 'timesteps', 'start', 'stop', 'plots']
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required key '{key}' in config file.")

    data_path = config['data_path']
    molecule = config['molecule']
    sim_num = config['sim_num']
    walkers = config['walkers']
    timesteps = config['timesteps']
    start = config['start']
    stop = config['stop']
    plots = config['plots']

    # edge checks
    if not os.path.isdir(data_path):
        raise ValueError(f"Provided data_path '{data_path}' is not a valid directory.")
    else:
        pass
    if start < 0 or stop < 0:
        raise ValueError("Check config.yml. Start and stop must be non-negative.")
    else:
        pass
    if start > stop:
        raise ValueError(f"Check config.yml. Start timestep {start} cannot be greater than stop timestep {stop}.")
    else:
        pass
    if stop > timesteps:
        raise ValueError(f"Check config.yml. Stop timestep {stop} exceeds the total timesteps {timesteps}.")
    else:
        pass

    print("")
    print(f"Molecule: {molecule}")
    print(f"Analyzing {walkers} walkers over {timesteps} timesteps...")
    print("")

    sim_data = load_data(data_path, molecule, sim_num, walkers, timesteps)
    analyzer, weights = sim_info(sim_data, start, stop)

    if 'eref' in plots:
        plot_eref(molecule, sim_num, sim_data, start, stop)
        print(f"Eref plot saved as {molecule}_sim_{sim_num}_zpe.png")
        print("")
    if 'one_dist' in plots:
        dist = config.get('dist')
        if dist is None or len(dist) != 2:
            raise ValueError("For 'one_dist' plot, provide argument 'dist' and make sure it contains two atom indices.")
        else:
            pass
        plot_dist(molecule, analyzer, weights, dist)
        print(f"one_dist plot saved as {molecule}_{dist[0]}{dist[1]}_dist.png")
        print("")
    if 'mult_dist' in plots:
        mult_dists = config.get('mult_dists')
        if mult_dists is None or not all(len(d) == 2 for d in mult_dists):
            raise ValueError("For 'mult_dist' plot, 'mult_dists' must be provided and each must have two atom indices.")
        else:
            pass
        plot_dists(molecule, sim_num, analyzer, weights, mult_dists, hist=False, exp=False)
        print(f"mult_dist plot saved as {molecule}_sim_{sim_num}_mult_dists.png")
        print("")
    if 'two_d_dist' in plots:
        two_d_dists = config.get('2d_dists')
        if two_d_dists is None or not all(len(d) == 2 for d in two_d_dists):
            raise ValueError("For 'two_d_dist' plot, '2d_dists' must be provided and each must have two atom indices.")
        else:
            pass
        plot_2d(molecule, sim_num, analyzer, weights, two_d_dists, exp=False)
        print(f"two_d_dist plot saved as {molecule}_sim_{sim_num}_2d.png")
        print("")
    else:
        print("No plots specified. Exiting successfully...")

if __name__ == '__main__':
    main()
