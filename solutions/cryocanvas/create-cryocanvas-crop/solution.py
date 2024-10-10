 ###album catalog: cold-storage

from album.runner.api import setup, get_data_path
import uuid

MODEL_URL = "https://zenodo.org/records/8358240/files/tomotwin_latest.pth?download=1"
DATA_DIR_URL = "https://ftp.ebi.ac.uk/empiar/world_availability/10499/"

def download_file(url, destination):
    """Download a file from a URL to a destination path."""
    import requests
    response = requests.get(url, stream=True)
    with open(destination, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

def install():
    import os
    data_path = get_data_path()
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    model_path = os.path.join(data_path, "tomotwin_latest.pth")
    if not os.path.exists(model_path):
        download_file(MODEL_URL, model_path)

def run():
    from album.runner.api import get_args
    import os
    import numpy as np
    import zarr
    import mrcfile
    import shutil
    from scipy.ndimage import zoom
    import subprocess
    import tempfile
    from tomotwin.modules.inference.embedor import TorchEmbedor

    def compute_embeddings(crop, model_path, output_path):
        """Computes embeddings for the cropped MRC data using the TomoTwin model with padding for edges."""
        unique_id = str(uuid.uuid4())
        temp_cropped_mrc_path = os.path.join(tempfile.gettempdir(), f"temp_cropped_{unique_id}.mrc")
        with mrcfile.new(temp_cropped_mrc_path, overwrite=True) as mrc:
            mrc.set_data(crop)

        embedding_path = os.path.join(output_path, "embeddings")
        os.makedirs(embedding_path, exist_ok=True)

        subprocess.run(f"CUDA_VISIBLE_DEVICES=0,1 tomotwin_embed.py tomogram -m {model_path} -v {temp_cropped_mrc_path} -b 256 -o {embedding_path} -s 1", shell=True, check=True)

        # Placeholder: Process and load the embeddings correctly
        embeddings_file = os.path.join(embedding_path, "embedding_result.npy")
        return np.load(embeddings_file)

    args = get_args()
    mrc_path = args.mrcfile
    zarr_path = args.zarr_path
    crop_coords = [args.z_start, args.z_end, args.y_start, args.y_end, args.x_start, args.x_end]

    model_path = os.path.join(get_data_path(), "tomotwin_latest.pth")

    with mrcfile.open(mrc_path, permissive=True) as mrc:
        crop = mrc.data[crop_coords[0]:crop_coords[1], crop_coords[2]:crop_coords[3], crop_coords[4]:crop_coords[5]]

    embeddings = compute_embeddings(crop, model_path, os.path.dirname(zarr_path))

    zarr_dir = os.path.dirname(zarr_path)
    if not os.path.exists(zarr_dir):
        os.makedirs(zarr_dir, exist_ok=True)

    zarr_file = zarr.open(zarr_path, mode='a')
    zarr_file.create_group('crop', overwrite=True)
    zarr_file['crop/original_data'] = crop
    zarr_file.create_group('features', overwrite=True)
    zarr_file['features/tomotwin'] = embeddings

    print("Data processing completed and saved to Zarr.")

setup(
    group="cryocanvas",
    name="create-cryocanvas-crop",
    version="0.0.1",
    title="Compute TomoTwin Embedding and Store with Cropped MRC in Zarr",
    description="Computes TomoTwin embeddings for a specified crop of MRC data with edge padding and stores both the cropped data and embeddings in a Zarr file.",
    solution_creators=["Kyle Harrington"],
    tags=["data processing", "crop", "tomotwin", "embedding", "Zarr", "Python"],
    license="MIT",
    album_api_version="0.5.1",
    args=[
        {"name": "mrcfile", "type": "file", "required": True, "description": "Path to the MRC file"},
        {"name": "zarr_path", "type": "string", "required": True, "description": "Path for the output Zarr file"},
        {"name": "z_start", "type": "integer", "required": True, "description": "Start coordinate in Z dimension"},
        {"name": "z_end", "type": "integer", "required": True, "description": "End coordinate in Z dimension"},
        {"name": "y_start", "type": "integer", "required": True, "description": "Start coordinate in Y dimension"},
        {"name": "y_end", "type": "integer", "required": True, "description": "End coordinate in Y dimension"},
        {"name": "x_start", "type": "integer", "required": True, "description": "Start coordinate in X dimension"},
        {"name": "x_end", "type": "integer", "required": True, "description": "End coordinate in X dimension"}
    ],    
    run=run,
    install=install,
    dependencies={
        "parent": {
            "group": "tomotwin",
            "name": "generate-embedding",
            "version": "0.0.9",
        }
    },        
)
