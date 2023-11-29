###album catalog: cold-storage

import os
import requests

from album.runner.api import setup, get_data_path, get_args


env_file = """name: cryolo
channels:
  - conda-forge
  - defaults
dependencies:
  - pyqt=5
  - python=3.10
  - 'numpy>=1.18.5'
  - libtiff
  - wxPython=4.1.1
  - adwaita-icon-theme
  - 'setuptools<66'
  - pip
  - pip:
      - nvidia-pyindex
      - cryoet-data-portal
      - 'cryolo[c11]'
"""


def download_file(url, destination):
    """Download a file from a URL to a destination path."""
    response = requests.get(url, stream=True)
    with open(destination, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)


def install():
    pass


def run():
    import subprocess

    command = ["cryolo_gui.py", "train"]

    args_dict = get_args()

    # Required arguments
    if "conf" in args_dict:
        command.extend(["-c", args_dict["conf"]])
    if "warmup" in args_dict:
        command.extend(["-w", str(args_dict["warmup"])])

    # Optional arguments
    if "gpu" in args_dict:
        command.extend(["-g"] + args_dict["gpu"].split())
    if "num_cpu" in args_dict:
        command.extend(["-nc", str(args_dict["num_cpu"])])
    if "gpu_fraction" in args_dict:
        command.extend(["--gpu_fraction", str(args_dict["gpu_fraction"])])
    if "early" in args_dict:
        command.extend(["-e", str(args_dict["early"])])
    if "fine_tune" in args_dict:
        command.append("--fine_tune")
    if "layers_fine_tune" in args_dict:
        command.extend(["-lft", str(args_dict["layers_fine_tune"])])
    if "cleanup" in args_dict:
        command.append("--cleanup")
    if "ignore_directions" in args_dict:
        command.append("--ignore_directions")
    if "seed" in args_dict:
        command.extend(["--seed", str(args_dict["seed"])])
    if "warm_restarts" in args_dict:
        command.append("--warm_restarts")
    if "skip_augmentation" in args_dict:
        command.append("--skip_augmentation")

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running crYOLO: {e}")


setup(
    group="cryolo",
    name="train",
    version="0.0.1",
    title="crYOLO train",
    description="training command for crYOLO.",
    solution_creators=["Kyle Harrington"],
    cite=[
        {
            "text": "Wagner, T., Merino, F., Stabrin, M., Moriya, T., Antoni, C., Apelbaum, A., Hagel, P., Sitsel, O., Raisch, T., Prumbaum, D. and Quentin, D., 2019. SPHIRE-crYOLO is a fast and accurate fully automated particle picker for cryo-EM. Communications biology, 2(1), p.218..",
            "url": "https://cryolo.readthedocs.io/en/stable/index.html",
        }
    ],
    tags=["imaging", "cryoet", "Python", "particle picking", "machine learning"],
    license="MIT",
    covers=[
        {
            "description": "Cover image for crYOLO from https://cryolo.readthedocs.io/en/stable/index.html.",
            "source": "cover.png",
        }
    ],
    album_api_version="0.5.1",
    args=[
        {
            "name": "conf",
            "type": "file",
            "description": "Path to configuration file for crYOLO.",
            "required": True,
        },
        {
            "name": "warmup",
            "type": "integer",
            "description": "Number of warmup epochs.",
            "required": True,
        },
        {
            "name": "gpu",
            "type": "string",
            "description": "GPU(s) to be used, separated by whitespace.",
            "required": False,
        },
        {
            "name": "num_cpu",
            "type": "integer",
            "description": "Number of CPUs used during training.",
            "required": False,
        },
        {
            "name": "gpu_fraction",
            "type": "float",
            "description": "Fraction of memory per GPU used during training.",
            "required": False,
        },
        {
            "name": "early",
            "type": "integer",
            "description": "Early stop patience.",
            "required": False,
        },
        {
            "name": "fine_tune",
            "type": "boolean",
            "description": "Set to true for fine-tuning mode.",
            "required": False,
        },
        {
            "name": "layers_fine_tune",
            "type": "integer",
            "description": "Layers to be trained when using fine tuning.",
            "required": False,
        },
        {
            "name": "cleanup",
            "type": "boolean",
            "description": "Delete filtered images after training.",
            "required": False,
        },
        {
            "name": "ignore_directions",
            "type": "boolean",
            "description": "Skip directional learning for filament training data.",
            "required": False,
        },
        {
            "name": "seed",
            "type": "integer",
            "description": "Seed for random number generator.",
            "required": False,
        },
        {
            "name": "warm_restarts",
            "type": "boolean",
            "description": "Use warm restarts and cosine annealing during training.",
            "required": False,
        },
        {
            "name": "skip_augmentation",
            "type": "boolean",
            "description": "Deactivate data augmentation during training.",
            "required": False,
        },
    ],
    run=run,
    install=install,
    dependencies={"environment_file": env_file},
)
