###album catalog: cold-storage

import os

from album.runner.api import setup, get_data_path, get_args


env_file = """channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.11
"""

# TODO install could check the install status of target solution on remote machine

def run():
    import subprocess
    import re
    import threading
    
    args = get_args()

    remote_host = args.remote_host
    remote_user = args.remote_user
    mrc_file_path = args.mrcfile

    # TODO fix hard coded remote album
    album_path = "/hpc/mydata/kyle.harrington/micromamba/envs/album/bin/album"

    # Run the local Album solution remotely with no browser opening
    remote_album_command = f"{album_path} run neuroglancer:view-mrc:0.0.4 --mrcfile {mrc_file_path} --open_browser False"

    # SSH command for running the Album solution remotely
    ssh_command = f"ssh {remote_user}@{remote_host} '{remote_album_command}'"

    # Shared list to store potential URLs
    potential_urls = []

    try:
        # Start the SSH command and capture its output
        process = subprocess.Popen(ssh_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Define a function to capture the output
        def capture_output():
            for line in process.stdout:
                print("Debug: Captured line:", line.strip())  # Debugging
                potential_urls.append(line.strip())

        # Start the thread to capture the output
        capture_thread = threading.Thread(target=capture_output)
        capture_thread.start()

        # Check for URL in the shared list
        url = None
        while url is None:
            time.sleep(1)  # Wait a bit before checking again
            while potential_urls:
                line = potential_urls.pop(0)
                urls = re.findall(r'http[s]?://[^/]+/', line)
                if urls:
                    url = urls[0]
                    break

        # Extract the port number from the URL
        port = int(url.split(':')[-1].rstrip('/'))
        print(f"Port extracted: {port}")

        # SSH command for port forwarding
        ssh_port_forwarding_command = f"ssh -L {port}:localhost:{port} {remote_user}@{remote_host}"

        # Start the SSH port forwarding
        subprocess.Popen(ssh_port_forwarding_command, shell=True)

        print(f"Access Neuroglancer at: http://localhost:{port}/")

    except Exception as e:
        print(f"Error: {e}")

    
setup(
    group="neuroglancer",
    name="view-remote-mrc",
    version="0.0.1",
    title="View a remote MRC file with neuroglancer",
    description="Neuroglancer viewer for MRC files that runs on a remote system.",
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
        {"name": "remote_host", "type": "string", "required": True, "description": "Remote host address"},
        {"name": "remote_user", "type": "string", "required": True, "description": "Username for the remote host"},
        {"name": "mrcfile", "type": "file", "required": True, "description": "Path to the MRC file on the remote machine"},
        {"name": "mmap", "type": "boolean", "required": False, "description": "Use memory-mapped file for MRC file"},
    ],  
    run=run,
    dependencies={"environment_file": env_file},
)
