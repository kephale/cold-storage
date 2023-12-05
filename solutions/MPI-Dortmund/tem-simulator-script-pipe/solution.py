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
    - "git+https://github.com/MPI-Dortmund/tem-simulator-scripts.git"
"""


def local_repository_path():
    data_path = get_data_path()
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    return os.path.join(data_path, "ctffind")


def install():
    import subprocess
    import zipfile
    import shutil
    from urllib.request import urlopen
    from io import BytesIO

    # Define the URL and the local path for the zip file
    tem_simulator_url = "https://sourceforge.net/projects/tem-simulator/files/TEM-simulator_1.3.zip/download"
    local_zip_path = "/tmp/TEM-simulator_1.3.zip"

    # Download the zip file
    with urlopen(tem_simulator_url) as response:
        with open(local_zip_path, "wb") as out_file:
            shutil.copyfileobj(response, out_file)

    # Unzip the contents
    with zipfile.ZipFile(local_zip_path, "r") as zip_ref:
        zip_ref.extractall("/tmp")

    # Find the directory that was just created by unzipping
    src_directory = "/tmp/TEM-simulator_1.3/src"  # Modify this path as needed

    # Enter the src subdirectory and run make
    os.chdir(src_directory)

    # Get the current conda environment's include and lib paths for fftw3
    conda_prefix = os.environ["CONDA_PREFIX"]
    include_path = os.path.join(conda_prefix, "include")
    lib_path = os.path.join(conda_prefix, "lib")

    # Set environment variables for the make process
    os.environ["C_INCLUDE_PATH"] = include_path
    os.environ["LIBRARY_PATH"] = lib_path

    # Run make
    subprocess.run(["make"], check=True)

    # Move the resulting binary to the conda environment's bin directory
    bin_path = os.path.join(conda_prefix, "bin")
    shutil.move("TEM-simulator", bin_path)

    # Get the directory path of the FFTW library
    fftw_lib_dir = os.path.join(conda_prefix, "lib")

    # Update the rpath of the TEM-simulator binary to include the directory path of the FFTW library
    tem_simulator_binary = os.path.join(bin_path, "TEM-simulator")
    subprocess.run(
        ["install_name_tool", "-add_rpath", fftw_lib_dir, tem_simulator_binary],
        check=True,
    )


def run():
    import os
    import subprocess

    args = get_args()
    pdb_path = getattr(args, "pdbs", "pdbs/*.pdb")

    # Count the number of PDB files in the specified directory
    pdb_directory = os.path.dirname(pdb_path)
    pdb_files = [file for file in os.listdir(pdb_directory) if file.endswith(".pdb")]
    npdbs = len(pdb_files)  # Number of PDB files

    script_path = "tsimscripts_pipe.sh"
    command = [script_path, f"--npdbs {npdbs}"]

    # Add the rest of the arguments to the command
    for arg in vars(args):
        value = getattr(args, arg)
        command.append(f"--{arg} {value}")

    # Run the subprocess and capture the output
    try:
        # Use Popen to execute the script and capture the output
        with subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=1,
            universal_newlines=True,
        ) as proc:
            for (
                line
            ) in proc.stdout:  # You can also use proc.stderr here to capture errors
                print(line, end="")  # Print the output in real-time

        # Wait for the subprocess to finish and get the exit code
        proc.communicate()
        if proc.returncode != 0:
            print(f"Script ended with return code: {proc.returncode}")
    except Exception as e:
        print(f"Error running tem-simulator-script: {e}")

    # TODO check if there was an error by inspecting logs in the output directory simulator.log


setup(
    group="MPI-Dortmund",
    name="tem-simulator-script-pipe",
    version="0.0.3",
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
        {
            "description": "Screenshot of the volume render of a reconstruction created with this solution. Visualized in napari.",
            "source": "cover.png",
        }
    ],
    album_api_version="0.5.1",
    args=[
        {
            "name": "pdbs",
            "type": "string",
            "description": "Path to PDB files",
            "default": "/Users/kharrington/git/MPI-Dortmund/tem-simulator-scripts/pdbs/*.pdb",
        },
        {
            "name": "output",
            "type": "string",
            "description": "Output directory",
            "default": "out_sim_tomo_1",
        },
        {
            "name": "random_seed",
            "type": "integer",
            "description": "Random seed",
            "default": 10,
        },
        {
            "name": "pdbs_fil",
            "type": "string",
            "description": "Path to filament PDB files",
            "default": "/Users/kharrington/git/MPI-Dortmund/tem-simulator-scripts/resources/filament_files/*.pdb",
        },
        {
            "name": "settings_fil",
            "type": "string",
            "description": "Path to settings file",
            "default": "/Users/kharrington/git/MPI-Dortmund/tem-simulator-scripts/resources/filament_files/*.json",
        },
        {
            "name": "nsubs",
            "type": "integer",
            "description": "Number of substitutions",
            "default": 100,
        },
        {"name": "dose", "type": "integer", "description": "Dose", "default": 15000},
        {"name": "fiducialsize", "type": "integer", "description": "Size of fiducials"},
        {"name": "vesiclesize", "type": "integer", "description": "Size of vesicles"},
        {"name": "nvesicle", "type": "integer", "description": "Number of vesicles"},
        {"name": "nfiducial", "type": "integer", "description": "Number of fiducials"},
        {
            "name": "defocus_lower",
            "type": "integer",
            "description": "Lower limit of defocus",
        },
        {
            "name": "defocus_upper",
            "type": "integer",
            "description": "Upper limit of defocus",
        },
        {"name": "thickness", "type": "integer", "description": "Thickness"},
        {
            "name": "s1",
            "type": "boolean",
            "description": "Early abort flag",
            "default": False,
        },
    ],
    run=run,
    install=install,
    dependencies={"environment_file": env_file},
)

if False:
    import os
    import subprocess
    from album.runner.api import get_active_solution

    arg_list = get_active_solution().setup()["args"]

    os.chdir("/tmp/tsimtest")

    pdb_path = get_active_solution().get_arg("pdbs")["default"]

    # Count the number of PDB files in the specified directory
    pdb_directory = os.path.dirname(pdb_path)
    pdb_files = [file for file in os.listdir(pdb_directory) if file.endswith(".pdb")]
    npdbs = len(pdb_files)  # Number of PDB files

    script_path = "tsimscripts_pipe.sh"
    command = [script_path, f"--npdbs {npdbs}"]

    arg_keys = [arg["name"] for arg in get_active_solution().setup()["args"]]

    # Add the rest of the arguments to the command
    for arg in arg_keys:
        value = get_active_solution().get_arg(arg)["default"]
        command.append(f"--{arg} {value}")

    print(f"command: {' '.join(command)}")

    # Run the subprocess and capture the output
    try:
        # Use Popen to execute the script and capture the output
        with subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=1,
            universal_newlines=True,
        ) as proc:
            for (
                line
            ) in proc.stdout:  # You can also use proc.stderr here to capture errors
                print(line, end="")  # Print the output in real-time

        # Wait for the subprocess to finish and get the exit code
        proc.communicate()
        if proc.returncode != 0:
            print(f"Script ended with return code: {proc.returncode}")
    except Exception as e:
        print(f"Error running tem-simulator-script: {e}")
