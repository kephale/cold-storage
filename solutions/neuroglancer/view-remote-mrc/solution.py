###album catalog: cold-storage

import os

from album.runner.api import setup, get_data_path, get_args


env_file = """channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.11
  - urllib3
"""

# TODO install could check the install status of target solution on remote machine

def run():
    import subprocess
    import re
    import threading
    import time
    from urllib.parse import urlparse
    import signal
    
    args = get_args()

    remote_host = args.remote_host
    remote_user = args.remote_user
    mrc_file_path = args.mrcfile
    reuse_ssh = args.reuse_ssh

    # TODO fix hard coded remote album
    album_path = "/hpc/mydata/kyle.harrington/micromamba/envs/album/bin/album"

    # Run the local Album solution remotely with no browser opening
    remote_album_command = f"{album_path} run neuroglancer:view-mrc:0.0.6 --mrcfile {mrc_file_path} --open_browser False"

    # SSH command for running the Album solution remotely
    if not reuse_ssh:
        ssh_command = f"ssh {remote_user}@{remote_host} '{remote_album_command}'"
    else:
        ssh_command = f"ssh -o ControlPath=~/.ssh/sockets/%r@%h-%p {remote_user}@{remote_host} '{remote_album_command}'"

    print(f"Remote command: {remote_album_command}")
    print(f"SSH command: {ssh_command}")
    
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

        # Polling for the URL file
        timeout = 60  # Timeout in seconds
        start_time = time.time()
        url_file_path = "/tmp/neuroglancer_viewer_url.txt"
        url = None

        while time.time() - start_time < timeout:
            ssh_command_read_url = f"ssh {remote_user}@{remote_host} 'cat {url_file_path}'"
            proc = subprocess.Popen(ssh_command_read_url, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = proc.communicate()

            if proc.returncode == 0 and stdout:
                url = stdout.strip()
                break
            else:
                time.sleep(5)  # Wait for 5 seconds before retrying

        if url:
            parsed_url = urlparse(url)
            port = parsed_url.port
            path = parsed_url.path
            query = parsed_url.query
            full_path = f"{path}?{query}" if query else path
            localhost_url = f"http://localhost:{port}{full_path}"
            print(f"Access Neuroglancer at: {localhost_url}")
        else:
            print("Failed to retrieve the Neuroglancer URL within the timeout period.")

                
        # SSH command for port forwarding
        if not reuse_ssh:
            ssh_port_forwarding_command = f"ssh -L {port}:localhost:{port} {remote_user}@{remote_host}"
        else:
            ssh_port_forwarding_command = f"ssh -o ControlPath=~/.ssh/sockets/%r@%h-%p -L {port}:localhost:{port} {remote_user}@{remote_host}"

        # Start the SSH port forwarding
        port_forward_proc = subprocess.Popen(ssh_port_forwarding_command, shell=True)

        print(f"Access Neuroglancer at: {localhost_url}")

    except Exception as e:
        print(f"Error: {e}")


    def signal_handler(signum, frame):
        print("Signal received, exiting.")
        process.kill()
        port_forward_proc.kill()

    # Set up signal handling
    signal.signal(signal.SIGINT, signal_handler)

    print("Press Ctrl+C to exit...")
    signal.pause()  # This will block until a signal is received
    
setup(
    group="neuroglancer",
    name="view-remote-mrc",
    version="0.0.6",
    title="View a remote MRC file with neuroglancer",
    description="Neuroglancer viewer for MRC files that runs on a remote system.",
    solution_creators=["Kyle Harrington"],
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
        {"name": "reuse_ssh", "type": "boolean", "required": False, "description": "Reuse a SSH connection if your SSH is setup properly", "default": False},
        {"name": "mrcfile", "type": "file", "required": True, "description": "Path to the MRC file on the remote machine"},
        {"name": "mmap", "type": "boolean", "required": False, "description": "Use memory-mapped file for MRC file"},
    ],  
    run=run,
    dependencies={"environment_file": env_file},
)
