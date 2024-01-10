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

def generate_html(fingerprints):
    html_content = "<html><body><h1>Dataset Fingerprints</h1>"
    for i, fp in enumerate(fingerprints):
        html_content += f"<h2>Tomogram {i+1}</h2>"
        html_content += "<p>Original Size: {}<br>Cropped Size: {}</p>".format(fp['original_size'], fp['cropped_size'])
        html_content += "<p>Statistics:<br>Mean: {}<br>Standard Deviation: {}<br>0.5 Percentile: {}<br>99.5 Percentile: {}<br>Min: {}<br>Max: {}</p>".format(
            fp['statistics']['mean'], fp['statistics']['std_dev'], fp['statistics']['percentile_0.5'], 
            fp['statistics']['percentile_99.5'], fp['statistics']['min'], fp['statistics']['max'])
        html_content += "<img src='data:image/png;base64,{}'>".format(fp['center_slice_base64'])
        html_content += "<hr>"
    html_content += "</body></html>"
    return html_content

def run():
    mrc_list_path = get_args().mrcindexfile
    html_output = 'output.html'

    with open(mrc_list_path, 'r') as file:
        mrc_paths = file.read().splitlines()

    fingerprints = [compute_fingerprint(path) for path in mrc_paths]

    html_content = generate_html(fingerprints)

    with open(html_output, 'w') as f:
        f.write(html_content)

setup(
    group="kyleharrington",
    name="tomogram-fingerprint",
    version="0.0.1",
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
    ],
    run=run,
    dependencies={"environment_file": env_file},
)
