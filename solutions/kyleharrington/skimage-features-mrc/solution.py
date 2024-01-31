###album catalog: cold-storage


from album.runner.api import setup, get_args

def run():
    import os
    import zarr
    import mrcfile
    from skimage.feature import multiscale_basic_features
    from album.runner.api import get_args
    
    args = get_args()

    mrc_file = args.mrcfile
    zarr_path = args.zarr_path
    group_name = args.group_name

    try:
        print(f"Received MRC file: {mrc_file}")
        print(f"Zarr file path: {zarr_path}")
        print(f"Group name: {group_name}")

        # Ensure the directory for the Zarr file exists
        zarr_dir = os.path.dirname(zarr_path)
        if not os.path.exists(zarr_dir):
            print(f"Creating directory: {zarr_dir}")
            os.makedirs(zarr_dir, exist_ok=True)

        # Load the MRC file
        with mrcfile.open(mrc_file, permissive=True) as mrc:
            print("MRC file opened successfully.")
            data = mrc.data

        # Compute features using multiscale_basic_features
        print("Computing features...")
        features = multiscale_basic_features(
            image=data,
            intensity=True,
            edges=True,
            texture=True,
            sigma_min=0.5,
            sigma_max=16,
            num_sigma=10,
            channel_axis=None
        )

        # Open or create the Zarr file
        print(f"Opening/Creating Zarr file at: {zarr_path}")
        zarr_file = zarr.open(zarr_path, mode='a')

        # Create or overwrite the group
        print(f"Creating/Overwriting group: {group_name}")
        group = zarr_file.require_group(group_name)

        # Create a dataset in the group for the features
        print("Creating dataset in the group...")
        dataset = group.create_dataset('features', shape=features.shape, chunks=True, dtype=features.dtype)
        dataset[:] = features

        print(f"Feature group '{group_name}' saved to Zarr file: {zarr_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


setup(
    group="kyleharrington",
    name="skimage-features-mrc",
    version="0.0.3",
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
    dependencies={
        "parent": {
            "group": "kyleharrington",
            "name": "headless-parent",
            "version": "0.0.2",
        }        
    },    
)
