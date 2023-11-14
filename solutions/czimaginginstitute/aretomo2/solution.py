###album catalog: cold-storage

import os

from album.runner.api import setup, get_data_path, get_args


env_file = """name: aretomo2
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.11
"""


def local_repository_path():
    if not os.path.exists(get_data_path()):
        os.makedirs(get_data_path())

    return os.path.join(get_data_path(), "git")


def install():
    import os
    import subprocess

    # TODO: convenience hack for Kyle
    # Check if 'CUDAHOME' is in environment variables
    if "CUDAHOME" not in os.environ:
        # 'CUDAHOME' is not set, now check for 'mod_cuda_prefix'
        if "mod_cuda_prefix" in os.environ:
            # This is the value from `module load ...`
            os.environ["CUDAHOME"] = os.environ["mod_cuda_prefix"]
            print(f"Setting CUDAHOME to {os.environ['CUDAHOME']}")
        else:
            print("'CUDAHOME' is not set and 'mod_cuda_prefix' is also not available.")
    else:
        print(f"'CUDAHOME' is already set to: {os.environ['CUDAHOME']}")

    # URL for the AreTomo2 repository
    repo_url = "https://github.com/czimaginginstitute/AreTomo2.git"

    # Path to clone the repository
    clone_path = local_repository_path()

    # Check if the repo already exists, if not, clone it
    if not os.path.exists(os.path.join(clone_path, ".git")):
        subprocess.check_call(["git", "clone", repo_url, clone_path])

    # Change to the cloned repository directory
    os.chdir(clone_path)

    # Modify makefile11 to remove hardcoded CUDAHOME line
    makefile_path = os.path.join(clone_path, "makefile11")
    with open(makefile_path, "r") as file:
        makefile_contents = file.readlines()

    with open(makefile_path, "w") as file:
        for line in makefile_contents:
            if line.startswith("CUDAHOME ="):
                continue  # Skip the hardcoded CUDAHOME line
            file.write(line)

    # Use subprocess to compile AreTomo2
    # Replace 'makefile11' with the appropriate makefile based on your GPU's compute capability
    subprocess.check_call(["make", "exe", "-f", "makefile11"], env=os.environ)


def run():
    import subprocess
    
    # Get the path to the AreTomo2 executable
    aretomo2_path = os.path.join(local_repository_path(), "AreTomo2")

    # Ensure that the executable exists
    if not os.path.exists(aretomo2_path):
        print(f"Executable not found at {aretomo2_path}")
        return

    # Get arguments from get_args()
    args_dict = get_args()

    # Construct the command with arguments
    command = [aretomo2_path]
    for arg, value in args_dict.items():
        command.append(f"--{arg}")
        if value is not None:
            command.append(str(value))

    # Execute the command
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running AreTomo2: {e}")

