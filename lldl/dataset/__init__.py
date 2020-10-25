import numpy as np
import urllib.request
import io
from tqdm import trange
import time

def download(url):
    with urllib.request.urlopen(url) as r:
        length = int(r.getheader('content-length'))
        blocksize = length//10

        data = b''
        for x in trange(0, length + blocksize, blocksize):
            data += r.read(blocksize)

        return io.BytesIO(data)

datasets = ["gazebo", "gmapping", "synthetic_small_appartment", "synthetic_big_appartment", "synthetic_big_appartment_objects"]
def load(name):
    if name not in datasets:
        raise Exception(f"Dataset name must be one of {datasets}")

    print("Loading LiDAR data...")
    time.sleep(0.1)
    with download(f'http://dev.sschultze.de:9999/{name}_x.npy') as data:
        x = np.load(data)
    
    print("Loading coordinate data...")
    time.sleep(0.1)
    with download(f'http://dev.sschultze.de:9999/{name}_y.npy') as data:
        y = np.load(data)

    return x, y

