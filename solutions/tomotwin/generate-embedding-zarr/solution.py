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

    import mrcfile
    import shutil
    from scipy.ndimage import zoom
    from tomotwin.modules.inference.embedor import TorchEmbedorDistributed, Embedor, TorchEmbedor
    from tomotwin.modules.inference.argparse_embed_ui import EmbedConfiguration
    from tomotwin.embed_main import make_embeddor, sliding_window_embedding
    from tomotwin.modules.inference.boxer import Boxer, SlidingWindowBoxer

    def is_s3_path(path):
        return str(path).startswith("s3://")

    def open_zarr_store(path):
        if is_s3_path(path):
            fs = s3fs.S3FileSystem(anon=True)
            return zarr.open(s3fs.S3Map(path, s3=fs), mode='r')
        else:
            return zarr.open(path, mode='r')
    
    def embed_and_write_to_zarr(input_zarr_path: str, output_zarr_path: str, conf: EmbedConfiguration, window_size: int, slices: tuple, mask: np.array = None):
        """
        Embeds a specified slice of a tomogram stored in a Zarr array and writes the embeddings into a Zarr array in image space.
        Extends the input slice based on the window size for embedding and handles bounds checking.

        :param input_zarr_path: Path to the input Zarr array containing the tomogram.
        :param output_zarr_path: Path to the output Zarr array to write embeddings.
        :param embedor: Embedor instance for generating embeddings.
        :param conf: Embedding configuration.
        :param window_size: Size of the sliding window for embedding.
        :param slices: A tuple of slice objects specifying the region to embed.
        :param mask: Optional mask array, must have the same shape as the input tomogram.
        """
        # Load the full tomogram from Zarr
        full_tomo = zarr.open_array(input_zarr_path)

        print(f"Tomogram shape: {full_tomo.shape}")
        print(f"Slices {slices}")

        # Determine the shape for the region of interest based on the provided slices
        slice_shapes = tuple(s.stop - s.start for s in slices)
        # Shape of the output embeddings array for the sliced region, adding an extra dimension for embeddings
        embedding_shape = slice_shapes + (32,)
        
        # Calculate half of the window size for boundary extension
        half_window = window_size // 2

        # Extend the slices to include additional context for the sliding window, while handling bounds
        extended_slices = tuple(
            slice(max(0, s.start - half_window), min(full_tomo.shape[dim], s.stop + half_window))
            for dim, s in enumerate(slices)
        )

        # Extract the extended slice from the tomogram
        tomo_slice_extended = full_tomo[extended_slices]

        # Apply mask if provided (mask must also be sliced accordingly)
        if mask is not None:
            mask = mask[extended_slices]  # Adjust mask to the extended slice
            assert tomo_slice_extended.shape == mask.shape, "Extended tomogram slice and mask shape need to be equal."

        # Embedding logic as before, now using the extended slice
        embedor = make_embeddor(conf, rank=None, world_size=1)  # Example setup
        embeddings = sliding_window_embedding(tomo=tomo_slice_extended, boxer=SlidingWindowBoxer(box_size=window_size, stride=conf.stride, zrange=None, mask=mask), embedor=embedor)
        if embeddings is None:
            return None  # Handle cases where no embeddings were generated

        # Adjust the embeddings to match the original requested slice (remove the context extension)
        embeddings_adjusted = embeddings[
            max(0, half_window - slices[0].start):half_window + slice_shapes[0],
            max(0, half_window - slices[1].start):half_window + slice_shapes[1],
            max(0, half_window - slices[2].start):half_window + slice_shapes[2],
            :
        ]

        assert embeddings_adjusted.shape[:-1] == slice_shapes, "Adjusted embeddings shape does not match target slice shape."

        # Write the adjusted embeddings into the output Zarr array
        output_zarr = zarr.open_array(output_zarr_path, mode='a', shape=embedding_shape, chunks=(64, 64, 64, 32), dtype=np.float32)
        output_zarr[slices] = embeddings_adjusted

        return embeddings_adjusted  # Return the adjusted embeddings
    
    model_path = os.path.join(get_data_path(), "tomotwin_latest.pth")
    zarr_input_path = get_args().zarrinput
    zarr_output_path = get_args().zarrembedding
    slices = eval(get_args().slices)

    print(f"Embedding tomogram slice from Zarr ({zarr_input_path}) to Zarr embedding ({zarr_output_path})")

    # Example function call - you need to define or adapt these functions (e.g., Embedor, EmbedConfiguration, etc.) based on your actual codebase
    conf = EmbedConfiguration(model_path, None, None, None, 2)  # Placeholder for any configuration needed
    conf.model_path = model_path
    conf.batchsize = 35
    conf.stride = [1, 1, 1]
    conf.window_size = 37

    print(f"Config: {conf}")
    
    embed_and_write_to_zarr(zarr_input_path, zarr_output_path, conf, window_size=37, slices=slices)

setup(
    group="tomotwin",
    name="generate-embedding-zarr",
    version="0.0.12",
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
