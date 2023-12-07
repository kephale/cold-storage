from album.runner.api import setup, get_args

###album catalog: cold-storage

# Environment file for Jupyter Lab with RISE
env_file = """channels:
  - conda-forge
  - defaults
dependencies:
  - jupyterlab
  - rise
"""


def run():
    import subprocess

    subprocess.run(["jupyter", "lab"])


# Set up the Album catalog entry
setup(
    group="album",
    name="tutorial-czii2023",
    version="0.1.0",
    title="album tutorial for czii in 2023",
    description="This solution runs a Jupyter-based album tutorial presentation.",
    solution_creators=["Kyle Harrington"],
    tags=["jupyter", "presentation", "album"],
    license="MIT",
    album_api_version="0.5.1",
    dependencies={"environment_file": env_file},
    run=run,
)
