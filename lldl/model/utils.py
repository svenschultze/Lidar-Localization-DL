import tensorflow as tf

def wrap_padding(pad_size):
    def layer(input_tensor):
        size = input_tensor.shape[1]
        tile_amount = tf.constant([1, 3, 1], tf.int32)
        tiled = tf.tile(input_tensor, tile_amount)
        padded = tiled[:,size - pad_size:pad_size - size]
        return padded

    return layer