###album catalog: cold-storage

from io import StringIO

import os
from album.runner.api import setup, get_data_path, get_args

env_file = StringIO(
    """channels:
  - conda-forge
  - defaults    
dependencies:
  - python>=3.8
  - pip
  - numpy
  - matplotlib
  - scikit-image
  - pip:
    - mrcfile
"""
)

def crop_to_non_zero_region(data):
    import numpy as np
    non_zero_indices = np.nonzero(data)
    min_indices = np.min(non_zero_indices, axis=1)
    max_indices = np.max(non_zero_indices, axis=1)
    return data[min_indices[0]:max_indices[0]+1, 
                min_indices[1]:max_indices[1]+1, 
                min_indices[2]:max_indices[2]+1]

def compute_fingerprint(path_to_mrc):
    import mrcfile
    import numpy as np
    import matplotlib.pyplot as plt
    from skimage.transform import resize
    import base64
    from io import BytesIO
    
    with mrcfile.open(path_to_mrc) as mrc:
        tomogram = mrc.data
        original_size = tomogram.shape
        cropped_tomogram = crop_to_non_zero_region(tomogram)
        cropped_size = cropped_tomogram.shape

        foreground = cropped_tomogram[cropped_tomogram > 0]
        stats = {
            'mean': np.mean(foreground),
            'std_dev': np.std(foreground),
            'percentile_0.5': np.percentile(foreground, 0.5),
            'percentile_99.5': np.percentile(foreground, 99.5),
            'min': np.min(foreground),
            'max': np.max(foreground)
        }

        counts, bins = np.histogram(foreground, bins=50)

        center_slice = cropped_tomogram[cropped_tomogram.shape[0] // 2, :, :]
        center_slice_resized = resize(center_slice, (256, 256), anti_aliasing=True)

        buffer = BytesIO()
        plt.imsave(buffer, center_slice_resized, format='png', cmap='gray')
        base64_image = base64.b64encode(buffer.getvalue()).decode()

        return {
            'original_size': original_size,
            'cropped_size': cropped_size,
            'statistics': stats,
            'histogram': {'bins': bins.tolist(), 'counts': counts.tolist()},
            'center_slice_base64': base64_image
        }

def append_html_fingerprint(f, fingerprint, filename, index):
    f.write(f"<h2>Tomogram {index+1} - {filename}</h2>")
    f.write(f"<p>Original Size: {fingerprint['original_size']}<br>Cropped Size: {fingerprint['cropped_size']}</p>")
    f.write(f"<p>Statistics:<br>Mean: {fingerprint['statistics']['mean']}<br>Standard Deviation: {fingerprint['statistics']['std_dev']}<br>0.5 Percentile: {fingerprint['statistics']['percentile_0.5']}<br>99.5 Percentile: {fingerprint['statistics']['percentile_99.5']}<br>Min: {fingerprint['statistics']['min']}<br>Max: {fingerprint['statistics']['max']}</p>")
    histogram_html = "<p>Histogram:<br>Bins: {}<br>Counts: {}</p>".format(fingerprint['histogram']['bins'], fingerprint['histogram']['counts'])
    f.write(histogram_html)
    f.write(f"<img src='data:image/png;base64,{fingerprint['center_slice_base64']}'>")
    f.write("<hr>")

def run():
    mrc_list_path = get_args().mrcindexfile
    html_output = get_args().outputfile

    with open(html_output, 'w') as f:
        f.write("<html><body><h1>Dataset Fingerprints</h1>")

        with open(mrc_list_path, 'r') as file:
            mrc_paths = file.read().splitlines()

        for i, path in enumerate(mrc_paths):
            fingerprint = compute_fingerprint(path)
            filename = os.path.basename(path)
            append_html_fingerprint(f, fingerprint, filename, i)

        f.write("</body></html>")

setup(
    group="kyleharrington",
    name="tomogram-fingerprint",
    version="0.0.3",
    title="Tomogram fingerprint",
    description="Compute the dataset fingerprints of a cryoET tomogram.",
    solution_creators=["Kyle Harrington"],
    cite=[
        {
            "text": "Kyle. Also check out team tomo",
            "url": "",
        }
    ],
    tags=[
        "cryoet",
        "dataset",
    ],
    license="MIT",
    covers=[
        {
            "description": "Example of a dataset.",
            "source": "cover.png",
        }
    ],
    album_api_version="0.5.1",
    args=[
        {"name": "mrcindexfile", "type": "file", "required": True, "description": "Path to the file containing list of MRC files"},
        {"name": "outputfile", "type": "file", "required": True, "description": "Path to the output HTML file"},
    ],
    run=run,
    dependencies={"environment_file": env_file},
)
