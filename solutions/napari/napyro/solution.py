###album catalog: cold-storage

from io import StringIO

from album.runner.api import setup

env_file = StringIO(
    """name: napryo
channels:
  - pytorch-nightly
  - fastai
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
  - fsspec
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
  - album
  - "opencv-python-headless>=0.4.8"
  - "napari>=0.4.18"
  - "transformers>=4.36.1"
  - "imageio-ffmpeg>=0.4.8"
  - segment-anything
  - networkx
  - ipython  
  - pip:
    - idr-py
    - omero-rois
#    - imaris-ims-file-reader
#    - scanpy
#    - hypothesis
    - "tensorstore>=0.1.51"
    - compressed-segmentation
    - pyspng-seunglab
#    - "tabulous>=0.5.4"
    - imglyb
    - imglyb-bdv
#    - "pyheif>=0.7"
    - "ome-zarr>=0.8.0"
    - tootapari
    - Mastodon.py
    - "qrcode>=7.4.1"
#    - "napari-process-points-and-surfaces>=0.4.2" # leads to 0.4.17 dependency
    - pygeodesic
#    - skan
#    - napari-boids
#    - "napari-matplotlib>=1" # has a requirement of <0.4.18
    - "cellpose-napari>=0.1.4"
    - "tensorflow-macos;  platform_system==\"Darwin\" and platform_machine==\"arm64\""
    - "tensorflow-metal;  platform_system==\"Darwin\" and platform_machine==\"arm64\""    
    - "pydantic-ome-ngff>=0.2.3"
    - "python-dotenv>=0.21"
    - validate-pyproject[all]
    - ndjson
    - requests_toolbelt
    - cytosim
    - "xgboost>=2"
    - "cryoet-data-portal>=2"
    - "napari-cryoet-data-portal>=0.2.1"
#    - bpy
#    - black
#    - pre-commit
    - mrcfile
    - "starfile>=0.5.0"
    - "imodmodel>=0.0.7"
    - cryotypes
#    - "git+https://github.com/KosinskiLab/pyTME.git"
    - napari-omero
    - napari-stable-diffusion
#    - tyssue
#    - napari-tyssue
#    - napari-metadata
#    - napari-graph
    - napari-conference
    - napari-workshop-browser
    - napari-skimage-regionprops
    - "git+https://github.com/kevinyamauchi/morphometrics.git"
    - blik
    - napari-properties-plotter
    - napari-properties-viewer
    - napari-label-interpolator
"""
)


def run():
    import napari

    viewer = napari.Viewer()
    
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
