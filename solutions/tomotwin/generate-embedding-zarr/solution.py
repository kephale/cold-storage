###album catalog: cold-storage

from album.runner.api import setup, get_data_path, get_args

env_file = """name: tomotwin
channels:
  - nvidia
  - pytorch
  - rapidsai
  - conda-forge
  - defaults
dependencies:
  - python=3.10
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
  - zarr
  - s3fs
  - aiobotocore
  - botocore
  - pip:
      - tomotwin-cryoet
      - cryoet-data-portal
      - mrcfile
"""

MODEL_URL = "https://zenodo.org/records/8358240/files/tomotwin_latest.pth?download=1"

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
    # Ensure the data path exists
    if not os.path.exists(data_path):
        os.makedirs(data_path)

    # Download the model
    model_path = os.path.join(data_path, "tomotwin_latest.pth")
    if not os.path.exists(model_path):
        download_file(MODEL_URL, model_path)

def run():    
    import os
    import requests
    import numpy as np
    import zarr
    import s3fs
    import math

    import mrcfile
    import shutil
    from scipy.ndimage import zoom
    from tomotwin.modules.inference.embedor import TorchEmbedorDistributed, Embedor, TorchEmbedor
    from tomotwin.modules.inference.argparse_embed_ui import EmbedConfiguration
    from tomotwin.embed_main import make_embeddor
    from tomotwin.modules.inference.boxer import Boxer, SlidingWindowBoxer

    def is_s3_path(path):
        return str(path).startswith("s3://")

    def open_zarr_store(path):
        if is_s3_path(path):
            fs = s3fs.S3FileSystem(anon=True)
            return zarr.open(s3fs.S3Map(path, s3=fs), mode='r')
        else:
            return zarr.open(path, mode='r')

    def sliding_window_embedding(tomo: np.array, boxer: Boxer, embedor: Embedor) -> np.array:
        '''
        Embeds the tomogram using a sliding window approach, placing embeddings in an array based on their positions.

        :param tomo: Tomogram as a numpy array.
        :param boxer: Box provider that generates positions for embedding.
        :param embedor: Embedor to embed the boxes extracted from the tomogram.
        :return: A numpy array with embeddings placed according to their positions.
        '''
        boxes = boxer.box(tomogram=tomo)
        embeddings = embedor.embed(volume_data=boxes)
        if embeddings is None:
            return None

        # Assuming the shape of tomo is Z, Y, X and embeddings are in Z, Y, X, Embed_dim
        # Initialize an empty array for the embeddings with an additional dimension for the embedding vector
        embedding_array = np.zeros(tomo.shape + (embeddings.shape[-1],), dtype=embeddings.dtype)

        for i in range(embeddings.shape[0]):
            pos_z, pos_y, pos_x = boxes.get_localization(i).astype(int)
            embedding_array[pos_z, pos_y, pos_x, :] = embeddings[i]

        return embedding_array        
    
    def embed_and_write_to_zarr(input_zarr_path, output_zarr_path, conf, window_size, slices):
        full_tomo = zarr.open_array(input_zarr_path, mode='r')
        output_zarr = zarr.open(output_zarr_path, mode='a', shape=full_tomo.shape + (32,), chunks=(64, 64, 64, 32), dtype=np.float32)

        # Calculate the extended slices to include boundary data for the 37x37x37 box
        boundary_size = math.ceil(window_size / 2) - 1
        extended_slices = (
            slice(max(0, slices[0].start - boundary_size), min(full_tomo.shape[0], slices[0].stop + boundary_size)),
            slice(max(0, slices[1].start - boundary_size), min(full_tomo.shape[1], slices[1].stop + boundary_size)),
            slice(max(0, slices[2].start - boundary_size), min(full_tomo.shape[2], slices[2].stop + boundary_size))
        )

        tomo_slice_extended = full_tomo[extended_slices]

        embedor = make_embeddor(conf, rank=None, world_size=1)
        embedding_array = sliding_window_embedding(tomo_slice_extended, boxer=SlidingWindowBoxer(box_size=window_size, stride=conf.stride), embedor=embedor)

        if embedding_array is None:
            return None

        # Calculate the starting indices for trimming the extended embedding_array to fit back into the original slice dimensions
        trim_start_z = slices[0].start - extended_slices[0].start
        trim_start_y = slices[1].start - extended_slices[1].start
        trim_start_x = slices[2].start - extended_slices[2].start

        # Calculate the ending indices for trimming
        trim_end_z = trim_start_z + (slices[0].stop - slices[0].start)
        trim_end_y = trim_start_y + (slices[1].stop - slices[1].start)
        trim_end_x = trim_start_x + (slices[2].stop - slices[2].start)

        # Trim the embedding_array to match the original slice dimensions
        trimmed_embedding_array = embedding_array[
            trim_start_z:trim_end_z,
            trim_start_y:trim_end_y,
            trim_start_x:trim_end_x,
            :
        ]

        output_zarr[slices] = trimmed_embedding_array

        print("Embedding written to Zarr.")
    
    model_path = os.path.join(get_data_path(), "tomotwin_latest.pth")
    zarr_input_path = get_args().zarrinput
    zarr_output_path = get_args().zarrembedding
    slices = eval(get_args().slices)

    print(f"Embedding tomogram slice from Zarr ({zarr_input_path}) to Zarr embedding ({zarr_output_path})")

    # Setup embedding configuration
    conf = EmbedConfiguration(model_path, None, None, None, 2)
    conf.model_path = model_path
    conf.batchsize = 35
    conf.stride = [1, 1, 1]
    conf.window_size = 37

    print(f"Config: {conf}")
    
    embed_and_write_to_zarr(zarr_input_path, zarr_output_path, conf, window_size=37, slices=slices)

setup(
    group="tomotwin",
    name="generate-embedding-zarr",
    version="0.0.15",
    title="Generate an embedding with TomoTwin for a Zarr file",
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
        {"name": "zarrinput", "type": "string", "required": True, "description": "Path to the input Zarr file"},
        {"name": "zarrembedding", "type": "string", "required": True, "description": "Path for the output Zarr embedding file"},
        {"name": "slices", "type": "string", "required": True, "description": "Slices for the region of interest, specified as a string, e.g. (slice(0,100), slice(0,100), slice(0,100))"},
    ],
    run=run,
    install=install,
    dependencies={"environment_file": env_file},
)
