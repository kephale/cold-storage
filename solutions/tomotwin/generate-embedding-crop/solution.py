###album catalog: cold-storage

import os
import requests

from album.runner.api import setup, get_data_path, get_cache_path, get_args


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
  - cuda-version=11.8
  - protobuf[version='>3.20']
  - tensorboard
  - optuna
  - mysql-connector-python
  - pip
  - pytorch-metric-learning
  - pip:
      - tomotwin-cryoet
      - cryoet-data-portal
      - mrcfile
"""


MODEL_URL = "https://zenodo.org/records/8358240/files/tomotwin_latest.pth?download=1"
DATA_DIR_URL = "https://ftp.ebi.ac.uk/empiar/world_availability/10499/"

def download_file(url, destination):
    """Download a file from a URL to a destination path."""
    response = requests.get(url, stream=True)
    with open(destination, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
            
def install():
    data_path = get_data_path()
    # Ensure the data path exists
    if not os.path.exists(data_path):
        os.makedirs(data_path)

    # Download the model
    model_path = os.path.join(data_path, "tomotwin_latest.pth")
    if not os.path.exists(model_path):
        download_file(MODEL_URL, model_path)
    

def run():
    import json
    from cryoet_data_portal import Client, Tomogram
    from scipy.ndimage import zoom
    import mrcfile
    import numpy as np
    import shutil

    args = get_args()
    model_path = os.path.join(get_data_path(), "tomotwin_latest.pth")
    mrc_path = args.mrcfile
    output_path = args.embeddingfile

    # Crop coordinates
    x_start, x_end = args.x_start, args.x_end
    y_start, y_end = args.y_start, args.y_end
    z_start, z_end = args.z_start, args.z_end
    
    print(f"Embedding tomogram crop from mrc ({mrc_path}) to embedding ({output_path})")

    with mrcfile.open(mrc_path) as mrc:
        data = mrc.data[z_start:z_end, y_start:y_end, x_start:x_end]

    # Temporary path for cropped MRC
    temp_cropped_mrc_path = os.path.join("/tmp/temp_cropped.mrc")
    with mrcfile.new(temp_cropped_mrc_path, overwrite=True) as mrc:
        mrc.set_data(data)
    
    # Continue with the adjusted mrc_path pointing to the cropped version
    mrc_path = temp_cropped_mrc_path
    output_path = get_args().embeddingfile
    
    print(f"Embedding tomogram from mrc ({mrc_path}) to embedding ({output_path})")

    embedding_path = os.path.join(get_cache_path(), "out/embed/tomo/")
    embeddings = os.path.join(embedding_path, f"{os.path.splitext(os.path.basename(mrc_path))[0]}_embeddings.temb")
    clustering_path = os.path.join(get_cache_path(), "out/clustering/")
    mask_path = os.path.join(get_cache_path(), "out/mask/")

    # Ensure that embedding_path and clustering_path exist
    os.makedirs(embedding_path, exist_ok=True)
    os.makedirs(clustering_path, exist_ok=True)

    if get_args().use_median_mask:
        print("Using median mask to filter points for embedding.")
        # Generate mask
        os.system(f"CUDA_VISIBLE_DEVICES=0,1 tomotwin_tools.py embedding_mask median -i {mrc_path} -m {model_path} -o {mask_path}")
    
        # Calculate embedding
        os.system(f"CUDA_VISIBLE_DEVICES=0,1 tomotwin_embed.py tomogram -m {model_path} -v {mrc_path} -b 256 -o {embedding_path} -s 1 --mask {mask_path}/{os.path.splitext(os.path.basename(mrc_path))[0]}_mask.mrc")
    else:
        print("Not using a median mask, this may take longer than embedding with a mask.")
        # Calculate embedding
        os.system(f"CUDA_VISIBLE_DEVICES=0,1 tomotwin_embed.py tomogram -m {model_path} -v {mrc_path} -b 256 -o {embedding_path} -s 1")

    # Calculate umap
    print("Estimate UMAP manifold and generate embedding mask")
    os.system(f"tomotwin_tools.py umap -i {embeddings} -o {clustering_path}")

    shutil.copytree(clustering_path, output_path, dirs_exist_ok=True)

    
setup(
    group="tomotwin",
    name="generate-embedding-crop",
    version="0.0.9",
    title="Generate an embedding with TomoTwin for a crop of a mrc",
    description="TomoTwin on an example from the czii cryoet dataportal.",
    solution_creators=["Kyle Harrington"],
    cite=[{"text": "Rice, G., Wagner, T., Stabrin, M. et al. TomoTwin: generalized 3D localization of macromolecules in cryo-electron tomograms with structural data mining. Nat Methods (2023). https://doi.org/10.1038/s41592-023-01878-z.", "url": "https://tomotwin-cryoet.readthedocs.io/en/stable/index.html"}],
    tags=["imaging", "cryoet", "Python", "particle picking", "machine learning"],
    license="MIT",
    covers=[{
        "description": "Cover image for TomoTwin tutorial 2 applied to data from cryoet-data-portal TS_030 from doi:10.1038/s41592-022-01746-2. The image shows a highlighted region of embedding space that covers some particles in the tomogram.",
        "source": "cover.png"
    }],
    album_api_version="0.5.1",
    args=[
        {"name": "mrcfile", "type": "file", "required": True, "description": "Path to the MRC file"},
        {"name": "embeddingfile", "type": "file", "required": True, "description": "Path for the output embedding file"},
        {"name": "use_median_mask", "type": "boolean", "required": False, "default": False,  "description": "Use median mask for filtering"},
        {"name": "x_start", "type": "integer", "required": True, "description": "Crop start on the X axis"},
        {"name": "x_end", "type": "integer", "required": True, "description": "Crop end on the X axis"},
        {"name": "y_start", "type": "integer", "required": True, "description": "Crop start on the Y axis"},
        {"name": "y_end", "type": "integer", "required": True, "description": "Crop end on the Y axis"},
        {"name": "z_start", "type": "integer", "required": True, "description": "Crop start on the Z axis"},
        {"name": "z_end", "type": "integer", "required": True, "description": "Crop end on the Z axis"},
    ],
    run=run,
    install=install,
    dependencies={
        "parent": {
            "group": "tomotwin",
            "name": "generate-embedding",
            "version": "0.0.7",
        }
    },    
)

