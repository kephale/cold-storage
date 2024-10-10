###album catalog: cold-storage

from album.runner.api import setup

def download_and_prepare_dataset(client, crop_coords):
    import appdirs

    import os
    import zarr
    import json
    from urllib.parse import urlparse, unquote

    from cryoet_data_portal import Client, Tomogram, Annotation

    from ome_zarr.io import parse_url
    from ome_zarr.reader import Reader

    import numpy as np
    
    # Select the first tomogram
    tomos = Tomogram.find(client, [Tomogram.tomogram_voxel_spacing.run.dataset.organism_name == "Schizosaccharomyces pombe"])
    tomos = list(tomos)
    first_tomo = tomos[0] if tomos else None

    if not first_tomo:
        raise ValueError("No tomograms found for the specified criteria")

    # Download and prepare the Zarr file
    zarr_path = first_tomo.to_dict()["https_omezarr_dir"]
    reader = Reader(parse_url(zarr_path))
    nodes = list(reader())
    multiscale_img = nodes[0].data

   
    # Use the provided cropping coordinates
    cropped_img = multiscale_img[0][crop_coords[0]:crop_coords[1], crop_coords[2]:crop_coords[3], crop_coords[4]:crop_coords[5]]

    # Save the cropped image into a new Zarr file in the appdirs path
    appdir_path = appdirs.user_data_dir("cryocanvas")
    if not os.path.exists(appdir_path):
        os.makedirs(appdir_path)
    demo_zarr_path = os.path.join(appdir_path, 'demo_dataset.zarr')
    demo_zarr = zarr.open(demo_zarr_path, mode='w')
    demo_zarr.create_dataset('demo_image', data=np.array(cropped_img), chunks=(10, 10, 10))

    return demo_zarr_path


def run():
    """Run the album solution."""

    from album.runner.api import get_args
    
    # Get cropping coordinates from arguments
    args = get_args()
    crop_coords = [args.crop_z_start, args.crop_z_end, args.crop_y_start, args.crop_y_end, args.crop_x_start, args.crop_x_end]
    # crop_coords = [0, 100, 0, 100, 0, 100]

    from cryoet_data_portal import Client
    # In your main function or where appropriate
    try:
        client = Client()
        demo_dataset_path = download_and_prepare_dataset(client, crop_coords)
        print(f"Demo dataset saved to {demo_dataset_path}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    

setup(
    group="cryocanvas",
    name="setup_demo",
    version="0.0.2",
    title="Setup a demo environment for CryoCanvas",
    description="Setup a demo environment for CryoCanvas using the CZ Cryo ET Data Portal.",
    solution_creators=["Kyle Harrington"],
    tags=["particle picking", "CryoET", "Python"],
    license="MIT",
    covers=[{
        "description": "Cover image.",
        "source": "cover.png"
    }],
    album_api_version="0.5.1",
    args=[
        {"name": "crop_z_start", "type": "integer", "required": True, "description": "Start coordinate for cropping on Z axis", "default": 0},
        {"name": "crop_z_end", "type": "integer", "required": True, "description": "End coordinate for cropping on Z axis", "default": 100},
        {"name": "crop_y_start", "type": "integer", "required": True, "description": "Start coordinate for cropping on Y axis", "default": 0},
        {"name": "crop_y_end", "type": "integer", "required": True, "description": "End coordinate for cropping on Y axis", "default": 100},
        {"name": "crop_x_start", "type": "integer", "required": True, "description": "Start coordinate for cropping on X axis", "default": 0},
        {"name": "crop_x_end", "type": "integer", "required": True, "description": "End coordinate for cropping on X axis", "default": 100}
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


