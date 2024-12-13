import pytest
import os
import subprocess
import sys
import yaml
from pathlib import Path

# test types:
# a smoke test is a very basic test to ensure the code runs without error on known-good input
# edge tests are tests that push the boundaries of what the code expects, such as missing keys, invalid ranges, etx.
# one-shot tests are tests with known inputs and expected outputs for a single, well-defined scenario
# pattern tests run the function multiple times with a series of inputs to ensure consistent behavior

@pytest.fixture
def valid_config(tmp_path):
    """
    Temporarily creates a valid config file for a known-good scenario.
    This config includes all required keys and values within normal ranges.
    """
    config = {
        'data_path': 'src/pyvisdmc/test_data',
        'molecule': 'h5o3',
        'sim_num': 0,
        'walkers': 5000,
        'timesteps': 20000,
        'start': 10000,
        'stop': 20000,
        'plots': ['eref', 'one_dist', 'mult_dist', 'two_d_dist'],
        'dist': [0,1],
        'mult_dists': [[2,3],[2,4],[2,0]],
        '2d_dists': [[2,3],[5,6]]
    }
    config_file = tmp_path / "config.yaml"
    with config_file.open('w') as f:
        yaml.dump(config, f)
    return config_file

def run_main(config_path):
    """
    Helper function to run main.py with temporary config file.
    """
    return subprocess.run(
        [sys.executable, "src/pyvisdmc/main.py", str(config_path)],
        capture_output=True, text=True
    )

def test_smoke(valid_config):
    """
    Smoke test to ensure main.py runs to completion with a valid config.
    - Checks return code is 0 (no error).
    - Checks last output string is printed to confirm main got to the end.
    """
    result = run_main(valid_config)
    assert result.returncode == 0, "Expected no error on valid input."
    assert "Version" in result.stdout, "Expected to see version info in output."
    assert "two_d_dist plot saved" in result.stdout, "Expected summary line in output."

def test_invalid_data_path(tmp_path):
    """
    Edge test for an invalid user input data_path.
    """
    config = {
        'data_path': 'path/that/does/not/exist',
        'molecule': 'h5o3',
        'sim_num': 0,
        'walkers': 5000,
        'timesteps': 20000,
        'start': 10000,
        'stop': 20000,
        'plots': ['eref']
    }

    config_file = tmp_path / "invalid_data_path_config.yaml"
    with config_file.open('w') as f:
        yaml.dump(config, f)

    result = run_main(config_file)
    assert result.returncode != 0, "Expected failure due to invalid data_path."
    assert f"Check config.yml. Provided data_path path/that/does/not/exist is not a valid directory." in result.stderr

def test_non_int_sim_num(tmp_path):
    """
    Edge test for sim_num not an integer.
    """
    config = {
        'data_path': 'src/pyvisdmc/test_data',
        'molecule': 'h5o3',
        'sim_num': "zero",  # non-integer
        'walkers': 5000,
        'timesteps': 20000,
        'start': 10000,
        'stop': 20000,
        'plots': ['eref']
    }
    config_file = tmp_path / "non_int_sim_num_config.yaml"
    with config_file.open('w') as f:
        yaml.dump(config, f)

    result = run_main(config_file)
    assert result.returncode != 0
    assert "Check config.yml. Simulation number must be a non-negative integer." in result.stderr


def test_negative_sim_num(tmp_path):
    """
    Edge test for nonsense sim number.
    """
    config = {
        'data_path': 'src/pyvisdmc/test_data',
        'molecule': 'h5o3',
        'sim_num': -1,  # negative
        'walkers': 5000,
        'timesteps': 20000,
        'start': 10000,
        'stop': 20000,
        'plots': ['eref']
    }
    config_file = tmp_path / "negative_sim_num_config.yaml"
    with config_file.open('w') as f:
        yaml.dump(config, f)

    result = run_main(config_file)
    assert result.returncode != 0
    assert "Check config.yml. Simulation number must be a non-negative integer." in result.stderr


