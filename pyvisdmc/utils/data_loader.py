import pyvibdmc as pv
import h5py

def load_data(path_to_data):
    sim_data = pv.SimInfo(f'{path_to_data}/H5O3_0_sim_info.hdf5')
    return sim_data
