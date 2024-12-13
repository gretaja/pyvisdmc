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
    assert "Check config.yml. Stop timestep 30000 exceeds the total timesteps 20000" in result.stderr

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
    assert "For 'one_dist' plot, 'dist' must be provided and contain two atom indices." in result.stderr

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
        'timesteps': 5000,
        'start': 1000,
        'stop': 2000,
        'plots': ['eref'],
    }
    config_file = tmp_path / "config.yaml"
    with config_file.open('w') as f:
        yaml.dump(config, f)

    result = run_main(config_file)
    assert result.returncode == 0, "Expected success with known-good minimal config."
    assert "Molecule: h5o3" in result.stdout
    assert "Analyzing 5000 walkers over 5000 timesteps..." in result.stdout
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
        'timesteps': 5000,
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
    assert "Analyzing 5000 walkers over 10000 timesteps..." in result.stdout
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

    for stop_val in [1000, 1001, 1250, 2348, 5000, 5998, 9999, 10000]:
        cfg = base_config.copy()
        cfg['start'] = 0
        cfg['stop'] = stop_val

        config_file = tmp_path / f"config_{stop_val}.yaml"
        with config_file.open('w') as f:
            yaml.dump(cfg, f)

        result = run_main(config_file)
        assert result.returncode == 0, f"Expected success with stop={stop_val}"
        assert "Analyzing 5000 walkers over 10000 timesteps..." in result.stdout
        assert "No plots specified. Exiting successfully..." in result.stdout

