###album catalog: cold-storage

from album.runner.api import setup



def run():
    """Run the album solution with partitioned processing."""
    import os
    import pandas as pd
    import numpy as np
    import zarr
    import mrcfile
    from concurrent.futures import ThreadPoolExecutor, as_completed
    from album.runner.api import get_args
    
    args = get_args()

    # Paths to input files and number of workers
    mrc_path = args.mrcfile
    embeddings_path = args.embeddingfile
    zarr_path = args.zarr_path
    zarr_group = args.zarr_group
    num_workers = args.num_workers  # Get the number of workers

    print("Reading input files")
    mrc_data = mrcfile.mmap(mrc_path, permissive=True).data
    embedding_df = pd.read_pickle(embeddings_path)

    print(f"MRC data shape: {mrc_data.shape}")
    print(f"Embedding DataFrame shape: {embedding_df.shape}")

    # Ensure the directory for the Zarr file exists
    zarr_dir = os.path.dirname(zarr_path)
    if not os.path.exists(zarr_dir):
        os.makedirs(zarr_dir, exist_ok=True)

    # Determine the number of features in the DataFrame (excluding X, Y, Z)
    embedding_dims = embedding_df.shape[1] - 3

    zarr_file = zarr.open(zarr_path, mode='a')
    group = zarr_file.require_group(zarr_group)

    # Handling datasets creation or replacement in Zarr group
    mrc_dataset_name = 'data'
    if mrc_dataset_name in group:
        print(f"Dataset '{mrc_dataset_name}' already existed, replacing.")
        del group[mrc_dataset_name]
    mrc_dataset = group.create_dataset(mrc_dataset_name, shape=mrc_data.shape, chunks=(10, 200, 200), dtype=mrc_data.dtype)
    mrc_dataset[:] = mrc_data

    embedding_dataset_name = zarr_group
    if embedding_dataset_name in group:
        print(f"Dataset '{embedding_dataset_name}' already existed, replacing.")
        del group[embedding_dataset_name]
    embedding_dataset = group.create_dataset(embedding_dataset_name,
                                             shape=(mrc_data.shape[0], mrc_data.shape[1], mrc_data.shape[2], embedding_dims),
                                             chunks=(10, 200, 200, embedding_dims),
                                             dtype='float32')

    # Partitioning DataFrame for parallel processing
    partitions = np.array_split(embedding_df, num_workers)

    def process_partition(partition, batch_size=1000):
        """Process a partition of the DataFrame and batch write to Zarr dataset."""
        buffer = []  # Initialize buffer to hold batch data
        for index, row in partition.iterrows():
            z, y, x = int(row['Z']), int(row['Y']), int(row['X'])
            values = row.values[3:]
            if z < mrc_data.shape[0] and y < mrc_data.shape[1] and x < mrc_data.shape[2]:
                buffer.append(((z, y, x), values))
                if len(buffer) >= batch_size:
                    write_batch(buffer)  # Write batch to Zarr and reset buffer
                    buffer = []
        if buffer:  # Check if there's any data left in the buffer
            write_batch(buffer)

    def write_batch(buffer):
        """Write a batch of updates to the Zarr dataset."""
        for (z, y, x), values in buffer:
            embedding_dataset[z, y, x, :] = values

    # Create a ThreadPoolExecutor to manage concurrency
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        # Submit each partition to the executor
        futures = [executor.submit(process_partition, partition) for partition in partitions]

        # Wait for all submitted tasks to complete
        for future in as_completed(futures):
            try:
                future.result()  # Handle results or exceptions here
            except Exception as exc:
                print(f"Generated an exception: {exc}")

    print(f"Data and embeddings have been successfully saved to Zarr group '{zarr_group}' in file '{zarr_path}'")




setup(
    group="cryocanvas",
    name="embedding_df_to_zarr",
    version="0.0.9",
    title="Convert a TomoTwin embedding DataFrame to Zarr Format",
    description="Converts a given DataFrame to a Zarr file format.",
    solution_creators=["Kyle Harrington"],
    tags=["data conversion", "DataFrame", "Zarr", "Python"],
    license="MIT",
    covers=[{
        "description": "Cover image.",
        "source": "cover.png"
    }],
    album_api_version="0.5.1",
    args=[
        {"name": "mrcfile", "type": "file", "required": True, "description": "Path to the MRC file"},
        {"name": "embeddingfile", "type": "file", "required": True, "description": "Path to the embedding DataFrame file"},
        {"name": "num_workers", "type": "integer", "required": True, "description": "Number of workers for processing the dataframe", "default": 1},
        {"name": "zarr_path", "type": "string", "required": True, "description": "Path for the Zarr file"},
        {"name": "zarr_group", "type": "string", "required": True, "description": "Name of the group in the Zarr file to store the data"}
    ],
    run=run,
    dependencies={
        "parent": {
            "group": "kyleharrington",
            "name": "headless-parent",
            "version": "0.0.5",
        }
    },
)
