###album catalog: cold-storage

import os
import requests

from album.runner.api import setup, get_data_path


env_file = """name: tomotwin
channels:
  - nvidia
  - pytorch
  - rapidsai
  - conda-forge
  - defaults
dependencies:
  - pytorch[version='>=2.1']
  - torchvision
  - pandas[version='<2']
  - scipy
  - numpy
  - matplotlib
  - pytables
  - cuml=23.04
  - cudatoolkit=11.8
  - protobuf[version='>3.20']
  - tensorboard
  - optuna
  - mysql-connector-python
  - pip
  - bs4
  - pip:
      - tomotwin-cryoet
"""


MODEL_URL = "https://zenodo.org/records/8358240/files/tomotwin_latest.pth?download=1"
DATA_DIR_URL = "https://ftp.ebi.ac.uk/empiar/world_availability/10499/"

def download_file(url, destination):
    """Download a file from a URL to a destination path."""
    response = requests.get(url, stream=True)
    with open(destination, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
            
def install():
    data_path = get_data_path()
    # Ensure the data path exists
    if not os.path.exists(data_path):
        os.makedirs(data_path)

    # Download the model
    model_path = os.path.join(data_path, "tomotwin_latest.pth")
    if not os.path.exists(model_path):
        download_file(MODEL_URL, model_path)
    

def run():
    import json
    from cryoet_data_portal import Client, Tomogram

    model_path = os.path.join(get_data_path(), "tomotwin_latest.pth")
    input_mrc = os.path.join(get_data_path(), "output.mrc")
    rescaled_mrc = os.path.join(get_data_path(), "rescaled.mrc")

    # Instantiate a client, using the data portal GraphQL API by default
    client = Client()

    # Find all tomograms related to a specific organism
    tomos = Tomogram.find(
        client,
        [
            Tomogram.tomogram_voxel_spacing.run.dataset.organism_name
            == "Schizosaccharomyces pombe"
        ],
    )
    tomo = list(tomos)[0]

    # Access any useful metadata for each tomogram
    print(tomo.name)

    # Print the tomogram metadata as a json string
    print(json.dumps(tomo.to_dict(), indent=4))

    # Download a 25% size preview image (uncomment to actually download files)
    tomo.download_mrcfile(binning=4, dest_path=input_mrc)
    
    # Assuming the `e2proc3d.py` and other tools are available in PATH
    print("Downscale tomogram")
    os.system(f"e2proc3d.py --apix=5.9359 --fouriershrink=1.684 {input_mrc} {rescaled_mrc}")
    print("Embedding tomogram")
    
    os.system(f"CUDA_VISIBLE_DEVICES=0,1 tomotwin_embed.py tomogram -m {model_path} -v {rescaled_mrc} -b 256 -o out/embed/tomo/ -s 2")
    print("Estimate UMAP manifold and generate embedding mask")
    os.system("tomotwin_tools.py umap -i out/embed/tomo/tomo_embeddings.temb -o out/clustering/")

setup(
    group="tomotwin",
    name="czii-cryoet-demo",
    version="0.0.1",
    title="TomoTwin demo on cz cryoet data portal",
    description="TomoTwin on an example from the czii cryoet dataportal.",
    solution_creators=["Kyle Harrington"],
    cite=[{"text": "Rice, G., Wagner, T., Stabrin, M. et al. TomoTwin: generalized 3D localization of macromolecules in cryo-electron tomograms with structural data mining. Nat Methods (2023). https://doi.org/10.1038/s41592-023-01878-z.", "url": "https://tomotwin-cryoet.readthedocs.io/en/stable/index.html"}],
    tags=["imaging", "cryoet", "Python", "particle picking", "machine learning"],
    license="MIT",
    covers=[],
    album_api_version="0.5.1",
    args=[],
    run=run,
    install=install,
    dependencies={"environment_file": env_file},
)

