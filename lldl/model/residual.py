import tensorflow as tf
from tensorflow.keras.layers import *
from tensorflow.keras.models import Model

from lldl.model.utils import wrap_padding

def resnet_block_1d(x, filters, kernel_size):
    c1 = Lambda(wrap_padding(int(kernel_size / 2)))(x)
    c1 = Conv1D(filters, kernel_size, use_bias=False)(c1)
    c1 = BatchNormalization()(c1)
    c1 = ReLU()(c1)

    c2 = Lambda(wrap_padding(int(kernel_size / 2)))(c1)
    c2 = Conv1D(filters, kernel_size, use_bias=False)(c2)
    c2 = BatchNormalization()(c2)
    c2 = Add()([x, c2])

    return ReLU()(c2)

def conv_block_1d(x, filters, kernel_size):
    c1 = Lambda(wrap_padding(int(kernel_size / 2)))(x)
    c1 = Conv1D(filters, kernel_size, use_bias=False)(c1)
    c1 = BatchNormalization()(c1)
    c1 = ReLU()(c1)

    c2 = Lambda(wrap_padding(int(kernel_size / 2)))(c1)
    c2 = Conv1D(filters, kernel_size, use_bias=False)(c2)
    c2 = BatchNormalization()(c2)
    return ReLU()(c2)

def build_model():
    x = input = Input((360,1))

    x = conv_block_1d(x, 16, 21)

    x = MaxPool1D(2)(x)
    x = resnet_block_1d(x, 16, 9)
    x = resnet_block_1d(x, 16, 9)
    x = resnet_block_1d(x, 16, 9)

    x = MaxPool1D(2)(x)
    x = conv_block_1d(x, 32, 9)
    x = resnet_block_1d(x, 32, 9)
    x = resnet_block_1d(x, 32, 9)

    x = MaxPool1D(2)(x)
    x = conv_block_1d(x, 64, 9)
    x = resnet_block_1d(x, 64, 9)
    x = resnet_block_1d(x, 64, 9)

    x = Flatten()(x)
    x = Dense(128, activation='relu')(x)
    x = Dense(64, activation='relu')(x)
    output = Dense(2)(x)
    return Model(inputs=input, outputs=output, name="residual_model")