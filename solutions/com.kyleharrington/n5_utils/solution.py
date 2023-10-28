from album.runner.api import setup

# Please import additional modules at the beginning of your method declarations.
# More information: https://docs.album.solutions/en/latest/solution-development/

env_file = """channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.8
  - pyimagej=1.0.2
  - openjdk=11.0.9.1
"""

def init_ij():
    import imagej
    # see this link for initialization options: https://github.com/imagej/pyimagej/blob/master/doc/Initialization.md
    return imagej.init('org.janelia.saalfeldlab:n5-utils:0.0.7-SNAPSHOT')


def install():
    print("Downloading maven dependencies. This may take a while. "
          "By default, maven dependencies are shared between applications - "
          "installing another solution with similar dependencies should be fast.")
    init_ij()


def run():
    from album.runner.api import get_args
    from pathlib import Path
    from scyjava import jimport
    import os

    ij = init_ij()

    View = jimport("org.janelia.saalfeldlab.View")

    # Create an instance of the View class
    view_instance = View()

    # Set the parameters. Here's an example input:
    view_instance.containerPaths = ["s3://janelia-cosem-datasets/jrc_mus-liver/jrc_mus-liver.n5"]
    view_instance.groupLists = ["/em/fibsem-uint8"]
    view_instance.resolutionStrings = ["16,16,16"]
    view_instance.contrastStrings = ["0,255"]
    view_instance.offsetStrings = ["4,4,4"]
    view_instance.axesStrings = ["0,2,1"]
    view_instance.numRenderingThreads = 4
    view_instance.screenScales = [1.0, 0.5, 0.25, 0.125]

    # Call the method of the View class
    result = view_instance.call()




setup(
    group="com.kyleharrington",
    name="n5_utils",
    version="0.1.0",
    title="n5-utils from Saalfeld Lab",
    description="An Album solution for using Saalfeld Lab's n5 utils.",
    authors=["Kyle Harrington"],
    cite=[{
        "text": "Saalfeld lab.",
        "url": "https://github.com/saalfeldlab/n5-utils"
    }],
    tags=["java", "n5", "bigdataviewer", "zarr"],
    license="MIT",
    documentation=[],
    covers=[],
    album_api_version="0.3.1",
    args=[],
    install=install,
    run=run,
    dependencies={'environment_file': env_file}
)
