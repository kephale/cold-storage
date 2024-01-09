###album catalog: cold-storage

from io import StringIO

from album.runner.api import setup

env_file = StringIO(
    """channels:
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
  - "opencv-python-headless>=0.4.8"
  - pip:
    - idr-py
    - album
    - omero-rois
    - imageio-ffmpeg
    - transformers
    - imaris-ims-file-reader
    - scanpy
    - pyarrow
    - invagination
    - hypothesis
    - "tensorstore>=0.1.51"
    - compressed-segmentation
    - pyspng-seunglab
    - "tabulous>=0.5.4"
    - imglyb
    - imglyb-bdv
    - "pyheif>=0.7"
    - "ome-zarr>=0.8.0"
    - epc
    - pygeodesic
    - skan
    - "tensorflow-macos;  platform_system==\\\"Darwin\\\" and platform_machine==\\\"arm64\\\""
    - "tensorflow-metal;  platform_system==\\\"Darwin\\\" and platform_machine==\\\"arm64\\\""    
    - "pydantic-ome-ngff>=0.2.3"
    - "python-dotenv>=0.21"
    - validate-pyproject[all]
    - segment-anything
    - ndjson
    - requests_toolbelt
    - networkx
    - cytosim
    - "xgboost>=2"
    - cryoet-data-portal>=2
    - mrcfile
    - ipython
    - mrcfile
    - "starfile>=0.5.0"
    - "imodmodel>=0.0.7"
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
