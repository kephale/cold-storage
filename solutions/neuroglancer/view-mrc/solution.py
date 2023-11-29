###album catalog: cold-storage

import os

from album.runner.api import setup, get_data_path, get_args


env_file = """channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.11
  - pip
  - pip:
    - neuroglancer
    - mrcfile
"""


def local_repository_path():
    if not os.path.exists(get_data_path()):
        os.makedirs(get_data_path())

    return os.path.join(get_data_path(), "git")


def install():
    import subprocess

    # URL for the gist repository
    gist_url = "https://gist.github.com/kephale/59a255383e9e1f5f096dedf657a5a091.git"

    # Path to clone the gist
    clone_path = local_repository_path()

    # Clone the gist
    if not os.path.exists(os.path.join(clone_path, ".git")):
        subprocess.check_call(["git", "clone", gist_url, clone_path])

# Modify the run function to run the script from the gist
def run():
    import subprocess
    import webbrowser
    import re
    import threading

    # Get the path to the script
    script_path = os.path.join(local_repository_path(), "mrc_neuroglancer.py")

    if not os.path.exists(script_path):
        print(f"Script not found at {script_path}")
        return

    command = ["python", script_path]
    for arg in vars(get_args()):
        value = getattr(get_args(), arg)
        command.append(f"--{arg}")
        if value is not None:
            command.append(str(value))

    print(f"Running {command}")

    try:
        # Start the script without waiting for it to complete
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Use a thread to read and process the output
        def process_output():
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(output.strip())
                    urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', output.strip())
                    if urls:
                        print(f"Opening URL: {urls[0]}")
                        webbrowser.open(urls[0])
                        break

        thread = threading.Thread(target=process_output)
        thread.start()

    except Exception as e:
        print(f"Error running script: {e}")
        
setup(
    group="neuroglancer",
    name="view-mrc",
    version="0.0.2",
    title="View a MRC file with neuroglancer",
    description="Neuroglancer viewer for MRC files.",
    solution_creators=["Ashley Anderson III, Kyle Harrington"],
    cite=[
        {
            "text": "Neuroglancer by Google folks.",
            "url": "https://github.com/google/neuroglancer",
        }
    ],
    tags=[
        "mrc",
        "neuroglancer",
        "visualization",
    ],
    license="Apache v2",
    covers=[
        {
            "description": "Example of Neuroglancer visualizing EMPIAR-10548 dataset.",
            "source": "cover.png",
        }
    ],
    album_api_version="0.5.1",
    args=[
        {"name": "mrcfile", "type": "file", "required": True, "description": "Path to the MRC file"},
        {"name": "mmap", "type": "boolean", "required": False, "description": "Use memory-mapped file for MRC file"},
    ],
    run=run,
    install=install,
    dependencies={"environment_file": env_file},
)