def test_zero_walkers(tmp_path):
    """
    Edge test for walkers not positive.
    """
    config = {
        'data_path': 'src/pyvisdmc/test_data',
        'molecule': 'h5o3',
        'sim_num': 0,
        'walkers': 0,  # zero walkers
        'timesteps': 20000,
        'start': 10000,
        'stop': 20000,
        'plots': ['eref']
    }
    config_file = tmp_path / "zero_walkers_config.yaml"
    with config_file.open('w') as f:
        yaml.dump(config, f)

    result = run_main(config_file)
    assert result.returncode != 0
    assert "Check config.yml. The number of walkers must be a positive integer." in result.stderr


def test_non_int_walkers(tmp_path):
    """
    Edge test for walkers not an integer.
    """
    config = {
        'data_path': 'src/pyvisdmc/test_data',
        'molecule': 'h5o3',
        'sim_num': 0,
        'walkers': 5000.5,  # non-integer
        'timesteps': 20000,
        'start': 10000,
        'stop': 20000,
        'plots': ['eref']
    }
    config_file = tmp_path / "non_int_walkers_config.yaml"
    with config_file.open('w') as f:
        yaml.dump(config, f)

    result = run_main(config_file)
    assert result.returncode != 0
    assert "Check config.yml. The number of walkers must be a positive integer." in result.stderr


def test_zero_timesteps(tmp_path):
    """
    Edge test for timesteps not positive.
    """
    config = {
        'data_path': 'src/pyvisdmc/test_data',
        'molecule': 'h5o3',
        'sim_num': 0,
        'walkers': 5000,
        'timesteps': 0,  # zero timesteps
        'start': 10000,
        'stop': 20000,
        'plots': ['eref']
    }
    config_file = tmp_path / "zero_timesteps_config.yaml"
    with config_file.open('w') as f:
        yaml.dump(config, f)

    result = run_main(config_file)
    assert result.returncode != 0
    assert "Check config.yml. The number of timesteps must be a positive integer." in result.stderr


def test_non_int_timesteps(tmp_path):
    """
    Edge test for timesteps not an integer.
    """
    config = {
        'data_path': 'src/pyvisdmc/test_data',
        'molecule': 'h5o3',
        'sim_num': 0,
        'walkers': 5000,
        'timesteps': "twenty_thousand",  # non-integer
        'start': 10000,
        'stop': 20000,
        'plots': ['eref']
    }
    config_file = tmp_path / "non_int_timesteps_config.yaml"
    with config_file.open('w') as f:
        yaml.dump(config, f)

    result = run_main(config_file)
    assert result.returncode != 0
    assert "Check config.yml. The number of timesteps must be a positive integer." in result.stderr
    

def test_start_greater_than_stop(tmp_path):
    """
    Edge test to check that user input start > stop raises a ValueError.
    """
    config = {
        'data_path': 'src/pyvisdmc/test_data',
        'molecule': 'h5o3',
        'sim_num': 0,
        'walkers': 5000,
        'timesteps': 20000,
        'start': 15000,
        'stop': 10000,
        'plots': []
    }
    config_file = tmp_path / "config.yaml"
    with config_file.open('w') as f:
        yaml.dump(config, f)

    result = run_main(config_file)
    assert result.returncode != 0, "Should fail because start > stop."
    assert "Check config.yml. Start timestep 15000 cannot be greater than stop timestep 10000" in result.stderr


def test_start_exceeds_timesteps(tmp_path):
    """
    Edge test for start > timesteps.
    """
    config = {
        'data_path': 'src/pyvisdmc/test_data',
        'molecule': 'h5o3',
        'sim_num': 0,
        'walkers': 5000,
        'timesteps': 20000,
        'start': 25000,  # start > timesteps
        'stop': 30000,
        'plots': ['eref']
    }
    config_file = tmp_path / "start_exceeds_timesteps_config.yaml"
    with config_file.open('w') as f:
        yaml.dump(config, f)

    result = run_main(config_file)
    assert result.returncode != 0
    assert "Check config.yml. Start timestep 25000 or stop timestep 30000 exceed total timesteps 20000." in result.stderr


def test_stop_exceeds_timesteps(tmp_path):
    """
    Edge test to check that stop > timesteps raises a ValueError.
    """
    config = {
        'data_path': 'src/pyvisdmc/test_data',
        'molecule': 'h5o3',
        'sim_num': 0,
        'walkers': 5000,
        'timesteps': 20000,
        'start': 10000,
        'stop': 30000,
        'plots': []
    }
    config_file = tmp_path / "config.yaml"
    with config_file.open('w') as f:
        yaml.dump(config, f)

    result = run_main(config_file)
    assert result.returncode != 0, "Should fail because stop > timesteps."
    assert "Check config.yml. Start timestep 10000 or stop timestep 30000 exceed total timesteps 20000." in result.stderr


