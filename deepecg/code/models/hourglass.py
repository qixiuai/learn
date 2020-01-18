
import tensorflow as tf

from tensorflow.keras.layers import Conv1D, BatchNormalization, ReLu, Lambda
from tensorflow.keras.models import Sequential


class Convolution(tf.keras.layers.Layer):

    def __init__(self, name="Convolution", out_dim, kernel_size, strides=1, with_bn=True):
        super(Convolution, self).__init__(name=name)
        self.conv1d = Conv1D(filters=out_dim, kernel_size=kernel_size, strides=strides, padding="same", use_bias=not with_bn)
        self.bn = BatchNormalization()
        
    def call(self, x):
        x = self.conv1d(x)
        x = self.bn(x)
        return tf.nn.relu(x)


class Residual(tf.keras.layers.Model):

    def __init__(self, inp_dim, out_dim, strides=1):
        self.inp_dim = inp_dim
        self.out_dim = out_dim
        self.strides = strides
        
        self.conv1 = Convolution(out_dim=out_dim, kernel_size=3, strides=1, with_bn=True)
        self.conv2 = Conv1D(out_dim=out_dim, kernel_size=3, strides=1)
        self.bn = BatchNormalization()
        self.skip = Sequential([
            Conv1D(out_dim, kernel_size=1, strides=strides),
            BatchNormalization(),
        ] if self.inp_dim != self.out_dim else [])
        
    def get_config(self):
        return {
            "inp_dim": inp_dim,
            "out_dim": out_dim,
            "strides": strides,
            "with_bn": with_bn,
        }

    def call(self, x):
        conv1 = self.conv1(x)
        conv2 = self.conv2(x)
        bn = self.bn(conv2)
        skip = self.skip(x)
        return tf.nn.relu(bn + skip)


class Hourglass(tf.keras.layers.Model):

    def __init__(self):
        pass

class StageModel(tf.keras.layers.Model):

    def __init__(self):
        pass

    def build(self, input_shape):
        pass

    def get_config(self):
        return {}

    def call(self, inputs):
        pass
        
    
class Residual(tf.keras.layers.Model):

    def __init__(self, k, inp_dim, out_dim, stride=1, with_bn=True):
        super(Residual, self).__init__()

        self.conv1 = Conv1D(inp_dim, out_dim, (3,), padding=(1,), stride=(stride,), bias=False)
        self.bn1 = BatchNormalization(out_dim)
        self.relu1 = ReLu()

        self.conv2 = Conv1D(out_dim, out_dim, (3,), padding=(1,), bias=False)
        self.bn2 = BatchNormalization(out_dim)

        self.skip = Sequential(
            Conv1D(inp_dim, out_dim, (1,), stride=(stride,), bias=False),
            BatchNormalization(out_dim),
        ) if stride != 1 or inp_dim != out_dim else Sequential()

        self.relu = ReLu()

    def call(self, inputs):
        x = inputs
        conv1 = self.conv1(x)
        bn1 = self.bn1(conv1)
        relu1 = self.relu1(bn1)

        conv2 = self.conv2(relu1)
        bn2 = self.bn2(conv2)

        skip = self.skip(x)
        return self.relu(bn2 + skip)



    
class Hourglass(tf.keras.layers.Layer):

    def __init__(self):
        pass

    def build(self, input_shape):
        pass

    def call(self, inputs):
        return inputs






