###album catalog: cold-storage

from album.runner.api import setup


def run():
    """Run the album solution."""

    import os
    import pandas as pd
    import zarr
    import mrcfile
    from concurrent.futures import ThreadPoolExecutor, as_completed
    from album.runner.api import get_args
    
    args = get_args()

    # Paths to input files
    mrc_path = args.mrcfile
    embeddings_path = args.embeddingfile
    zarr_path = args.zarr_path
    zarr_group = args.zarr_group

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

    print("Creating datasets in Zarr group")
    if 'data' in group:
        print("Dataset already existed, Deleting.")
        del group['data']
    mrc_dataset = group.create_dataset('data', shape=mrc_data.shape, chunks=(10, 200, 200), dtype=mrc_data.dtype)
    mrc_dataset[:] = mrc_data

    if zarr_group in group:
        print("Dataset already existed, Deleting.")
        del group[zarr_group]
    embedding_dataset = group.create_dataset(zarr_group,
                                             shape=(mrc_data.shape[0], mrc_data.shape[1], mrc_data.shape[2], embedding_dims),
                                             chunks=(10, 200, 200, embedding_dims),
                                             dtype='float32')

    def populate_embedding(z, y, x, values):
        """Function to populate embedding dataset. Ensures thread-safe write to Zarr dataset."""
        if z >= mrc_data.shape[0] or y >= mrc_data.shape[1] or x >= mrc_data.shape[2]:
            print(f"Index out of bounds: Z={z}, Y={y}, X={x}")
            return
        embedding_dataset[z, y, x, :] = values

    # Create a ThreadPoolExecutor to manage concurrency
    with ThreadPoolExecutor() as executor:
        # Submit tasks to the executor
        futures = [executor.submit(populate_embedding, int(row['Z']), int(row['Y']), int(row['X']), row.values[3:])
                   for index, row in embedding_df.iterrows()]

        # Wait for all submitted tasks to complete
        for future in as_completed(futures):
            try:
                future.result()  # You can handle results or exceptions here
            except Exception as exc:
                print(f"Generated an exception: {exc}")

    print(f"Data and embeddings have been successfully saved to Zarr group '{zarr_group}' in file '{zarr_path}'")



setup(
    group="cryocanvas",
    name="embedding_df_to_zarr",
    version="0.0.6",
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
        {"name": "zarr_path", "type": "string", "required": True, "description": "Path for the Zarr file"},
        {"name": "zarr_group", "type": "string", "required": True, "description": "Name of the group in the Zarr file to store the data"}
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
