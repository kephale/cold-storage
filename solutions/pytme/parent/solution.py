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
  - python>=3.11
  - numpy
  - imageio
  - pip
  - imagecodecs
  - scipy
  - fftw
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
  - ruff
  - napari
  - magicgui
  - pyfftw
  - pyqt
  - pip:
      - ipython
      - black
      - pre-commit
      - mrcfile
      - starfile
      - imodmodel
      - cryotypes
      - "git+https://github.com/KosinskiLab/pyTME.git"
"""
)


def run():
    pass


setup(
    group="pytme",
    name="parent",
    version="0.0.2",
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
