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
    import time

    # Get the path to the script
    script_path = os.path.join(local_repository_path(), "mrc_neuroglancer.py")

    if not os.path.exists(script_path):
        print("Debug: Script not found at", script_path)
        return

    command = ["python", "-u", script_path]
    for arg in vars(get_args()):
        value = getattr(get_args(), arg)
        if arg != "open_browser":
            command.append(f"--{arg}")
            if value is not None:
                command.append(str(value))

    # Shared list to store output from the subprocess
    output_lines = []

    open_browser = get_args().open_browser

    print("Launching neuroglancer")
    
    try:
        # Start the script without waiting for it to complete
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # Define a function to capture the output
        def capture_output():
            for line in process.stdout:
                print("STDOUT:", line.strip())
            for err_line in process.stderr:
                print("STDERR:", err_line.strip())

        # Start the thread to capture the output
        capture_thread = threading.Thread(target=capture_output)
        capture_thread.start()

        url_found = False

        # Main thread loop for processing the captured output
        while True:
            # Check if the thread is still alive, and join with timeout
            if capture_thread.is_alive():
                capture_thread.join(timeout=1)
            else:
                # If the thread is not alive, break the loop as the server might have stopped
                break

            for line in output_lines:
                print(f"Debug: output {line}")
                urls = re.findall(r'http[s]?://...', line)
                if urls and not url_found:
                    url_found = True
                    print("URL:", urls[0])
                    if open_browser:
                        webbrowser.open(urls[0])

            output_lines.clear()  # Clear the list after processing

            # If URL is found but browser is not to be opened, continue running
            if url_found and not open_browser:
                continue

    except Exception as e:
        print("Error running script:", e)

    print("Done")
    
setup(
    group="neuroglancer",
    name="view-mrc",
    version="0.0.6",
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
        {"name": "open_browser", "type": "boolean", "required": False, "default": True, "description": "Automatically open the browser with the URL"},
    ],
    run=run,
    install=install,
    dependencies={"environment_file": env_file},
)