def test_non_int_start(tmp_path):
    """
    Edge test for start not an integer.
    """
    config = {
        'data_path': 'src/pyvisdmc/test_data',
        'molecule': 'h5o3',
        'sim_num': 0,
        'walkers': 5000,
        'timesteps': 20000,
        'start': 10000.5,  # non-integer
        'stop': 20000,
        'plots': ['eref']
    }
    config_file = tmp_path / "non_int_start_config.yaml"
    with config_file.open('w') as f:
        yaml.dump(config, f)

    result = run_main(config_file)
    assert result.returncode != 0
    assert "Check config.yml. Start and stop must be non-negative integers." in result.stderr


def test_non_int_stop(tmp_path):
    """
    Edge test for stop not an integer.
    """
    config = {
        'data_path': 'src/pyvisdmc/test_data',
        'molecule': 'h5o3',
        'sim_num': 0,
        'walkers': 5000,
        'timesteps': 20000,
        'start': 10000,
        'stop': "twenty_thousand",  # non-integer
        'plots': ['eref']
    }
    config_file = tmp_path / "non_int_stop_config.yaml"
    with config_file.open('w') as f:
        yaml.dump(config, f)

    result = run_main(config_file)
    assert result.returncode != 0
    assert "Check config.yml. Start and stop must be non-negative integers." in result.stderr


def test_neg_start_stop(tmp_path):
    """
    Edge test to see if the correct ValueError is raised when a negative start/stop time is given.
    """
    config = {
        'data_path': 'src/pyvisdmc/test_data',
        'molecule': 'h5o3',
        'sim_num': 0,
        'walkers': 5000,
        'timesteps': 20000,
        'start': -10000,
        'stop': 20000,
        'plots': ['eref']
    }
    config_file = tmp_path / "config.yaml"
    with config_file.open('w') as f:
        yaml.dump(config, f)

    result = run_main(config_file)
    assert result.returncode != 0, "Should fail due to negative start time."
    assert "Check config.yml. Start and stop must be non-negative integers." in result.stderr


def test_plots_not_a_list(tmp_path):
    """
    Edge test for plot argument as a string instead of a list.
    """
    config = {
        'data_path': 'src/pyvisdmc/test_data',
        'molecule': 'h5o3',
        'sim_num': 0,
        'walkers': 5000,
        'timesteps': 20000,
        'start': 10000,
        'stop': 20000,
        'plots': 'eref'  # not a list
    }
    config_file = tmp_path / "plots_not_a_list.yaml"
    with config_file.open('w') as f:
        yaml.dump(config, f)

    result = run_main(config_file)
    assert result.returncode != 0
    assert "Check config.yml. Plots must be a list of strings." in result.stderr


def test_plots_not_strings(tmp_path):
    """
    Edge test for plot list with a non-string element.
    """
    config = {
        'data_path': 'src/pyvisdmc/test_data',
        'molecule': 'h5o3',
        'sim_num': 0,
        'walkers': 5000,
        'timesteps': 20000,
        'start': 10000,
        'stop': 20000,
        'plots': ['eref', 123]  # non-string element
    }
    config_file = tmp_path / "plots_not_strings.yaml"
    with config_file.open('w') as f:
        yaml.dump(config, f)

    result = run_main(config_file)
    assert result.returncode != 0
    assert "Check config.yml. Plots must be a list of strings." in result.stderr


def test_no_plots_specified(tmp_path):
    """
    Edge test for case when no plots are specified.
    """
    config = {
        'data_path': 'src/pyvisdmc/test_data',
        'molecule': 'h5o3',
        'sim_num': 0,
        'walkers': 5000,
        'timesteps': 20000,
        'start': 10000,
        'stop': 20000,
        'plots': []  # empty list
    }
    config_file = tmp_path / "no_plots_config.yaml"
    with config_file.open('w') as f:
        yaml.dump(config, f)

    result = run_main(config_file)
    assert result.returncode == 0, "No plots scenario is considered success, so check exit message accordingly."
    assert "No plots specified." in result.stderr

    
