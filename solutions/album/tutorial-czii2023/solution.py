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

def inject_javascript_into_notebook(notebook_path):
    import json
    
    # JavaScript snippet to be injected
    js_code = """
    <script>
    require(["base/js/namespace", "base/js/events"], function(Jupyter, events) {
        events.on("notebook_loaded.Notebook", function() {
            Jupyter.notebook.execute_all_cells();
            setTimeout(function() {
                $('#RISEButton').click();
            }, 5000); // Adjust the timeout as needed
        });
    });
    </script>
    """

    # Read the notebook
    with open(notebook_path, 'r') as file:
        notebook = json.load(file)

    # Check if the notebook already has a cell for the JS snippet
    js_cell_exists = any(cell['cell_type'] == 'code' and js_code in cell['source']
                         for cell in notebook['cells'])

    # Add the JS snippet if it doesn't exist
    if not js_cell_exists:
        js_cell = {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": f"%%html\n{js_code}"
        }
        notebook['cells'].insert(0, js_cell)

    # Save the notebook
    with open(notebook_path, 'w') as file:
        json.dump(notebook, file, indent=2)

def install():
    import subprocess

    repo_url = "https://github.com/kephale/cold-storage.git"
    clone_path = local_repository_path()

    # Clone the repository if it doesn't exist
    if not os.path.exists(os.path.join(clone_path, ".git")):
        subprocess.check_call(["git", "clone", repo_url, clone_path])

        # Inject JavaScript into the tutorial notebook
        tutorial_notebook_path = os.path.join(local_repository_path(), "tutorial.ipynb")
        inject_javascript_into_notebook(tutorial_notebook_path)
    
    def run_command(command):
        try:
            subprocess.check_call(command, shell=True)
            print(f"Successfully ran command: {' '.join(command)}")
        except subprocess.CalledProcessError as e:
            print(f"Error in running command: {' '.join(command)}\nError: {str(e)}")

    run_command("jupyter nbextension install --py hide_code --sys-prefix")
    run_command("jupyter nbextension enable --py hide_code --sys-prefix")
    run_command("jupyter serverextension enable --py hide_code")
    

def run():
    # Launch Jupyter Notebook
    import subprocess
    import webbrowser
    import time

    os.chdir(local_repository_path())
    
    # Path to the tutorial notebook
    notebook_path = os.path.join(local_repository_path(), "tutorial.ipynb")

    # Launch Jupyter Notebook
    url = "http://localhost:8888/notebooks/" + notebook_path
    subprocess.Popen(["jupyter", "notebook", "--NotebookApp.token=''"])
    
    # Allow time for the Jupyter server to start
    time.sleep(5)

    # Open the notebook in the default web browser
    webbrowser.open_new(url)


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
