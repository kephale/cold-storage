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
    return imagej.init('2.3.0')


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

    try:
        # create empty image
        img = ij.op().run("create.img", ij.py.to_java([100, 100, 100]))

        # write random values into image
        Random = jimport("java.util.Random")
        random = Random()
        for t in img:
            t.set(random.nextInt())

        # apply DoG filter
        img = ij.op().filter().dog(img, 5.0, 2.0)

        # delete output file if it exists already, create parent folder
        image_path = str(get_args().output_image_path)
        if os.path.exists(image_path):
            os.remove(image_path)
        Path(os.path.abspath(image_path)).parent.mkdir(parents=True, exist_ok=True)

        # save image to output file
        ij.io().save(ij.dataset().create(img), image_path)

    finally:
        ij.dispose()


def prepare_test():
    from album.runner.api import get_cache_path
    return {
        "--output_image_path": str(get_cache_path().joinpath("output.tif"))
    }


def test():
    from album.runner.api import get_cache_path
    assert get_cache_path().joinpath("output.tif").exists()


setup(
    group="my-group",
    name="my-solution",
    version="0.1.0",
    title="ImageJ2 template",
    description="An Album solution template generating an ImgLib2 image with random values in ImageJ2.",
    authors=["Album team"],
    cite=[{
        "text": "Rueden, C. T., Schindelin, J., Hiner, M. C., DeZonia, B. E., Walter, A. E., Arena, E. T., & Eliceiri, K. W. (2017). ImageJ2: ImageJ for the next generation of scientific image data. BMC Bioinformatics, 18(1).",
        "doi": "10.1186/s12859-017-1934-z",
        "url": "https://imagej.net"
    }],
    tags=["template", "java", "imagej2", "scijava", "scyjava"],
    license="unlicense",
    documentation=["documentation.md"],
    covers=[{
        "description": "Dummy cover image.",
        "source": "cover.png"
    }],
    album_api_version="0.3.1",
    args=[{
        "name": "output_image_path",
        "type": "file",
        "description": "The output file name to where a random image is going to be saved.",
        "required": True
    }],
    install=install,
    run=run,
    pre_test=prepare_test,
    test=test,
    dependencies={'environment_file': env_file}
)
