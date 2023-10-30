import os
from album.runner.api import setup, get_data_path

# Please import additional modules at the beginning of your method declarations.
# More information: https://docs.album.solutions/en/latest/solution-development/

def local_script_path():
    return os.path.join(get_data_path(), "preprocessor_gui.py")

def install():
    import urllib.request
    
    remote_path = "https://raw.githubusercontent.com/KosinskiLab/pyTME/137e518b4910cd1622414ad243c191f09813fc44/scripts/preprocessor_gui.py"

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
    name="preprocess-gui",
    version="0.0.1",
    title="preprocessing gui for pytme.",
    description="A napari-based preprocessing tool for pytme",
    solution_creators=["Kyle Harrington"],
    cite=[{"text": "KosinskiLab.", "url": "https://github.com/KosinskiLab/pyTME"}],
    tags=["imaging", "cryoet", "Python", "template matching"],
    license="MIT",
    covers=[{
        "description": "Cover image for pyTME's preprocess gui. Shows an instance of napari running the plugin. Image comes from https://kosinskilab.github.io/pyTME/quickstart/preprocessing.html.",
        "source": "cover.png"
    }],
    album_api_version="0.5.1",
    args=[],
    run=run,
    dependencies={
        "parent": {
            "group": "pytme",
            "name": "parent",
            "version": "0.0.1",
        }
    },
)
