###album catalog: cold-storage

from album.runner.api import setup


def run():
    from cryoet_data_portal import Client, Run
    from album.runner.api import get_args

    output_directory = get_args().output_directory
    dataset_id = get_args().dataset_id
    run_id = get_args().run_id
    
    # Instantiate a client, using the data portal GraphQL API by default
    client = Client()
    
    runs = Run.find(client, query_filters=[Run.name == run_id, Run.dataset.id == dataset_id])
    run = list(runs)[0]
    
    run.download_everything(output_directory)

    
setup(
    group="cryoetdataportal",
    name="download-mrc",
    version="0.0.1",
    title="Download a MRC from the CZ CryoET Data Portal",
    description="Download a MRC from the CZ CryoET Data Portal.",
    solution_creators=["Kyle Harrington"],
    tags=["cryoet", "data", "download"],
    license="MIT",
    covers=[{"description": "Cover image description", "source": "cover.png"}],
    album_api_version="0.5.1",
    args=[
        {"name": "dataset_id", "type": "integer", "required": True, "description": "Dataset ID for the MRC file"},
        {"name": "run_id", "type": "string", "required": True, "description": "Run ID for the MRC file"},
        {"name": "output_directory", "type": "file", "required": True, "description": "Directory for saving the output"}
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
