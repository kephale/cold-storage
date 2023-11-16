###album catalog: cold-storage

import os
import requests

from album.runner.api import setup, get_data_path, get_args


env_file = """name: cryolo
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.8
  - 'numpy>=1.18.5'
  - libtiff
  - wxPython=4.1.1
  - adwaita-icon-theme
  - 'setuptools<66'
  - scipy
  - mrcfile
  - h5py
  - pip
  - pip:
      - cryoet-data-portal
"""


def download_file(url, destination):
    """Download a file from a URL to a destination path."""
    response = requests.get(url, stream=True)
    with open(destination, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)


def install():
    import subprocess
    import sys
    
    ordered_packages = ["nvidia-pyindex", 'cryolo[c11]==1.9.6']

    for package in ordered_packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def run():
    import subprocess

    command = ["cryolo_gui.py", "config"]

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
    name="config",
    version="0.0.1",
    title="crYOLO config",
    description="config command for crYOLO.",
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
        # General arguments
        {
            "name": "train_image_folder",
            "type": "directory",
            "description": "Path to the image folder containing the images to train on.",
            "required": False,
        },
        {
            "name": "train_annot_folder",
            "type": "directory",
            "description": "Path to folder containing the your annotation files.",
            "required": False,
        },
        {
            "name": "saved_weights_name",
            "type": "file",
            "description": "Path for saving final weights.",
            "required": False,
        },
        {
            "name": "architecture",
            "type": "string",
            "description": "Backend network architecture.",
            "required": False,
        },
        {
            "name": "input_size",
            "type": "integer",
            "description": "Input size for the network.",
            "required": False,
        },
        {
            "name": "norm",
            "type": "string",
            "description": "Normalization method applied to the images.",
            "required": False,
        },
        {
            "name": "num_patches",
            "type": "integer",
            "description": "(DEPRECATED) Number of patches if patch mode is used.",
            "required": False,
        },
        {
            "name": "overlap_patches",
            "type": "integer",
            "description": "(DEPRECATED) Overlap of patches.",
            "required": False,
        },
        # Denoising options
        {
            "name": "filtered_output",
            "type": "directory",
            "description": "Output folder for filtered images.",
            "required": False,
        },
        {
            "name": "filter",
            "type": "string",
            "description": "Noise filter applied before training/picking.",
            "required": False,
        },
        {
            "name": "low_pass_cutoff",
            "type": "float",
            "description": "Low pass filter cutoff frequency.",
            "required": False,
        },
        {
            "name": "janni_model",
            "type": "file",
            "description": "Path to JANNI model.",
            "required": False,
        },
        {
            "name": "janni_overlap",
            "type": "integer",
            "description": "Overlap of patches in pixels for JANNI.",
            "required": False,
        },
        {
            "name": "janni_batches",
            "type": "integer",
            "description": "Number of batches for JANNI.",
            "required": False,
        },
        # Training options
        {
            "name": "pretrained_weights",
            "type": "file",
            "description": "Path to h5 file for initialization for fine-tuning.",
            "required": False,
        },
        {
            "name": "train_times",
            "type": "integer",
            "description": "How often each image is presented during one epoch.",
            "required": False,
        },
        {
            "name": "batch_size",
            "type": "integer",
            "description": "Number of images processed in parallel during training.",
            "required": False,
        },
        {
            "name": "learning_rate",
            "type": "float",
            "description": "Step size during training.",
            "required": False,
        },
        {
            "name": "nb_epoch",
            "type": "integer",
            "description": "Maximum number of epochs for training.",
            "required": False,
        },
        {
            "name": "object_scale",
            "type": "float",
            "description": "Penalty scaling factor for missing picking particles.",
            "required": False,
        },
        {
            "name": "no_object_scale",
            "type": "float",
            "description": "Penalty scaling factor for picking background.",
            "required": False,
        },
        {
            "name": "coord_scale",
            "type": "float",
            "description": "Penalty scaling factor for errors in estimating position.",
            "required": False,
        },
        {
            "name": "class_scale",
            "type": "float",
            "description": "Penalty scaling factor for class estimation errors.",
            "required": False,
        },
        {
            "name": "debug",
            "type": "boolean",
            "description": "Provide statistics during training if true.",
            "required": False,
        },
        # Validation configuration
        {
            "name": "valid_image_folder",
            "type": "directory",
            "description": "Path to folder containing validation image files.",
            "required": False,
        },
        {
            "name": "valid_annot_folder",
            "type": "directory",
            "description": "Path to folder containing validation box files.",
            "required": False,
        },
        # Other option
        {
            "name": "log_path",
            "type": "directory",
            "description": "Path for log saving.",
            "required": False,
        },
    ],
    run=run,
    install=install,
    dependencies={"environment_file": env_file},
)
