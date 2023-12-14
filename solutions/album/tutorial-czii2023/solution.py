from album.runner.api import setup, get_args

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
"""



def install():
    import subprocess
    
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

    subprocess.run(["jupyter", "notebook"])


# Set up the Album catalog entry
setup(
    group="album",
    name="tutorial-czii2023",
    version="0.1.1",
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
