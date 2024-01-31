###album catalog: cold-storage


from album.runner.api import setup, get_args

def run():
    import os
    import zarr
    import numpy as np
    import mrcfile
    from skimage.feature import multiscale_basic_features
    
    args = get_args()

    mrc_file = args.mrcfile
    zarr_path = args.zarr_path
    group_name = args.group_name

    # Load the MRC file
    with mrcfile.open(mrc_file, permissive=True) as mrc:
        data = mrc.data

    # Compute features using multiscale_basic_features
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

    # Check if the Zarr file exists and open it, otherwise create a new Zarr file
    if os.path.exists(zarr_path):
        zarr_file = zarr.open(zarr_path, mode='a')
    else:
        zarr_file = zarr.open(zarr_path, mode='w')

    # Save the features to a Zarr group
    zarr_file.create_group(group_name, overwrite=True)
    zarr_file[group_name][:] = features

    print(f"Feature group '{group_name}' saved to Zarr file: {zarr_path}")

setup(
    group="kyleharrington",
    name="skimage-features-mrc",
    version="0.0.1",
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
