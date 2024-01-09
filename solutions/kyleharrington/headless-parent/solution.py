###album catalog: cold-storage

from io import StringIO

from album.runner.api import setup

env_file = StringIO(
    """channels:
  - pytorch-nightly
  - conda-forge
  - defaults
dependencies:
  - python>=3.10
  - pybind11
  - pip
  - boost-cpp
  - mpfr
  - gmp
  - cgal
  - numpy
  - scyjava >= 1.8.1
  - scipy
  - scikit-image
  - matplotlib
  - pandas
  - pytables
  - jupyter
  - notebook
  - jupytext
  - quantities
  - ipywidgets
  - ipyvolume
  - meshio
  - zarr
  - xarray
  - hdf5
  - mpfr
  - gmp
  - pyvista
  - omero-py
  - pyimagej >= 1.4.0
  - pyopencl
  - reikna
  - openjdk=11
  - jupyterlab
  - pytorch
  - torchvision
  - diffusers
  - einops
  - fire
  - maven
  - pillow
  - openjpeg
  - imagecodecs
  - "bokeh>=2.4.2,<3"
  - python-graphviz
  - ipycytoscape
  - fftw
  - s3fs
  - pooch
  - yappi
  - ftfy
  - tqdm
  - imageio
  - pyarrow
  - squidpy
  - h5py
  - tifffile
  - nilearn
  - flake8
  - pytest
  - asv
  - pint
  - pytest-cov
  - mypy
  - opencv
  - flask
  - vtk
  - libnetcdf
  - ruff
  - confuse
  - jpype1 >= 1.4.1
  - labeling >= 0.1.12
  - lazy_loader
  - lxml
  - ninja
  - pythran
  - gql
  - boto3
  - pip:
    - idr-py
    - album
    - omero-rois
    - imageio-ffmpeg
    - transformers
    - gradio
    - imaris-ims-file-reader
    - scanpy
    - pyarrow
    - invagination
    - hypothesis
    - tensorstore
    - alabaster
    - compressed-segmentation
    - pyspng-seunglab
    - tabulous
    - imglyb
    - imglyb-bdv
    - fibsem_tools
    - pyheif
    - "ome-zarr>=0.3.0"
    - importmagic
    - epc
    - ruff
    - python-lsp-server[all]
    - pylsp-mypy
    - pyls-isort
    - python-lsp-black
    - pyls-memestra
    - pylsp-rope
    - python-lsp-ruff
    - snakeviz
    - pyaudio
    - Mastodon.py
    - qrcode
    - opencv-python-headless
    - pygeodesic
    - skan
    - stardist
    - "tensorflow-macos;  platform_system==\\\"Darwin\\\" and platform_machine==\\\"arm64\\\""
    - "tensorflow-metal;  platform_system==\\\"Darwin\\\" and platform_machine==\\\"arm64\\\""    
    - pydantic-ome-ngff
    - python-dotenv
    - validate-pyproject[all]
    - segment-anything
    - ndjson
    - requests_toolbelt
    - networkx
    - cytosim
    - xgboost
    - cryoet-data-portal
    - mrcfile
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
    import napari

    viewer = napari.Viewer()
    
    napari.run()


setup(
    group="kyleharrington",
    name="headless-parent",
    version="0.0.1",
    title="Parent environment for a big python environment for cryoET.",
    description="A parent environment for a big python environment for cryoET",
    solution_creators=["Kyle Harrington"],
    cite=[{"text": "Kyle. Also check out TeamTomo", "url": ""}],
    tags=["imaging", "cryoet", "Python"],
    license="MIT",
    covers=[],
    album_api_version="0.5.1",
    args=[],
    run=run,
    dependencies={"environment_file": env_file},
)
