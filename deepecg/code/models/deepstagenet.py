import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Dense, Conv1D, MaxPooling1D, Dropout
from tensorflow.keras.layers import Flatten, Dropout, BatchNormalization
from tensorflow.keras.layers import Concatenate
from tensorflow.python.ops.init_ops_v2 import he_normal, he_uniform
from tensorflow import initializers

from tensorflow.keras import Model
from tensorflow.keras import Sequential
from tensorflow.python.ops.init_ops_v2 import Initializer
from tensorflow.python.framework import dtypes

class Convolution(tf.keras.layers.Layer):

    def __init__(self, out_dim, kernel_size, strides=1, with_bn=True,  name="Convolution"):
        super(Convolution, self).__init__(name=name)
        self.conv1d = Conv1D(filters=out_dim, kernel_size=kernel_size, strides=strides, padding="same", use_bias=not with_bn)
        self.bn = BatchNormalization()
        
    def call(self, x):
        x = self.conv1d(x)
        x = self.bn(x)
        return tf.nn.relu(x)


class Residual(tf.keras.Model):

    def __init__(self, inp_dim, out_dim, strides=1):
        super(Residual, self).__init__()
        self.inp_dim = inp_dim
        self.out_dim = out_dim
        self.strides = strides

        self.conv1 = Convolution(out_dim=out_dim, kernel_size=3, strides=strides, with_bn=True)
        self.conv2 = Conv1D(filters=out_dim, kernel_size=3, strides=1, padding="same")
        self.bn = BatchNormalization()
        self.skip = Sequential([
            Conv1D(out_dim, kernel_size=1, strides=strides),
            BatchNormalization(),
        ] if strides != 1 or self.inp_dim != self.out_dim else [])

        self.dropout = Dropout(0.5)

    def get_config(self):
        return {
            "inp_dim": self.inp_dim,
            "out_dim": self.out_dim,
            "strides": self.strides,
        }

    def call(self, x):
        conv1 = self.conv1(x)
        conv2 = self.conv2(conv1)
        bn = self.bn(conv2)
        skip = self.skip(x)
        out = tf.nn.relu(bn + skip)
        out = self.dropout(out)
        return out


class HighFreqBlock(Model):

    def __init__(self):
        super(HighFreqBlock, self).__init__()
        ### best 1
        #self.conv = Conv1D(filters=32, kernel_size=7, strides=2)
        #self.conv1d_bn_layers = [Residual(inp_dim=64, out_dim=64, strides=2) for _ in range(8)]
        ### exper 1
        self.conv = Conv1D(filters=32*2, kernel_size=7, strides=2)
        #self.conv1d_bn_layers = [Residual(inp_dim=96, out_dim=96, strides=2) for _ in range(8)]
        #self.conv1d_bn_layers = [Residual(inp_dim=32*2*2+i*32, out_dim=32*2*2+(i+1)*32, strides=2) for i in range(8)]
        self.conv1d_bn_layers = [Residual(inp_dim=96, out_dim=96, strides=2) for i in range(8)]
        self.flatten = Flatten()

    def call(self, x):
        x = self.conv(x)
        for conv1d_bn in self.conv1d_bn_layers:
            x = conv1d_bn(x)
        x = self.flatten(x)
        return x

class LowFreqBlock(Model):

    def __init__(self):
        super(LowFreqBlock, self).__init__()
        ### best 1
        #self.conv = Conv1D(filters=32, kernel_size=7, strides=2)
        #self.conv1d_bn_layers = [Residual(inp_dim=64, out_dim=64, strides=2) for _ in range(8)]
        ### exper 1
        self.conv = Conv1D(filters=32*2, kernel_size=100, strides=6)
        self.conv1d_bn_layers = [Residual(inp_dim=96, out_dim=96, strides=2) for _ in range(8)]
        #self.conv1d_bn_layers = [Residual(inp_dim=32*2*2+i*32, out_dim=32*2*2+(i+1)*32, strides=2) for i in range(8)]
        self.flatten = Flatten()

    def call(self, x):
        x = self.conv(x)
        for conv1d_bn in self.conv1d_bn_layers:
            x = conv1d_bn(x)
        x = self.flatten(x)
        return x


class BiasPrior(Initializer):

    def __init__(self, dtype=dtypes.float32):
        self.dtype = dtype
        root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        prior = np.load(root+"/user_data/classes_prior.npy")
        self.log_prior = -np.log((1-prior) / prior)
        
    def __call__(self, shape, dtype=None):
        if dtype is None:
            dtype = self.dtype
        return tf.constant(self.log_prior, dtype=self.dtype)
            
    def get_config(self):
        return {"dtype": self.dtype.name}
    
class DeepStageNet(Model):

    def __init__(self, params, name="deepstagenet"):
        super(DeepStageNet, self).__init__(name=name)
        self.params = params
        self.high_freq_block = HighFreqBlock()
        self.low_freq_block = LowFreqBlock()
        #self.concatenate = Concatenate(axis=1)
        #self.softmax = tf.keras.layers.Dense(55, activation="sigmoid")
        self.softmax = tf.keras.layers.Dense(55, bias_initializer=BiasPrior, activation="sigmoid")
        #self.softmax = tf.keras.layers.Dense(55, activation="sigmoid")

    def call(self, inputs):
        x, anno = inputs
        high_freq = self.high_freq_block(x)
        low_freq = self.low_freq_block(x)
        high_freq = tf.concat([high_freq, low_freq, anno], 1)
        x = self.softmax(high_freq)
        return x

if __name__ == '__main__':
    import pdb
    net = DeepStageNet()
    variables = net.trainable_variables
    print(variables)
    pdb.set_trace()
