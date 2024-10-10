###album catalog: cold-storage

from album.runner.api import setup, get_args

env_file = """channels:
  - conda-forge
dependencies:
  - python=3.10
  - pandas
  - requests
"""

def run():
    # Imports inside the run function
    import os
    import urllib.request
    import pandas as pd

    # Download cath-names.txt and PDB files based on CATH IDs
    def download_cath_names_and_pdbs(target_dir):
        """Download cath-names.txt and PDB files based on CATH IDs."""
        # Create target directory if necessary
        os.makedirs(target_dir, exist_ok=True)

        # Fetch the CATH names list
        CATH_URL = "http://download.cathdb.info/cath/releases/latest-release/cath-classification-data/cath-names.txt"
        cath_list_path = os.path.join(target_dir, "cath-names.txt")
        urllib.request.urlretrieve(CATH_URL, cath_list_path)

        # Parse the cath-names list
        df = pd.read_csv(cath_list_path, comment='#', sep='\s+', header=None, usecols=[1], names=['pdb_id'])
        df['pdb_id'] = df['pdb_id'].str[:4]  # Extract the PDB ID

        # Download PDB files
        base_url = "https://files.rcsb.org/download/"
        for pdb_id in df['pdb_id']:
            pdb_url = f"{base_url}{pdb_id}.pdb"
            output_path = os.path.join(target_dir, f"{pdb_id}.pdb")
            try:
                urllib.request.urlretrieve(pdb_url, output_path)
                print(f"Downloaded {pdb_id} to {target_dir}")
            except Exception as e:
                print(f"Failed to download {pdb_id}: {e}")

    # Get arguments from album
    args = get_args()
    target_dir = args.target_dir
    download_cath_names_and_pdbs(target_dir)

setup(
    group="cathdb",
    name="download-pdbs",
    version="0.0.1",
    title="CATH Names and PDB Downloader",
    description="Downloads CATH names and corresponding PDB files into the specified directory.",
    solution_creators=["Kyle Harrington"],
    tags=["bioinformatics", "CATH", "PDB", "protein structures", "data download"],
    license="MIT",
    album_api_version="0.5.1",
    args=[
        {
            "name": "target_dir",
            "type": "string",
            "description": "Directory to save the CATH names and downloaded PDB files",
            "required": True,
        }
    ],
    run=run,
    dependencies={"environment_file": env_file},
)
