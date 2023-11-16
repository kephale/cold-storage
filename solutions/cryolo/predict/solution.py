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

    command = ["cryolo_gui.py", "predict"]

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
    name="predict",
    version="0.0.1",
    title="crYOLO predict",
    description="prediction command for crYOLO.",
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
            "name": "conf",
            "type": "file",
            "description": "Path to the crYOLO configuration file.",
            "required": True,
        },
        {
            "name": "weights",
            "type": "file",
            "description": "Path to the trained model.",
            "required": True,
        },
        {
            "name": "input",
            "type": "file",
            "description": "Path to one or multiple image folders/images.",
            "required": True,
        },
        {
            "name": "output",
            "type": "directory",
            "description": "Path to the output folder.",
            "required": True,
        },
        # Optional arguments
        {
            "name": "threshold",
            "type": "float",
            "description": "Confidence threshold.",
            "required": False,
        },
        {
            "name": "gpu",
            "type": "string",
            "description": "Specify which GPU(s) should be used.",
            "required": False,
        },
        {
            "name": "distance",
            "type": "integer",
            "description": "Distance for particle removal.",
            "required": False,
        },
        {
            "name": "minsize",
            "type": "integer",
            "description": "Minimum estimated diameter for particles.",
            "required": False,
        },
        {
            "name": "maxsize",
            "type": "integer",
            "description": "Maximum estimated diameter for particles.",
            "required": False,
        },
        {
            "name": "prediction_batch_size",
            "type": "integer",
            "description": "Number of images predicted in one batch.",
            "required": False,
        },
        {
            "name": "gpu_fraction",
            "type": "float",
            "description": "Fraction of memory per GPU used during prediction.",
            "required": False,
        },
        {
            "name": "num_cpu",
            "type": "integer",
            "description": "Number of CPUs used during filtering/filament tracing.",
            "required": False,
        },
        {
            "name": "norm_margin",
            "type": "float",
            "description": "Relative margin size for normalization.",
            "required": False,
        },
        {
            "name": "monitor",
            "type": "boolean",
            "description": "Activate monitoring mode for input folder.",
            "required": False,
        },
        {
            "name": "otf",
            "type": "boolean",
            "description": "On the fly filtering, filtered micrographs will not be written to disk.",
            "required": False,
        },
        {
            "name": "cleanup",
            "type": "boolean",
            "description": "Delete filtered images after prediction is done.",
            "required": False,
        },
        {
            "name": "skip",
            "type": "boolean",
            "description": "Skip images that were already picked.",
            "required": False,
        },
        # Filament options
        {
            "name": "filament",
            "type": "boolean",
            "description": "Activate filament mode.",
            "required": False,
        },
        {
            "name": "box_distance",
            "type": "integer",
            "description": "Distance in pixel between two boxes.",
            "required": False,
        },
        {
            "name": "minimum_number_boxes",
            "type": "integer",
            "description": "Minimum number of boxes per filament.",
            "required": False,
        },
        {
            "name": "straightness_method",
            "type": "string",
            "description": "Method to measure the straightness of a line.",
            "required": False,
        },
        {
            "name": "straightness_threshold",
            "type": "float",
            "description": "Threshold value for the straightness method.",
            "required": False,
        },
        {
            "name": "search_range_factor",
            "type": "float",
            "description": "The search range for connecting boxes.",
            "required": False,
        },
        {
            "name": "angle_delta",
            "type": "integer",
            "description": "Angle delta in degree.",
            "required": False,
        },
        {
            "name": "directional_method",
            "type": "string",
            "description": "Method for directional filament estimation.",
            "required": False,
        },
        {
            "name": "filament_width",
            "type": "integer",
            "description": "Filament width in pixel.",
            "required": False,
        },
        {
            "name": "mask_width",
            "type": "integer",
            "description": "Mask width in pixel for convolution method.",
            "required": False,
        },
        {
            "name": "nosplit",
            "type": "boolean",
            "description": "(DEPRECATED) Do not split to curved filaments.",
            "required": False,
        },
        {
            "name": "nomerging",
            "type": "boolean",
            "description": "Do not merge filaments.",
            "required": False,
        },
        # Tomography options
        {
            "name": "tomogram",
            "type": "boolean",
            "description": "Activate tomography picking mode.",
            "required": False,
        },
        {
            "name": "tracing_search_range",
            "type": "integer",
            "description": "Search range in pixel for tracing.",
            "required": False,
        },
        {
            "name": "tracing_memory",
            "type": "integer",
            "description": "Tracing memory in frames for particle tracking.",
            "required": False,
        },
        {
            "name": "minimum_number_boxes_3d",
            "type": "integer",
            "description": "Minimum number of boxes per filament in 3D mode.",
            "required": False,
        },
        {
            "name": "tracing_min_length",
            "type": "integer",
            "description": "Minimum number of boxes in one trace for valid particle.",
            "required": False,
        },
        {
            "name": "tracing_window_size",
            "type": "integer",
            "description": "Window width when averaging filament positions.",
            "required": False,
        },
        {
            "name": "tracing_min_edge_weight",
            "type": "float",
            "description": "Minimum edge weight for filament tracing.",
            "required": False,
        },
        {
            "name": "tracing_merge_thresh",
            "type": "float",
            "description": "Threshold for merging filaments in tracing.",
            "required": False,
        },
        # Deprecated/Experimental/Special options
        {
            "name": "patch",
            "type": "integer",
            "description": "(DEPRECATED) Number of patches.",
            "required": False,
        },
        {
            "name": "write_empty",
            "type": "boolean",
            "description": "Write empty box files when no particle could be found.",
            "required": False,
        },
    ],
    run=run,
    install=install,
    dependencies={"environment_file": env_file},
)
