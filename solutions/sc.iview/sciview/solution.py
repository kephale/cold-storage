from album.runner.api import setup

# Please import additional modules at the beginning of your method declarations.
# More information: https://docs.album.solutions/en/latest/solution-development/

def init_ij():
    import imagej
    # see this link for initialization options: https://github.com/imagej/pyimagej/blob/master/doc/Initialization.md
    return imagej.init(['org.blosc:jblosc', 'sc.iview:sciview'])


def install():
    print("Downloading maven dependencies. This may take a while. "
          "By default, maven dependencies are shared between applications - "
          "installing another solution with similar dependencies should be fast.")
    init_ij()


# def run():
#     from album.runner.api import get_args
#     from pathlib import Path
#     from scyjava import config, jimport
#     import os
#     import subprocess

#     # This should be OS independent instead, currently macos only
#     config.add_option('-Djna.library.path=/opt/homebrew/Cellar/c-blosc/1.21.1/lib')

#     config.endpoints.append('org.janelia.saalfeldlab:n5-utils:0.0.7-SNAPSHOT')
    
#     View = jimport("org.janelia.saalfeldlab.View")
#     CommandLine = jimport("picocli.CommandLine")

#     cmd_script = "n5-view"
    
#     # Define the arguments
#     args = [
#         "-i", "s3://janelia-cosem-datasets/jrc_mus-liver/jrc_mus-liver.n5",
#         "-d", "/em/fibsem-uint8",
#         "-r", "16,16,16",
#         "-c", "0,255",
#         "-o", "4,4,4",
#         "-a", "0,2,1",
#         "-t", "4",
#         "-s", "1.0,0.5,0.25,0.125"
#     ]

#     # Combine the command script with its arguments
#     cmd = [cmd_script] + args

#     # Use subprocess to run the command
#     result = subprocess.run(cmd, capture_output=True, text=True)

#     # If you want to capture and print stdout or stderr
#     print(result.stdout)
#     print(result.stderr)

#     return result

def run():
    import subprocess
    import os
    from jgo import main

    # Define a function to check Java version and decide whether to use the ConcMarkSweepGC flag
    # def needs_concmarksweepgc():
    #     result = subprocess.run(["java", "-version"], capture_output=True, text=True, stderr=subprocess.STDOUT)
    #     return "1.8" in result.stdout

    # Generate cp.txt using Maven
    # maven_cmd = ["mvn", "-Dmdep.outputFile=cp.txt", "-Dmdep.includeScope=runtime", "dependency:build-classpath"]
    # subprocess.run(maven_cmd, check=True)

    # Prepare the java command
    mem = 8  # assuming you want to use 8GB, change as per your needs
    jar_path = os.path.expanduser("~/.m2/repository/org/janelia/saalfeldlab/n5-utils/0.0.7-SNAPSHOT/n5-utils-0.0.7-SNAPSHOT.jar")

    # cmd = [
    #     "java",
    #     f"-Xmx{mem}g",
    #     "-Djna.library.path=/opt/homebrew/Cellar/c-blosc/1.21.1/lib",
    #     "-cp",
    #     f"{jar_path}:cp.txt",  # Using cp.txt as part of the classpath
    #     "org.janelia.saalfeldlab.View"
    # ]

    # s3://janelia-cosem-datasets/jrc_mus-liver/jrc_mus-liver.n5
    
    
    cmd = ["jgo", "sc.iview:sciview:7227a02a22:sc.iview.ImageJMain"]
    

    # main(['org.janelia.saalfeldlab:n5-utils:0.0.7-SNAPSHOT'] + args)
    
    # Use subprocess to run the command
    result = subprocess.run(cmd, capture_output=True, text=True)

    # If you want to capture and print stdout or stderr
    print(result.stdout)
    print(result.stderr)

    # TODO: update the jgo parser to also match s3 paths, not just http
    
    return result



setup(
    group="sc.iview",
    name="sciview",
    version="0.1.0",
    title="sciview",
    description="sciview is a 3D/VR/AR visualization tool for large data from the Fiji community",
    authors=["Kyle Harrington"],
    cite=[{
        "text": "sciview team.",
        "url": "https://github.com/scenerygraphics/sciview"
    }],
    tags=["sciview", "fiji", "imagej", "3d", "vr", "ar"],
    license="MIT",
    documentation=[],
    covers=[{
        "description": "Cover image for sciview. Shows a schematic of the sciview UI with an electron microscopy image that contains segmented neurons.",
        "source": "cover.png"
    }],
    album_api_version="0.3.1",
    args=[],
    install=install,
    run=run,
    dependencies={
        "parent": {
            "group": "com.kyleharrington",
            "name": "fiji_parent",
            "version": "0.1.0",
        }
    },
)


if __name__== "__main__":
    run()