def test_missing_key(tmp_path):
    """
    Edge test to see if the correct ValueError is raised when we remove a required key ('molecule').
    """
    config = {
        'data_path': 'src/pyvisdmc/test_data',
        'sim_num': 0,
        'walkers': 5000,
        'timesteps': 20000,
        'start': 10000,
        'stop': 20000,
        'plots': ['eref']
    }
    config_file = tmp_path / "config.yaml"
    with config_file.open('w') as f:
        yaml.dump(config, f)

    result = run_main(config_file)
    assert result.returncode != 0, "Should fail due to missing key."
    assert "Missing required key 'molecule'" in result.stderr, "Expected error message about missing key."


def test_invalid_dist_for_one_dist(tmp_path):
    """
    Edge test when the user input dist for 'one_dist' plot does not have length 2. 
    Test that length 3 raises a ValueError
    """
    config = {
        'data_path': 'src/pyvisdmc/test_data',
        'molecule': 'h5o3',
        'sim_num': 0,
        'walkers': 5000,
        'timesteps': 20000,
        'start': 10000,
        'stop': 20000,
        'plots': ['one_dist'],
        'dist': [0,1,2] # invalid length
    }
    config_file = tmp_path / "config.yaml"
    with config_file.open('w') as f:
        yaml.dump(config, f)

    result = run_main(config_file)
    assert result.returncode != 0, "Should fail because dist has invalid length."
    assert "For 'one_dist' plot, provide argument 'dist' and make sure it contains two atom indices." in result.stderr

def test_one_shot_known_values(tmp_path):
    """
    One shot test providing a minimal config with known values and a single plot.
    Checks for output lines from a successful run.
    """
    config = {
        'data_path': 'src/pyvisdmc/test_data',
        'molecule': 'h5o3',
        'sim_num': 0,
        'walkers': 5000,
        'timesteps': 20000,
        'start': 12000,
        'stop': 19000,
        'plots': ['eref'],
    }
    config_file = tmp_path / "config.yaml"
    with config_file.open('w') as f:
        yaml.dump(config, f)

    result = run_main(config_file)
    assert result.returncode == 0, "Expected success with known-good minimal config."
    assert "Molecule: h5o3" in result.stdout
    assert "Analyzing 5000 walkers over 20000 timesteps..." in result.stdout
    assert "Eref plot saved as h5o3_sim_0_zpe.png" in result.stdout

def test_one_shot_different_molecule(tmp_path):
    """
    Another one shot test, using a different molecule and plot type.
    """
    config = {
        'data_path': 'src/pyvisdmc/test_data',
        'molecule': 'h2o',
        'sim_num': 0,
        'walkers': 5000,
        'timesteps': 20000,
        'start': 0,
        'stop': 5000,
        'plots': ['two_d_dist'],
        '2d_dists': [[0,1], [1,2]]
    }
    config_file = tmp_path / "config.yaml"
    with config_file.open('w') as f:
        yaml.dump(config, f)

    result = run_main(config_file)
    assert result.returncode == 0, "Expected success with two_d_dist."
    assert "Molecule: h2o" in result.stdout
    assert "Analyzing 5000 walkers over 20000 timesteps..." in result.stdout
    assert "two_d_dist plot saved as h2o_sim_0_2d.png" in result.stdout
    
def test_pattern_multiple_runs(tmp_path):
    """
    Pattern test: runs main multiple times with increasing stop values.
    Ensures that for various stop values within timesteps, main completes successfully.
    """
    base_config = {
        'data_path': 'src/pyvisdmc/test_data',
        'molecule': 'h5o3',
        'sim_num': 0,
        'walkers': 5000,
        'timesteps': 20000,
        'plots': [],
    }

    for stop_val in [11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000]:
        cfg = base_config.copy()
        cfg['start'] = 10000
        cfg['stop'] = stop_val

        config_file = tmp_path / f"config_{stop_val}.yaml"
        with config_file.open('w') as f:
            yaml.dump(cfg, f)

        result = run_main(config_file)
        assert result.returncode == 0, f"Expected success with stop={stop_val}"
        assert "Analyzing 5000 walkers over 20000 timesteps..." in result.stdout
        assert "No plots specified. Exiting successfully..." in result.stdout
