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
  - pythreejs
  - ipyvolume
  - vispy
  - meshio
  - zarr
  - xarray
  - hdf5
  - mpfr
  - gmp
  - pyvista
  - pyqt
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
  - napari-segment-blobs-and-things-with-membranes
  - s3fs
  - pooch
  - qtpy
  - superqt
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
  - pytest-qt
  - pytest-cov
  - mypy
  - opencv
  - flask
  - vedo
  - vtk
  - libnetcdf
  - ruff
  - qscintilla2
  - confuse
  - jpype1 >= 1.4.1
  - labeling >= 0.1.12
  - lazy_loader
  - lxml
  - ocl_icd_wrapper_apple
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
    - napari-process-points-and-surfaces
    - opencv-python-headless
    - pygeodesic
    - skan
    - napari-boids
    - napari-matplotlib
    - stardist-napari
    - cellpose-napari
    - stardist
    - "tensorflow-macos;  platform_system==\\\"Darwin\\\" and platform_machine==\\\"arm64\\\""
    - "tensorflow-metal;  platform_system==\\\"Darwin\\\" and platform_machine==\\\"arm64\\\""    
    - pydantic-ome-ngff
    - python-dotenv
    - validate-pyproject[all]
    - segment-anything
    - ndjson
    - requests_toolbelt
    - PartSeg
    - networkx
    - btrack[napari]>=0.6.1
    - cytosim
    - xgboost
    - cryoet-data-portal
    - napari-cryoet-data-portal
     - mrcfile
     - bpy
     - ipython
     - black
     - pre-commit
     - mrcfile
     - starfile
     - imodmodel
     - cryotypes
     - "git+https://github.com/KosinskiLab/pyTME.git"
     - napari-omero
     - napari-stable-diffusion
     - tyssue
     - napari-tyssue
     - napari-metadata
     - napari-graph
     - napari-conference
     - napari-workshop-browser
     - napari-skimage-regionprops
     - "git+https://github.com/kevinyamauchi/morphometrics.git"
"""
)


def run():
    import napari

    napari.run()


setup(
    group="napari",
    name="napyro",
    version="0.0.1",
    title="Parent environment for a big napari environment for cryoET.",
    description="A parent environment for a big napari environment for cryoET",
    solution_creators=["Kyle Harrington"],
    cite=[{"text": "Kyle. Also check out TeamTomo", "url": ""}],
    tags=["imaging", "cryoet", "Python", "napari"],
    license="MIT",
    covers=[],
    album_api_version="0.5.1",
    args=[],
    run=run,
    dependencies={"environment_file": env_file},
)