from album.runner.api import setup, get_args

###album catalog: cold-storage

env_file = """channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.9
  - requests
"""

def download_pdbs(pdb_ids, output_dir):
    import requests
    import os

    base_url = "https://files.rcsb.org/download/"
    for pdb_id in pdb_ids:
        pdb_url = f"{base_url}{pdb_id}.pdb"
        response = requests.get(pdb_url)
        if response.status_code == 200:
            output_path = os.path.join(output_dir, f"{pdb_id}.pdb")
            with open(output_path, "wb") as file:
                file.write(response.content)
            print(f"Downloaded {pdb_id} to {output_dir}")
        else:
            print(f"Failed to download {pdb_id}: HTTP Status Code {response.status_code}")


def run():
    import os
    
    args = get_args()
    pdb_list = args.pdbs.split(",")
    output_dir = args.output_dir if args.output_dir else os.getcwd()
    download_pdbs(pdb_list, output_dir)


# Set up the Album catalog entry
setup(
    group="kyleharrington",
    name="download-pdbs",
    version="0.0.3",
    title="PDB File Downloader",
    description="A utility to download PDB files from a list of PDB IDs.",
    solution_creators=["Your Name"],
    tags=["bioinformatics", "PDB", "protein structures", "data download"],
    license="MIT",
    album_api_version="0.5.1",
    args=[
        {
            "name": "pdbs",
            "type": "string",
            "description": "Comma-separated list of PDB IDs to download",
        },
        {
            "name": "output_dir",
            "type": "string",
            "description": "Optional: Directory to save the downloaded PDB files (default is current directory)",
            "default": "",
            "required": False,
        }
    ],
    run=run,
    dependencies={"environment_file": env_file},    
)
