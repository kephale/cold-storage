###album catalog: cold-storage

import os
import requests

from album.runner.api import setup, get_data_path


env_file = """name: tomotwin
channels:
  - nvidia
  - pytorch
  - rapidsai
  - conda-forge
  - defaults
dependencies:
  - pytorch[version='>=2.1']
  - torchvision
  - pandas[version='<2']
  - scipy
  - numpy
  - matplotlib
  - pytables
  - cuml=23.04
  - cudatoolkit=11.8
  - protobuf[version='>3.20']
  - tensorboard
  - optuna
  - mysql-connector-python
  - pip
  - bs4
  - pip:
      - tomotwin-cryoet
"""


MODEL_URL = "https://zenodo.org/records/8358240/files/tomotwin_latest.pth?download=1"
DATA_DIR_URL = "https://ftp.ebi.ac.uk/empiar/world_availability/10499/"

def download_file(url, destination):
    """Download a file from a URL to a destination path."""
    response = requests.get(url, stream=True)
    with open(destination, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

def download_recursive(base_url, destination_path):
    """Recursively download directories and files starting from a base URL."""
    from bs4 import BeautifulSoup
    
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    for link in soup.find_all('a'):
        href = link.get('href')
        if href.endswith("/"):
            # This is a directory; recursively download its contents
            download_recursive(base_url + href, os.path.join(destination_path, href))
        else:
            # This is a file; download it
            download_file(base_url + href, os.path.join(destination_path, href))

            
def load_tiff_directory(directory_path):
    import tifffile
    import numpy as np
    
    # Load all tiff files from the directory
    tiff_files = [f for f in os.listdir(directory_path) if f.endswith('.tif') or f.endswith('.tiff')]
    tiff_files.sort()  # Ensure files are in order
    
    # Load the first image to get dimensions
    first_image = tifffile.imread(os.path.join(directory_path, tiff_files[0]))
    height, width = first_image.shape
    
    # Initialize a 3D array for all images
    all_images = np.zeros((len(tiff_files), height, width), dtype=np.uint8)  # Assuming voxel type is UNSIGNED BYTE
    
    for i, tiff_file in enumerate(tiff_files):
        all_images[i] = tifffile.imread(os.path.join(directory_path, tiff_file))
    
    return all_images

def write_to_mrc(data, output_path):
    import mrcfile
    
    with mrcfile.new(output_path, overwrite=True) as mrc:
        mrc.set_data(data)
            
def install():
    data_path = get_data_path()
    # Ensure the data path exists
    if not os.path.exists(data_path):
        os.makedirs(data_path)

    # Download the model
    model_path = os.path.join(data_path, "tomotwin_latest.pth")
    if not os.path.exists(model_path):
        download_file(MODEL_URL, model_path)

    # Download the data directory
    download_recursive(DATA_DIR_URL, data_path)

    # Load tiff images and convert to 3D array
    images_3d = load_tiff_directory(data_path)
    
    # Write 3D array to mrc file
    mrc_path = os.path.join(data_path, "output.mrc")
    write_to_mrc(images_3d, mrc_path)
    

def run():
    model_path = os.path.join(get_data_path(), "tomotwin_latest.pth")
    input_mrc = os.path.join(get_data_path(), "output.mrc")
    rescaled_mrc = os.path.join(get_data_path(), "rescaled.mrc")
    
    # Assuming the `e2proc3d.py` and other tools are available in PATH
    print("Downscale tomogram")
    os.system(f"e2proc3d.py --apix=5.9359 --fouriershrink=1.684 {input_mrc} {rescaled_mrc}")
    print("Embedding tomogram")
    
    os.system(f"CUDA_VISIBLE_DEVICES=0,1 tomotwin_embed.py tomogram -m {model_path} -v {rescaled_mrc} -b 256 -o out/embed/tomo/ -s 2")
    print("Estimate UMAP manifold and generate embedding mask")
    os.system("tomotwin_tools.py umap -i out/embed/tomo/tomo_embeddings.temb -o out/clustering/")

setup(
    group="tomotwin",
    name="tutorial-2",
    version="0.0.1",
    title="TomoTwin tutorial 2.",
    description="A tutorial for TomoTwin",
    solution_creators=["Kyle Harrington"],
    cite=[{"text": "Rice, G., Wagner, T., Stabrin, M. et al. TomoTwin: generalized 3D localization of macromolecules in cryo-electron tomograms with structural data mining. Nat Methods (2023). https://doi.org/10.1038/s41592-023-01878-z.", "url": "https://tomotwin-cryoet.readthedocs.io/en/stable/index.html"}],
    tags=["imaging", "cryoet", "Python", "particle picking", "machine learning"],
    license="MIT",
    covers=[{
        "description": "Cover image for TomoTwin. The image comes from the TomoTwin documentation: https://tomotwin-cryoet.readthedocs.io.",
        "source": "cover.png"
    }],
    album_api_version="0.5.1",
    args=[],
    run=run,
    install=install,
    dependencies={"environment_file": env_file},
)

