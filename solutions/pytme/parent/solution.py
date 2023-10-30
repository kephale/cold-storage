from io import StringIO

from album.runner.api import setup

# Please import additional modules at the beginning of your method declarations.
# More information: https://docs.album.solutions/en/latest/solution-development/

env_file = StringIO(
    """channels:
  - pytorch-nightly
  - conda-forge
  - defaults
dependencies:
  - python=3.9
  - zarr
  - numpy
  - imageio
  - ome-zarr
  - opencv
  - pip
  - dask
  - pandas[version='<2']
  - scipy
  - matplotlib
  - xarray
  - hdf5
  - omero-py
  - pytorch[version='>=2.1']
  - torchvision
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
  - libnetcdf
  - ruff
  - meshio
  - pip:
      - ipython
      - black
      - pre-commit
      - album
      - mrcfile
      - python-dotenv
      - ndjson
      - cryoet-data-portal
      - napari-cryoet-data-portal
      - starfile
      - imodmodel
      - cryotypes
      - "git+https://github.com/teamtomo/membrain-seg.git"
"""
)


def run():
    pass


setup(
    group="pytme",
    name="parent",
    version="0.0.1",
    title="Parent environment for pytme.",
    description="A parent environment with git main of pytme",
    solution_creators=["Kyle Harrington"],
    cite=[{"text": "KosinskiLab.", "url": "https://github.com/KosinskiLab/pyTME"}],
    tags=["imaging", "cryoet", "Python", "template matching"],
    license="MIT",
    covers=[],
    album_api_version="0.5.1",
    args=[],
    run=run,
    dependencies={"environment_file": env_file},
)
