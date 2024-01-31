###album catalog: cold-storage

from album.runner.api import setup


def run():
    import mrcfile
    from album.runner.api import get_args

    args = get_args()
    input_mrc_path = args.input_mrc
    output_mrc_path = args.output_mrc
    start_z = args.start_z
    end_z = args.end_z

    # Open the input MRC file
    with mrcfile.open(input_mrc_path, permissive=True) as mrc:
        data = mrc.data
        # Crop the data along the Z-axis
        cropped_data = data[start_z:end_z]

        # Create a new MRC file for the cropped data
        with mrcfile.new(output_mrc_path, overwrite=True) as new_mrc:
            new_mrc.set_data(cropped_data)

            # Copy metadata from the original MRC file
            new_mrc.voxel_size = mrc.voxel_size
            new_mrc.header = mrc.header
            new_mrc.extended_header = mrc.extended_header

    print(f"Cropped MRC file saved to {output_mrc_path}")


    
setup(
    group="cryoetdataportal",
    name="crop-mrc",
    version="0.0.1",
    title="Crop a MRC from the CZ CryoET Data Portal",
    description="Crop a MRC from the CZ CryoET Data Portal.",
    solution_creators=["Kyle Harrington"],
    tags=["cryoet", "data", "crop"],
    license="MIT",
    covers=[{"description": "Cover image description", "source": "cover.png"}],
    album_api_version="0.5.1",
    args=[        
        {"name": "input_mrc", "type": "file", "required": True, "description": "Input mrc file"},
        {"name": "output_mrc", "type": "file", "required": True, "description": "Output mrc file"},
        {"name": "start_z", "type": "integer", "required": True, "description": "Start Z for cropping"},
        {"name": "end_z", "type": "integer", "required": True, "description": "End Z for cropping"},
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
