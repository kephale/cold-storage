###album catalog: cold-storage

import os

from album.runner.api import setup, get_data_path, get_args

env_file = """name: cryocanvas
channels:
  - nvidia
  - pytorch
  - rapidsai
  - conda-forge
  - defaults
dependencies:
  - pytorch[version='>=2.1']
  - torchvision
  - pandas[version='<2']
  - scipy
  - numpy
  - matplotlib
  - pytables
  - cuml=23.04
  - cudatoolkit=11.8
  - protobuf[version='>3.20']
  - tensorboard
  - optuna
  - mysql-connector-python
  - pip
  - bs4
  - flask
  - pip:
      - tomotwin-cryoet
      - cryoet-data-portal
      - mrcfile
"""


def install():
    import subprocess
    # Clone the repository
    repo_url = "git@github.com:kephale/cryocanvas.git"
    clone_path = os.path.join(get_data_path(), "cryocanvas")
    if not os.path.exists(clone_path):
        subprocess.check_call(["git", "clone", repo_url, clone_path])

def run():
    import subprocess

    # Construct the command
    flask_app_path = os.path.join(get_data_path(), "cryocanvas", "backend", "main.py")
    command = ["python", flask_app_path, get_args().model_file, get_args().mrc_file]
    
    # Add Flask port if provided
    command.extend(["--port", str(get_args().flask_port)])

    # Start the Flask server
    subprocess.run(command, check=True)

setup(
    group="cryocanvas",
    name="backend",
    version="0.0.1",
    title="CryoCanvas backend",
    description="TBD.",
    solution_creators=["Kyle Harrington"],
    cite=[
        {
            "text": "TBD.",
            "url": "https://github.com/kephale/cryocanvas",
        }
    ],
    tags=[
        "tomography",
        "cryo-electron",
        "interactive",
        "segmentation",
        "napari",
    ],
    license="MIT",
    covers=[
        {
            "description": "TBD.",
            "source": "cover.png",
        }
    ],
    album_api_version="0.5.1",
    args=[
        {
            "name": "mrc_file",
            "type": "file",
            "description": "Input MRC file that stores the tomographic tilt series.",
            "required": True,
        },
        {
            "name": "model_file",
            "type": "file",
            "description": "TomoTwin model file",
            "required": True,
        },
        {
            "name": "flask_port",
            "type": "integer",
            "description": "port for the flask server",
            "required": True,
        },
    ],
    run=run,
    install=install,
    dependencies={"environment_file": env_file},
)    
