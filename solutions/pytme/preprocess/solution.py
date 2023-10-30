import os
from album.runner.api import setup, get_data_path

# Please import additional modules at the beginning of your method declarations.
# More information: https://docs.album.solutions/en/latest/solution-development/

def local_script_path():
    if not os.path.exists(get_data_path()):
        os.makedirs(get_data_path())
    
    return os.path.join(get_data_path(), "preprocess.py")

def install():
    import urllib.request
    
    remote_path = "https://raw.githubusercontent.com/KosinskiLab/pyTME/866fd928aefcf37a28f7482caceb737f71525eb3/scripts/preprocess.py"

    local_path = local_script_path()
    
    try:
        urllib.request.urlretrieve(remote_path, local_path)
        print(f"Downloaded {remote_path} to {local_path}")
    except Exception as e:
        print(f"Failed to download {remote_path}: {str(e)}")
    

def run():
    import subprocess

    subprocess.run(["python", local_script_path()], check=True)



setup(
    group="pytme",
    name="preprocess",
    version="0.0.2",
    title="preprocessing for pytme.",
    description="A command-line preprocessing tool for pytme",
    solution_creators=["Kyle Harrington"],
    cite=[{"text": "KosinskiLab.", "url": "https://github.com/KosinskiLab/pyTME"}],
    tags=["imaging", "cryoet", "Python", "template matching"],
    license="MIT",
    covers=[],
    album_api_version="0.5.1",
    args=[
        {
            "name": "output_path",
            "type": "file",
            "description": "The output file name (mrc).",
            "required": True
        },
        {
            "name": "input_path",
            "type": "file",
            "description": "The input file name (mrc) to be preprocessed.",
            "required": True
        },
        {
            "name": "parameter_path",
            "type": "file",
            "description": "A YAML file specifying preprocessing parameters. This can be created with pytme:preprocess-gui.",
            "required": True
        }
        
    ],
    install=install,
    run=run,
    dependencies={
        "parent": {
            "group": "pytme",
            "name": "parent",
            "version": "0.0.2",
        }
    },
)
