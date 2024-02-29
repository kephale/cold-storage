###album catalog: cold-storage

from album.runner.api import setup, get_data_path, get_args


env_file = """name: tomotwin
channels:
  - nvidia
  - pytorch
  - rapidsai
  - conda-forge
  - defaults
dependencies:
  - python=3.10
  - pytorch[version='>=2.1']
  - torchvision
  - pandas[version='<2']
  - scipy
  - numpy
  - matplotlib
  - pytables
  - cuml=23.04
  - cuda-version=11.8
  - protobuf[version='>3.20']
  - tensorboard
  - optuna
  - mysql-connector-python
  - pip
  - pytorch-metric-learning
  - zarr
  - s3fs
  - aiobotocore
  - botocore
  - tqdm
  - pip:
      - tomotwin-cryoet
      - cryoet-data-portal
      - mrcfile
"""


def run():
    # Import necessary libraries
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    import numpy as np
    import zarr
    import os
    from tqdm import tqdm

    # Define the student model architecture within the run function
    class StudentModel(nn.Module):
        def __init__(self, output_channels=128):
            super(StudentModel, self).__init__()
            self.layer1 = StudentBlock(1, 32, stride=2)
            self.layer2 = StudentBlock(32, 64, stride=2)
            self.layer3 = StudentBlock(64, 128, stride=2)
            self.pool = nn.AdaptiveAvgPool3d((1, 1, 1))
            self.fc = nn.Linear(128, output_channels)

        def forward(self, x):
            x = self.layer1(x)
            x = self.layer2(x)
            x = self.layer3(x)
            x = self.pool(x)
            x = torch.flatten(x, 1)
            x = self.fc(x)
            return x

    class StudentBlock(nn.Module):
        def __init__(self, in_channels, out_channels, stride=1):
            super(StudentBlock, self).__init__()
            self.conv1 = nn.Conv3d(in_channels, out_channels, kernel_size=3, stride=stride, padding=1)
            self.bn1 = nn.BatchNorm3d(out_channels)
            self.relu = nn.ReLU(inplace=True)

        def forward(self, x):
            out = self.conv1(x)
            out = self.bn1(out)
            out = self.relu(out)
            return out

    # Load student model from checkpoint
    def load_student_model(checkpoint_path, device):
        student_model = StudentModel(output_channels=32)
        checkpoint = torch.load(checkpoint_path, map_location=device)
        student_model.load_state_dict(checkpoint['state_dict'])
        student_model.to(device)
        student_model.eval()
        return student_model

    def generate_embeddings(volume, model, device, window_size=37, stride=10, output_channels=32):
        Z, Y, X = volume.shape
        embeddings_shape = (Z, Y, X, output_channels)
        embeddings = np.zeros(embeddings_shape, dtype=np.float32)  # Initialize the embeddings array

        class VolumeDataset(torch.utils.data.Dataset):
            def __init__(self, volume, window_size, stride):
                self.volume = volume
                self.window_size = window_size
                self.stride = stride
                self.indices = self.compute_indices(volume.shape, window_size, stride)

            @staticmethod
            def compute_indices(volume_shape, window_size, stride):
                indices = []
                z_dim, y_dim, x_dim = volume_shape
                for z in range(0, z_dim - window_size + 1, stride):
                    for y in range(0, y_dim - window_size + 1, stride):
                        for x in range(0, x_dim - window_size + 1, stride):
                            indices.append((z, y, x))
                return indices

            def __len__(self):
                return len(self.indices)

            def __getitem__(self, idx):
                z, y, x = self.indices[idx]
                patch = self.volume[z:z+self.window_size, y:y+self.window_size, x:x+self.window_size]
                return torch.tensor(patch, dtype=torch.float32).unsqueeze(0), (z, y, x)  # Include coordinates

        dataset = VolumeDataset(volume, window_size, stride)
        dataloader = torch.utils.data.DataLoader(dataset, batch_size=32, shuffle=False)

        with torch.no_grad():
            for data, coords in tqdm(dataloader, desc="Generating embeddings", leave=False):
                data = data.to(device)
                output = model(data)
                embeddings_batch = output.cpu().numpy()

                for i, (z, y, x) in enumerate(coords):
                    embeddings[z:z+window_size, y:y+window_size, x:x+window_size, :] = embeddings_batch[i]

        return embeddings

    # Main logic for embedding generation and saving to Zarr
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # checkpoint_path = os.path.join(get_data_path(), "student_checkpoint_epoch_90.pth.tar")
    checkpoint_path = "/home/kyle.harrington/czii/experiments/tomotwin_distillation/checkpoints-tmp/student_checkpoint_epoch_90.pth.tar"
    student_model = load_student_model(checkpoint_path, device)

    zarr_input_path = get_args().zarrinput
    zarr_output_path = get_args().zarrembedding
    slices_str = get_args().slices
    slices = eval(slices_str)

    input_zarr = zarr.open(zarr_input_path, mode='r')
    volume = input_zarr[slices]

    embeddings = generate_embeddings(volume, student_model, device, window_size=37, stride=1)

    output_zarr = zarr.open(zarr_output_path, mode='w', shape=embeddings.shape, dtype=embeddings.dtype)
    output_zarr[:] = embeddings

    print("Embedding written to Zarr.")


setup(
    group="cellcanvas",
    name="create_embedding_zarr_student",
    version="0.0.3",
    title="Generate Embeddings with Student Model",
    description="Use a distilled student model to generate embeddings for a Zarr dataset.",
    solution_creators=["Kyle Harrington"],
    cite=[{
        "text": "Kyle Harrington for CellCanvas",
        "url": "https://cellcanvas.org"
    }],
    tags=["embeddings", "deep learning", "zarr"],
    license="MIT",
    album_api_version="0.5.1",    
    args=[
        {"name": "zarrinput", "type": "string", "required": True, "description": "Path to the input Zarr file."},
        {"name": "zarrembedding", "type": "string", "required": True, "description": "Path for the output Zarr embedding file."},
        {"name": "slices", "type": "string", "required": True, "description": "Slices for the region of interest, specified as a string, e.g., (slice(0,100), slice(0,100), slice(0,100))."},
    ],
    run=run,
    dependencies={"environment_file": env_file},
)
