
###album catalog: cold-storage

import os
import subprocess

from album.runner.api import setup, get_data_path, get_args



env_file = """channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.9
  - biotite
  - pip
  - pip:
    - tem-simulator-scripts
"""


def local_repository_path():
    data_path = get_data_path()
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    return os.path.join(data_path, "ctffind")

def install():
    pass

def run():
    import os
    import subprocess
    
    args = get_args()
    pdb_path = getattr(args, 'pdbs', 'pdbs/*.pdb')

    # Count the number of PDB files in the specified directory
    pdb_directory = os.path.dirname(pdb_path)
    pdb_files = [file for file in os.listdir(pdb_directory) if file.endswith('.pdb')]
    npdbs = len(pdb_files)  # Number of PDB files

    script_path = "tsimscripts_pipe.sh"
    command = [script_path, f"--npdbs={npdbs}"]

    # Add the rest of the arguments to the command
    for arg in vars(args):
        value = getattr(args, arg)
        command.append(f"--{arg}={value}")

    # Run the subprocess and capture the output
    try:
        # Use Popen to execute the script and capture the output
        with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, universal_newlines=True) as proc:
            for line in proc.stdout:  # You can also use proc.stderr here to capture errors
                print(line, end='')  # Print the output in real-time

        # Wait for the subprocess to finish and get the exit code
        proc.communicate()
        if proc.returncode != 0:
            print(f"Script ended with return code: {proc.returncode}")
    except Exception as e:
        print(f"Error running tem-simulator-script: {e}")


setup(
    group="MPI-Dortmund",
    name="tem-simulator-script-pipe",
    version="0.0.1",
    title="tem-simulator-script",
    description="tem simulator script.",
    solution_creators=["Kyle Harrington"],
    cite=[
        {
            "text": "H. Rullgård, L.-G. Öfverstedt, S. Masich, B. Daneholt, and O. Öktem, Simulation of transmission electron microscope images of biological specimens, Journal of Microscopy, 242 (2011). Provided by https://github.com/MPI-Dortmund/tem-simulator-scripts which is part of TomoTwin",
            "url": "https://tem-simulator.sourceforge.net/",
        }
    ],
    tags=[
        "cryo-electron microscopy",
        "simulator",
        "tem",
        "image processing",
    ],
    license="MIT",
    covers=[
    ],
    album_api_version="0.5.1",
    args=[
        {"name": "pdbs", "type": "string", "description": "Path to PDB files", "default": "/Users/kharrington/git/MPI-Dortmund/tem-simulator-scripts/pdbs/*.pdb"},
        {"name": "output", "type": "string", "description": "Output directory", "default": "out_sim_tomo_1"},
        {"name": "random_seed", "type": "integer", "description": "Random seed", "default": 10},
        {"name": "pdbs_fil", "type": "string", "description": "Path to filament PDB files", "default": "/Users/kharrington/git/MPI-Dortmund/tem-simulator-scripts/resources/filament_files/*.pdb"},
        {"name": "settings_fil", "type": "string", "description": "Path to settings file", "default": "/Users/kharrington/git/MPI-Dortmund/tem-simulator-scripts/resources/filament_files/*.json"},
        {"name": "nsubs", "type": "integer", "description": "Number of substitutions", "default": 100},
        {"name": "dose", "type": "integer", "description": "Dose", "default": 15000}        
    ],
    run=run,
    install=install,
    dependencies={"environment_file": env_file},
)
