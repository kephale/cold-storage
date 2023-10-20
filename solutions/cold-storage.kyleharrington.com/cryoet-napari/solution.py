from io import StringIO

from album.runner.api import setup

# Please import additional modules at the beginning of your method declarations.
# More information: https://docs.album.solutions/en/latest/solution-development/

env_file = StringIO(
    """channels:
  - nvidia
  - pytorch-nightly
  - conda-forge
  - defaults
  - rapidsai
  - cryoem
dependencies:
  - python=3.10
  - zarr
  - numpy
  - imageio
  - ome-zarr
  - opencv
  - napari
  - pip
  - dask
  - pandas[version='<2']
  - scipy
  - pyqt
  - matplotlib
  - xarray
  - hdf5
  - omero-py
  - pytorch[version='>=2.1']
  - torchvision
  - diffusers
  - einops
  - pillow
  - openjpeg
  - imagecodecs
  - fftw
  - s3fs
  - pooch
  - qtpy
  - superqt
  - yappi
  - imageio
  - tqdm
  - tifffile
  - flake8
  - h5py
  - mypy
  - pint
  - opencv
  - flask
  - vtk
  - libnetcdf
  - ruff
  - lxml
  - jupyter
  - notebook
  - pytables
  - ipywidgets
  - meshio
  - mysql-connector-python
  - protobuf[version='>3.20']
  - tensorboard
  - optuna
  - eman-dev[version='<=2.99.53']
  - pip:
      - "git+https://github.com/napari/napari.git"
      - blik
      - ipython
      - black
      - pre-commit
      - album
      - transformers
      - tensorstore
      - pydantic-ome-ngff
      - python-dotenv
      - ndjson
      - segment-anything
      - snakeviz
      - cryohub
      - cryoet-data-portal
      - napari-cryoet-data-portal
      - starfile
      - imodmodel
      - cryotypes
      - "git+https://github.com/teamtomo/membrain-seg.git"
      - cryodrgn
      - tomotwin-cryoet
      - lxml==4.9.0
"""
)


def run():
    pass


setup(
    group="cold-storage.kyleharrington.com",
    name="cryoet-napari",
    version="0.0.1",
    title="Parent environment for some napari cryoet tools.",
    description="A parent environment for cryoet solutions",
    solution_creators=["Kyle Harrington"],
    cite=[{"text": "Kyle Harrington.", "url": "https://kyleharrington.com"}],
    tags=["imaging", "cryoet", "Python"],
    license="MIT",
    covers=[],
    album_api_version="0.5.1",
    args=[],
    run=run,
    dependencies={"environment_file": env_file},
)