setup(
    group="czimaginginstitute",
    name="aretomo2",
    version="0.0.1",
    title="AreTomo2: Automated Tomographic Alignment and Reconstruction",
    description="AreTomo2 is a multi-GPU accelerated software package that automates motion-corrected marker-free tomographic alignment and reconstruction. It includes robust GPU-accelerated CTF estimation, offering fast, accurate, and easy integration into subtomogram processing workflows. AreTomo2 is capable of on-the-fly reconstruction of tomograms and CTF estimation in parallel with tilt series collection, enabling real-time sample quality assessment and collection parameter adjustments.",
    solution_creators=["Kyle Harrington"],
    cite=[
        {
            "text": "AreTomo: An integrated software package for automated marker-free, motion-corrected cryo-electron tomographic alignment and reconstruction, J. Struct Biology: X Vol 6, 2022",
            "url": "https://github.com/czimaginginstitute/AreTomo2",
        }
    ],
    tags=[
        "tomography",
        "cryo-electron",
        "GPU-acceleration",
        "CTF estimation",
        "real-time reconstruction",
    ],
    license="MIT",
    covers=[
        {
            "description": "Example of an AreTomo2 reconstructed tomogram, showcasing the capabilities of this automated alignment and reconstruction software.",
            "source": "cover.png",
        }
    ],
    album_api_version="0.5.1",
    args=[
        {
            "name": "InMrc",
            "type": "file",
            "description": "Input MRC file that stores the tomographic tilt series.",
            "required": True,
        },
        {
            "name": "OutMrc",
            "type": "file",
            "description": "Output MRC file that stores the aligned tilt series.",
            "required": True,
        },
        {
            "name": "AlnFile",
            "type": "file",
            "description": "Alignment file to be loaded and applied to the loaded tilt series.",
            "required": False,
        },
        {
            "name": "AngFile",
            "type": "file",
            "description": "Text file containing tilt angles. Must match the number and order of projection images in the input MRC file.",
            "required": False,
        },
        {
            "name": "TmpFile",
            "type": "file",
            "description": "Temporary image file for debugging.",
            "required": False,
        },
        {
            "name": "LogFile",
            "type": "file",
            "description": "Log file storing alignment data.",
            "required": False,
        },
        {
            "name": "TiltRange",
            "type": "string",
            "description": "Min and max tilts. By default, the header values are used.",
            "required": False,
        },
        {
            "name": "TiltAxis",
            "type": "float",
            "description": "Tilt axis, default header value.",
            "required": False,
        },
        {
            "name": "AlignZ",
            "type": "integer",
            "description": "Volume height for alignment, default 256",
            "required": False,
        },
        {
            "name": "VolZ",
            "type": "integer",
            "description": "Volume z height for reconstruction. Must be greater than 0 to reconstruct a volume. Default is 0, only aligned tilt series will be generated.",
            "required": False,
        },
        {
            "name": "OutBin",
            "type": "integer",
            "description": "Binning for aligned output tilt series, default 1",
            "required": False,
        },
        {
            "name": "Gpu",
            "type": "string",
            "description": "GPU IDs. Default 0.",
            "required": False,
        },
        {
            "name": "TiltCor",
            "type": "string",
            "description": "Correct the offset of tilt angle. Can be followed by two values for specifying offset adjustment in alignment and/or reconstruction.",
            "required": False,
        },
        {
            "name": "ReconRange",
            "type": "string",
            "description": "Specifies the min and max tilt angles for 3D volume reconstruction. Excludes tilt images outside this range in the reconstruction.",
            "required": False,
        },
        {
            "name": "PixSize",
            "type": "float",
            "description": "Pixel size in Angstrom of the input tilt series, required for dose weighting. If missing, dose weighting is disabled.",
            "required": False,
        },
        {
            "name": "Kv",
            "type": "float",
            "description": "High tension in kV, required for dose weighting and CTF estimation",
            "required": False,
        },
        {
            "name": "ImgDose",
            "type": "float",
            "description": "Dose on sample in each image exposure in e/A2. Not the accumulated dose. If missing, dose weighting is disabled.",
            "required": False,
        },
        {
            "name": "Cs",
            "type": "float",
            "description": "Spherical aberration in mm, required only for CTF correction",
            "required": False,
        },
        {
            "name": "$-10s",
            "type": "float",
            "description": "Amplitude contrast, default 0.07",
            "required": False,
        },
        {
            "name": "-10s",
            "type": "string",
            "description": "Guess of phase shift and search range in degree, required for CTF estimation with a phase plate installed.",
            "required": False,
        },
        {
            "name": "FlipVol",
            "type": "boolean",
            "description": "If non-zero, the reconstructed volume is saved in xyz fashion. Default is xzy.",
            "required": False,
        },
        {
            "name": "FlipInt",
            "type": "boolean",
            "description": "Flip the intensity of the volume. Default 0 means no flipping. Non-zero value flips.",
            "required": False,
        },
        {
            "name": "Sart",
            "type": "string",
            "description": "Specify number of SART iterations and number of projections per update. Default values are 15 and 5, respectively.",
            "required": False,
        },
        {
            "name": "Wbp",
            "type": "boolean",
            "description": "If specified as 1, enables weighted back projection for volume reconstruction.",
            "required": False,
        },
        {
            "name": "DarkTol",
            "type": "float",
            "description": "Set tolerance for removing dark images. Range is (0, 1), default 0.7. Higher value is more restrictive.",
            "required": False,
        },
        {
            "name": "TiltScheme",
            "type": "string",
            "description": "Determines sequence of tilt image acquisition, needed for accumulated dose determination. Three parameters required: starting angle, tilt step, and collection scheme (1, 2, or 3).",
            "required": False,
        },
        {
            "name": "OutXF",
            "type": "boolean",
            "description": "If set to a non-zero value, generates an IMOD compatible XF file.",
            "required": False,
        },
        {
            "name": "OutImod",
            "type": "integer",
            "description": "Generates Imod files needed by Relion4 or Warp for subtomogram averaging. Saved in a subfolder named after the output MRC file.",
            "required": False,
        },
        {
            "name": "Align",
            "type": "boolean",
            "description": "Skip alignment if set to 0. Used when the input MRC file is an aligned tilt series. Default is 1.",
            "required": False,
        },
        {
            "name": "CropVol",
            "type": "string",
            "description": "Crop the reconstructed volume to specified sizes in x and y directions. Enabled only when -RoiFile is enabled.",
            "required": False,
        },
        {
            "name": "Bft",
            "type": "string",
            "description": "B-factors for low-pass filter used in cross correlation. First value for global measurement, second for local measurement.",
            "required": False,
        },
        {
            "name": "IntpCor",
            "type": "boolean",
            "description": "Enables correction for information loss due to linear interpolation. Default setting value 1 enables the correction.",
            "required": False,
        },
    ],
    run=run,
    install=install,
    dependencies={"environment_file": env_file},
)
