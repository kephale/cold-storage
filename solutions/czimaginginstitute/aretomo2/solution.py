###album catalog: cold-storage

import os
import requests

from album.runner.api import setup, get_data_path


env_file = """name: aretomo2
channels:
  - nvidia
  - conda-forge
  - defaults
dependencies:
  - python=3.11
  - cudatoolkit=11.8
"""


def local_repository_path():
    if not os.path.exists(get_data_path()):
        os.makedirs(get_data_path())
    
    return os.path.join(get_data_path(), "git")

def download_file(url, destination):
    """Download a file from a URL to a destination path."""
    response = requests.get(url, stream=True)
    with open(destination, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
            
def install():
    import os
    import subprocess
    
    # URL for the AreTomo2 repository
    repo_url = "https://github.com/czimaginginstitute/AreTomo2.git"
    
    # Path to clone the repository
    clone_path = local_repository_path()

    # Check if the repo already exists, if not, clone it
    if not os.path.exists(os.path.join(clone_path, ".git")):
        subprocess.check_call(["git", "clone", repo_url, clone_path])

    # Change to the cloned repository directory
    os.chdir(clone_path)

    # Use subprocess to compile AreTomo2
    # Replace 'makefile11' with the appropriate makefile based on your GPU's compute capability
    subprocess.check_call(["make", "exe", "-f", "makefile11"])

def run():
    pass
    
setup(
    group="czimaginginstitute",
    name="aretomo2",
    version="0.0.1",
    title="AreTomo2: Automated Tomographic Alignment and Reconstruction",
    description="AreTomo2 is a multi-GPU accelerated software package that automates motion-corrected marker-free tomographic alignment and reconstruction. It includes robust GPU-accelerated CTF estimation, offering fast, accurate, and easy integration into subtomogram processing workflows. AreTomo2 is capable of on-the-fly reconstruction of tomograms and CTF estimation in parallel with tilt series collection, enabling real-time sample quality assessment and collection parameter adjustments.",
    solution_creators=["Kyle Harrington"],
    cite=[{
        "text": "AreTomo: An integrated software package for automated marker-free, motion-corrected cryo-electron tomographic alignment and reconstruction, J. Struct Biology: X Vol 6, 2022",
        "url": "https://github.com/czimaginginstitute/AreTomo2"
    }],
    tags=["tomography", "cryo-electron", "GPU-acceleration", "CTF estimation", "real-time reconstruction"],
    license="MIT",
    covers=[{
        "description": "Example of an AreTomo2 reconstructed tomogram, showcasing the capabilities of this automated alignment and reconstruction software.",
        "source": "cover.png"
    }],
    album_api_version="0.5.1",
    args=[],
    run=run,
    install=install,
    dependencies={"environment_file": env_file},
)
