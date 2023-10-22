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
    group="cold-storage.kyleharrington.com",
    name="membrane_seg_parent",
    version="0.0.1",
    title="Parent environment for membrane_seg.",
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
