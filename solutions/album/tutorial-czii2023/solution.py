import os
from album.runner.api import setup, get_args, get_data_path

###album catalog: cold-storage

# Environment file for Jupyter Notebook with RISE
env_file = """channels:
  - conda-forge
  - defaults
dependencies:
  - "notebook<7"
  - rise
  - pip
  - pip:
    - hide_code
    - "git+https://gitlab.com/album-app/album.git"
    - "git+https://gitlab.com/album-app/plugins/album-gui.git"
"""


def local_repository_path():
    path = os.path.join(get_data_path(), "album-tutorial-czii2023")
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def create_custom_html_template():
    import notebook
    import os

    notebook_dir = os.path.dirname(notebook.__file__)
    template_dir = os.path.join(notebook_dir, "templates")
    custom_template_dir = os.path.join(local_repository_path(), "custom_templates")
    os.makedirs(custom_template_dir, exist_ok=True)

    template_path = os.path.join(template_dir, "notebook.html")
    custom_template_path = os.path.join(custom_template_dir, "notebook.html")

    js_code = """<script>
    require(["base/js/namespace", "base/js/events"], function(Jupyter, events) {
        events.on("notebook_loaded.Notebook", function() {
            Jupyter.notebook.execute_all_cells();
            setTimeout(function() {
                $('#RISEButton').click();
            }, 5000); // Adjust the timeout as needed
        });
    });
    </script>"""

    with open(template_path, 'r') as original:
        with open(custom_template_path, 'w') as custom:
            for line in original:
                custom.write(line)
                if '</body>' in line:
                    custom.write(js_code + '\n')

    return custom_template_dir

def configure_jupyter_to_use_custom_template(custom_template_dir):
    from notebook import notebookapp
    import json

    config_dir = notebookapp.jupyter_config_dir()
    config_file_path = os.path.join(config_dir, 'jupyter_notebook_config.json')

    if os.path.exists(config_file_path):
        with open(config_file_path, 'r') as file:
            config = json.load(file)
    else:
        config = {}

    config['NotebookApp'] = {'extra_template_paths': [custom_template_dir]}

    with open(config_file_path, 'w') as file:
        json.dump(config, file, indent=2)

        
def install():
    import subprocess

    repo_url = "https://github.com/kephale/album-tutorial-czii2023"
    clone_path = local_repository_path()

    # Clone the repository if it doesn't exist
    if not os.path.exists(os.path.join(clone_path, ".git")):
        subprocess.check_call(["git", "clone", repo_url, clone_path])

    # Create custom HTML template and configure Jupyter
    custom_template_dir = create_custom_html_template()
    configure_jupyter_to_use_custom_template(custom_template_dir)
    
    def run_command(command):
        try:
            subprocess.check_call(command, shell=True)
            print(f"Successfully ran command: {' '.join(command)}")
        except subprocess.CalledProcessError as e:
            print(f"Error in running command: {' '.join(command)}\nError: {str(e)}")

    run_command("jupyter nbextension install --py hide_code --sys-prefix")
    run_command("jupyter nbextension enable --py hide_code --sys-prefix")
    run_command("jupyter serverextension enable --py hide_code")

def find_available_port():
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]    
    

def run():
    # Launch Jupyter Notebook
    import subprocess
    import webbrowser
    import time

    os.chdir(local_repository_path())
    
    # Find an available port for the Jupyter server
    port = find_available_port()

    # Path to the tutorial notebook
    notebook_path = "tutorial.ipynb"

    # Launch Jupyter Notebook on the available port
    url = f"http://localhost:{port}/notebooks/{notebook_path}"
    jupyter_process = subprocess.Popen(["jupyter", "notebook", f"--port={port}", "--NotebookApp.token=''"])
    
    # Allow time for the Jupyter server to start
    time.sleep(5)

    # Open the notebook in the default web browser
    webbrowser.open_new(url)

    # Wait for the Jupyter server process to terminate
    try:
        jupyter_process.wait()
    except KeyboardInterrupt:
        # Handle manual interruption (Ctrl+C)
        print("\nShutting down Jupyter server...")
        jupyter_process.terminate()


# Set up the Album catalog entry
setup(
    group="album",
    name="tutorial-czii2023",
    version="0.1.2",
    title="album tutorial for czii in 2023",
    description="This solution runs a Jupyter-based album tutorial presentation.",
    solution_creators=["Kyle Harrington"],
    tags=["jupyter", "presentation", "album"],
    license="MIT",
    album_api_version="0.5.1",
    dependencies={"environment_file": env_file},
    run=run,
    install=install,
)
