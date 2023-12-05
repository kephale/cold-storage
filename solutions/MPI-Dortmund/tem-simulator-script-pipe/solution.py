
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
    
    args = get_args()
    pdb_path = getattr(args, 'pdbs', 'pdbs/*.pdb')  # Get the path to PDB files

    # Count the number of PDB files in the specified directory
    pdb_directory = os.path.dirname(pdb_path)
    pdb_files = [file for file in os.listdir(pdb_directory) if file.endswith('.pdb')]
    npdbs = len(pdb_files)  # Number of PDB files

    script_path = "tsimscripts_pipe.sh"
    command = [script_path, f"--npdbs={npdbs}"]  # Include npdbs in the command

    # Add the rest of the arguments to the command
    for arg in vars(args):
        value = getattr(args, arg)
        command.append(f"--{arg}={value}")

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
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
