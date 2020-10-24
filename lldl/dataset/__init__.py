import numpy as np
import urllib.request
import io

datasets = ["gazebo", "gmapping"]
def load(name):
    if name not in datasets:
        raise Exception(f"Dataset name must be one of {datasets}")

    with urllib.request.urlopen(f'https://github.com/svenschultze/Lidar-Localization-DL/blob/main/lldl/dataset/data/{name}_x.npy?raw=true') as f:
        x = np.load(io.BytesIO(f.read()))
    
    with urllib.request.urlopen(f'https://github.com/svenschultze/Lidar-Localization-DL/blob/main/lldl/dataset/data/{name}_y.npy?raw=true') as f:
        y = np.load(io.BytesIO(f.read()))

    return x, y

