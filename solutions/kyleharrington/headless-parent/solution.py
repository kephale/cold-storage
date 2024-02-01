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
  - python>=3.8
  - pybind11
  - pip
  - boost-cpp
  - cgal
  - numpy >= 1.26
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
  - meshio
  - zarr
  - xarray
  - hdf5
  - mpfr
  - gmp
  - pyvista
#  - omero-py
  - pyimagej >= 1.4.0
  - pyopencl
  - reikna
  - openjdk=11
  - jupyterlab
  - pytorch
  - torchvision
  - diffusers
  - dill    
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
  - tqdm >= 4.38
  - imageio
  - pyarrow >= 13
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
#  - opencv
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
  - album
  - "opencv-python-headless>=0.4.8"
  - "transformers>=4.36.1"
  - "imageio-ffmpeg>=0.4.8"
  - segment-anything
  - networkx
  - ipython      
  - pip:
#    - idr-py
#    - omero-rois
    - imaris-ims-file-reader
    - scanpy
#    - invagination
#    - hypothesis
    - "tensorstore>=0.1.51"
    - compressed-segmentation
    - pyspng-seunglab
#    - "tabulous>=0.5.4"
    - imglyb
    - imglyb-bdv
    - "pyheif>=0.7"
    - "ome-zarr>=0.8.0"
    - epc
    - pygeodesic
    - skan
    - "pydantic-ome-ngff>=0.2.3"
    - "python-dotenv>=0.21"
    - validate-pyproject[all]
    - segment-anything
    - ndjson
    - requests_toolbelt
    - networkx
#    - cytosim
    - "xgboost>=2"
    - cryoet-data-portal>=2
    - mrcfile
    - "starfile>=0.5.0"
    - "imodmodel>=0.0.7"
    - cryotypes
#    - "git+https://github.com/KosinskiLab/pyTME.git"
"""
)


def run():
    import IPython

    IPython.start_ipython()


setup(
    group="kyleharrington",
    name="headless-parent",
    version="0.0.3",
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
