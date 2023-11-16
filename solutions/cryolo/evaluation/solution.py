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

    command = ["cryolo_gui.py", "evaluation"]

    args_dict = get_args()

    # Add all the arguments from args_dict to command
    for arg, value in args_dict.items():
        if value is not None:
            command.append(f"--{arg}")
            if isinstance(value, list):  # For arguments that accept multiple values
                command.extend(map(str, value))
            else:
                command.append(str(value))

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running crYOLO: {e}")


setup(
    group="cryolo",
    name="evaluation",
    version="0.0.1",
    title="crYOLO evaluation",
    description="evaluation command for crYOLO.",
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
        # Required arguments
        {
            "name": "config",
            "type": "file",
            "description": "Path to configuration file (.json).",
            "required": True,
        },
        {
            "name": "weights",
            "type": "file",
            "description": "Path to trained model (.h5 file).",
            "required": True,
        },
        {
            "name": "runfile",
            "type": "file",
            "description": "Path to runfile (.json) for model evaluation.",
            "required": False,
        },
        {
            "name": "output",
            "type": "file",
            "description": "Path to file where the results are written as .html.",
            "required": False,
        },
        # Optional arguments
        {
            "name": "images",
            "type": "directory",
            "description": "Path to folder with test images (ground truth).",
            "required": False,
        },
        {
            "name": "boxfiles",
            "type": "directory",
            "description": "Path to folder with box files (ground truth).",
            "required": False,
        },
        {
            "name": "gpu",
            "type": "string",
            "description": "Specify which GPU should be used.",
            "required": False,
        },
    ],
    run=run,
    install=install,
    dependencies={"environment_file": env_file},
)
