###album catalog: cold-storage

import os
import requests

from album.runner.api import setup, get_data_path


env_file = """name: cryolo-napari
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
  - napari=0.4.17
  - pyqt
  - pip
  - pip:
      - nvidia-pyindex
      - cryoet-data-portal
      - 'cryolo[c11]'
      - napari-boxmanager
"""


def download_file(url, destination):
    """Download a file from a URL to a destination path."""
    response = requests.get(url, stream=True)
    with open(destination, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
            
def install():
    pass

def run():
    pass
    
setup(
    group="cryolo",
    name="napari-cryolo",
    version="0.0.1",
    title="cryOLO demo on cz cryoet data portal",
    description="cryolo on an example from the czii cryoet dataportal.",
    solution_creators=["Kyle Harrington"],
    cite=[{"text": "Wagner, T., Merino, F., Stabrin, M., Moriya, T., Antoni, C., Apelbaum, A., Hagel, P., Sitsel, O., Raisch, T., Prumbaum, D. and Quentin, D., 2019. SPHIRE-crYOLO is a fast and accurate fully automated particle picker for cryo-EM. Communications biology, 2(1), p.218..", "url": "https://cryolo.readthedocs.io/en/stable/index.html"}],
    tags=["imaging", "cryoet", "Python", "particle picking", "machine learning"],
    license="MIT",
    covers=[{
        "description": "Cover image for crYOLO from https://cryolo.readthedocs.io/en/stable/index.html.",
        "source": "cover.png"
    }],
    album_api_version="0.5.1",
    args=[],
    run=run,
    install=install,
    dependencies={"environment_file": env_file},
)
