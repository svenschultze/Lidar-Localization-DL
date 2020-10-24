import tensorflow as tf
from tensorflow.keras.layers import *
from tensorflow.keras.models import Sequential

from lldl.model.utils import wrap_padding

def build_model():
    return Sequential([
        Input((360,1)),
        Lambda(wrap_padding(4)),
        Conv1D(64, 9, activation='relu'),
        Lambda(wrap_padding(4)),
        Conv1D(64, 9, activation='relu'),
        MaxPool1D(2),
        Lambda(wrap_padding(4)),
        Conv1D(64, 9, activation='relu'),
        Lambda(wrap_padding(4)),
        Conv1D(64, 9, activation='relu'),
        MaxPool1D(2),
        Flatten(),
        Dense(128, activation='relu'),
        Dense(64, activation='relu'),
        Dense(2)
    ], name="shallow_model")