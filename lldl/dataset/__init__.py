import numpy as np
import io
import pkgutil

def load(name):
    x_file = pkgutil.get_data(__name__, f'data/{name}_x.npy')
    x = np.load(io.BytesIO(x_file))

    y_file = pkgutil.get_data(__name__, f'data/{name}_y.npy')
    y = np.load(io.BytesIO(y_file))

    return x, y

