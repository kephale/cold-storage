###album catalog: cold-storage


from album.runner.api import setup


def run():
    from album.runner.api import get_args
    import os
    import numpy as np
    import pandas as pd
    import zarr
    import mrcfile
    from skimage.feature import multiscale_basic_features
    from numba import njit, prange

    @njit(parallel=True)
    def process_embedding_vectors(partition_df, crop_coords, vector_size, max_shape):
        subarray = np.zeros(max_shape, dtype=np.float32)  # Use maximal array size
        for i in prange(len(partition_df)):
            row = partition_df[i]
            z, y, x = int(row[0]) - crop_coords[0], int(row[1]) - crop_coords[2], int(row[2]) - crop_coords[4]
            embedding_vector = row[3:]  # Assuming the first three columns are Z, Y, X and the rest are embedding vector
            subarray[z, y, x, :] = embedding_vector
        return subarray

    def process_chunk(data_chunk, sigma_max):
        overlap = int(sigma_max * 3)
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
        return chunk_features[overlap:-overlap, overlap:-overlap, overlap:-overlap]

    args = get_args()

    mrc_path = args.mrcfile
    embeddings_path = args.embeddingfile
    zarr_path = args.zarr_path
    crop_coords = [args.z_start, args.z_end, args.y_start, args.y_end, args.x_start, args.x_end]
    crop_coords_array = np.array([args.z_start, args.z_end, args.y_start, args.y_end, args.x_start, args.x_end], dtype=np.int64)

    # Read and crop the MRC data
    with mrcfile.open(mrc_path, permissive=True) as mrc:
        crop = mrc.data[crop_coords[0]:crop_coords[1], crop_coords[2]:crop_coords[3], crop_coords[4]:crop_coords[5]]

    # Read and filter the embedding DataFrame
    embedding_df = pd.read_pickle(embeddings_path)
    cropped_embedding_df = embedding_df[(embedding_df['Z'] >= crop_coords[0]) & (embedding_df['Z'] < crop_coords[1]) &
                                        (embedding_df['Y'] >= crop_coords[2]) & (embedding_df['Y'] < crop_coords[3]) &
                                        (embedding_df['X'] >= crop_coords[4]) & (embedding_df['X'] < crop_coords[5])]

    # Determine the size of the embedding vector
    vector_size = cropped_embedding_df.shape[1] - 3
    max_shape = (crop_coords[1] - crop_coords[0], crop_coords[3] - crop_coords[2], crop_coords[5] - crop_coords[4], vector_size)
    
    # Partition the DataFrame for parallel processing
    partitioned_dfs = np.array_split(cropped_embedding_df, 24)

    # Convert DataFrame to NumPy array for numba processing
    cropped_embedding_np = cropped_embedding_df.to_numpy()

    # Determine the size of the embedding vector and the maximal shape
    vector_size = cropped_embedding_np.shape[1] - 3  # Adjust based on your DataFrame's structure
    max_shape = (crop_coords[1] - crop_coords[0], crop_coords[3] - crop_coords[2], crop_coords[5] - crop_coords[4], vector_size)

    # Directly call the numba-optimized function without multiprocessing
    final_embedding_array = process_embedding_vectors(cropped_embedding_np, crop_coords, vector_size, max_shape)

    # Compute skimage features for the crop
    sigma_max = 16
    features = process_chunk(crop, sigma_max=sigma_max)

    # Ensure the directory for the Zarr file exists
    zarr_dir = os.path.dirname(zarr_path)
    if not os.path.exists(zarr_dir):
        os.makedirs(zarr_dir, exist_ok=True)

    # Write outputs to Zarr
    zarr_file = zarr.open(zarr_path, mode='a')
    zarr_file.create_group('crop', overwrite=True)
    zarr_file['crop/original_data'] = crop
    zarr_file.create_group('features', overwrite=True)
    zarr_file['features/tomotwin'] = final_embedding_array    
    zarr_file['features/skimage'] = features

    print("Data processing completed and saved to Zarr.")


setup(
    group="cryocanvas",
    name="generate-sample-crop",
    version="0.0.9",
    title="Process Cropped Data with skimage Features",
    description="Processes a crop of the input MRC data and embeddings, computes skimage features, and writes to Zarr.",
    solution_creators=["Kyle Harrington"],
    tags=["data processing", "crop", "skimage", "features", "Zarr", "Python"],
    license="MIT",
    album_api_version="0.5.1",
    args=[
        {"name": "mrcfile", "type": "file", "required": True, "description": "Path to the MRC file"},
        {"name": "embeddingfile", "type": "file", "required": True, "description": "Path to the embedding DataFrame file"},
        {"name": "zarr_path", "type": "string", "required": True, "description": "Path for the output Zarr file"},
        {"name": "z_start", "type": "integer", "required": True, "description": "Start coordinate in Z dimension"},
        {"name": "z_end", "type": "integer", "required": True, "description": "End coordinate in Z dimension"},
        {"name": "y_start", "type": "integer", "required": True, "description": "Start coordinate in Y dimension"},
        {"name": "y_end", "type": "integer", "required": True, "description": "End coordinate in Y dimension"},
        {"name": "x_start", "type": "integer", "required": True, "description": "Start coordinate in X dimension"},
        {"name": "x_end", "type": "integer", "required": True, "description": "End coordinate in X dimension"}
    ],
    run=run,
    dependencies={
        "parent": {
            "group": "kyleharrington",
            "name": "headless-parent",
            "version": "0.0.4",
        }        
    },        
)
