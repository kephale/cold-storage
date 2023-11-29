###album catalog: cold-storage

import os
import subprocess

from album.runner.api import setup, get_data_path, get_args

def local_repository_path():
    data_path = get_data_path()
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    return os.path.join(data_path, "ctffind")

def install():
    repo_url = "https://grigoriefflab.umassmed.edu/system/tdf?path=ctffind-4.1.14.tar.gz&file=1&type=node&id=26"
    clone_path = local_repository_path()

    if not os.path.exists(clone_path):
        os.makedirs(clone_path)

    os.chdir(clone_path)
    subprocess.check_call(["wget", repo_url, "-O", "ctffind.tar.gz"])
    subprocess.check_call(["tar", "-zxvf", "ctffind.tar.gz"])
    os.chdir("ctffind-4.1.14")

    subprocess.check_call(["./configure"])# TODO set prefix locations
    subprocess.check_call(["make"])

def run():
    ctffind_path = os.path.join(local_repository_path(), "ctffind-4.1.14", "src", "ctffind")
    if not os.path.exists(ctffind_path):
        print(f"ctffind executable not found at {ctffind_path}")
        return

    args_dict = get_args()
    command = [ctffind_path]
    for arg, value in args_dict.items():
        command.append(f"--{arg}")
        if value is not None:
            command.append(str(value))

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running ctffind: {e}")

setup(
    group="grigoriefflab",
    name="ctffind4",
    version="0.0.1",
    title="CTFFIND4: Fast and Accurate Defocus Estimation",
    description="CTFFIND4 is a software package for accurate and fast estimation of defocus and astigmatism in electron micrographs. It is widely used in cryo-electron microscopy for preprocessing images before further analysis.",
    solution_creators=["Kyle Harrington"],
    cite=[
        {
            "text": "Rohou, A., & Grigorieff, N. (2015). CTFFIND4: Fast and accurate defocus estimation from electron micrographs. Journal of Structural Biology, 192(2), 216-221.",
            "url": "https://grigoriefflab.umassmed.edu/ctffind4",
        }
    ],
    tags=[
        "cryo-electron microscopy",
        "defocus estimation",
        "astigmatism",
        "image processing",
    ],
    license=" Janelia Research Campus Software Copyright 1.1, http://license.janelia.org/license/",
    covers=[
        {
            "description": "Image from https://grigoriefflab.umassmed.edu/ctffind4.",
            "source": "cover.png",
        }
    ],
    album_api_version="0.5.1",
    args=[
    ],
    run=run,
    install=install,
)
