import numpy as np
import urllib.request
import io
from tqdm import trange

def download(url):
    with urllib.request.urlopen(url) as r:
        length = int(r.getheader('content-length'))
        blocksize = length//10

        data = b''
        for x in trange(0, length + blocksize, blocksize):
            data += r.read(blocksize)

        return io.BytesIO(data)

datasets = ["gazebo", "gmapping"]
def load(name):
    if name not in datasets:
        raise Exception(f"Dataset name must be one of {datasets}")

    print("Loading LiDAR data...")
    with download(f'http://dev.sschultze.de:9999/{name}_x.npy') as buf:
        x = np.load(buf)
    
    print("Loading coordinate data...")
    with download(f'http://dev.sschultze.de:9999/{name}_y.npy') as buf:
        y = np.load(buf)

    return x, y

