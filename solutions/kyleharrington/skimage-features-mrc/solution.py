###album catalog: cold-storage


from album.runner.api import setup

def run():
    import os
    import zarr
    import mrcfile
    import numpy as np
    from skimage.feature import multiscale_basic_features
    from album.runner.api import get_args

    def process_chunk(data_chunk, sigma_max):
        overlap = int(sigma_max * 3)  # Define overlap based on the largest sigma
        padded_chunk = np.pad(data_chunk, ((overlap, overlap), (overlap, overlap), (overlap, overlap)), mode='reflect')
        chunk_features = multiscale_basic_features(
            image=padded_chunk,
            intensity=True,
            edges=True,
            texture=True,
            sigma_min=0.5,
            sigma_max=sigma_max,
            num_sigma=10,
            channel_axis=None
        )
        # Discard the overlap
        return chunk_features[overlap:-overlap, overlap:-overlap, overlap:-overlap]

    args = get_args()

    mrc_file = args.mrcfile
    zarr_path = args.zarr_path
    group_name = args.group_name
    sigma_max = 16  # Adjust sigma_max as needed

    try:
        # Ensure directory for Zarr file exists
        zarr_dir = os.path.dirname(zarr_path)
        os.makedirs(zarr_dir, exist_ok=True)

        # Load MRC file
        with mrcfile.open(mrc_file, permissive=True) as mrc:
            data = mrc.data

        # Open or create Zarr file
        zarr_file = zarr.open(zarr_path, mode='a')
        group = zarr_file.require_group(group_name)

        # Define the dataset shape and data type
        features_shape = (data.shape[0], data.shape[1], data.shape[2])  # Adjust as needed
        features_dtype = np.float32  # Adjust as needed

        # Create or append to the dataset
        if group_name in group.array_keys():
            features_dataset = group[group_name]
        else:
            features_dataset = group.create_dataset(group_name, shape=features_shape, chunks=True, dtype=features_dtype)

        # Chunk-wise processing
        chunk_size = 100  # Adjust based on memory capacity
        for start in range(0, data.shape[0], chunk_size):
            end = min(start + chunk_size, data.shape[0])
            chunk = data[start:end]
            chunk_features = process_chunk(chunk, sigma_max)
            features_dataset[start:end] = chunk_features

        print(f"Feature data saved in group '{group_name}' in Zarr file: {zarr_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


setup(
    group="kyleharrington",
    name="skimage-features-mrc",
    version="0.0.5",
    title="Compute basic fixed features for CryoET Data",
    description="Computes a feature group for cryoET data using skimage.feature.multiscale_basic_features and saves to a Zarr file.",
    solution_creators=["Kyle Harrington"],
    tags=["cryoet", "features", "zarr", "Python"],
    license="MIT",
    covers=[{"description": "Cover image description", "source": "cover.png"}],
    album_api_version="0.5.1",
    args=[
        {"name": "mrcfile", "type": "file", "required": True, "description": "Path to the MRC file"},
        {"name": "zarr_path", "type": "string", "required": True, "description": "Path for the Zarr file"},
        {"name": "group_name", "type": "string", "required": True, "description": "Name of the group in the Zarr file to store the features"}
    ],
    run=run,
    dependencies={
        "parent": {
            "group": "kyleharrington",
            "name": "headless-parent",
            "version": "0.0.2",
        }        
    },    
)
