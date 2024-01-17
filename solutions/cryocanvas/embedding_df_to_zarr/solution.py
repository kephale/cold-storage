###album catalog: cold-storage

from album.runner.api import setup

def run():
    """Run the album solution."""

    import pandas as pd
    import zarr
    import mrcfile
    from album.runner.api import get_args
    
    # Paths to input files
    mrc_path = get_args().mrcfile
    embeddings_path = get_args().embeddingfile

    # Read the MRC file and DataFrame
    mrc_data = mrcfile.mmap(mrc_path, permissive=True).data
    embedding_df = pd.read_pickle(embeddings_path)

    # Determine the number of features in the DataFrame (excluding X, Y, Z)
    embedding_dims = embedding_df.shape[1] - 3

    # Path for the output Zarr file
    output_path = get_args().zarr_output

    # Create Zarr file
    zarr_file = zarr.open(output_path, mode='w')

    # Create datasets in Zarr file
    zarr_file.create_dataset('mrc_data', data=mrc_data, chunks=(10, 200, 200))
    embedding_dataset = zarr_file.create_dataset('embedding', 
                                                 shape=(mrc_data.shape[0], mrc_data.shape[1], mrc_data.shape[2], embedding_dims),
                                                 chunks=(10, 200, 200, embedding_dims),
                                                 dtype='float32')

    # Populate the embedding dataset
    for index, row in embedding_df.iterrows():
        z, y, x = int(row['Z']), int(row['Y']), int(row['X'])
        embedding_dataset[z, y, x, :] = row.values[3:]

    print(f"Data and embeddings have been successfully saved to {output_path}")


setup(
    group="cryocanvas",
    name="embedding_df_to_zarr",
    version="0.0.1",
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
        {"name": "dataframe", "type": "file", "required": True, "description": "Path to the DataFrame file"},
        {"name": "zarr_output", "type": "file", "required": True, "description": "Path for the output Zarr file"}
    ],
    run=run,
    dependencies={
        "parent": {
            "group": "kyleharrington",
            "name": "headless-parent",
            "version": "0.0.1",
        }
    },
)
