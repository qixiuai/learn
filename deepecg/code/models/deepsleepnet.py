
import tensorflow as tf
from tensorflow.keras.layers import Dense, Conv1D, MaxPooling1D
from tensorflow.keras.layers import Flatten, Dropout, BatchNormalization
from tensorflow.keras.layers import Concatenate
from tensorflow.python.ops.init_ops_v2 import he_normal, he_uniform
from tensorflow import initializers

from tensorflow.keras import Model
from tensorflow.keras import Sequential

class Conv1DBN(Model):

    def __init__(self,
                 filters=None,
                 kernel_size=None,
                 strides=1):
        super(Conv1DBN, self).__init__()
        self.conv1d = Conv1D(filters=filters,
                             kernel_size=kernel_size,
                             strides=strides,
                             padding="same", 
                             kernel_initializer=he_uniform(),
                             activation="linear",
                             use_bias=False)
        self.bn = BatchNormalization()

    def call(self, x):
        x = self.conv1d(x)
        x = self.bn(x)
        x = tf.nn.relu(x)
        return x


class LowFreqBlock(Model):

    def __init__(self):
        super(LowFreqBlock, self).__init__()
        self.conv1d_bn_1 = Conv1DBN(filters=64, kernel_size=400, strides=50)
        self.maxpooling1d_1 = MaxPooling1D(pool_size=4, strides=4, padding="same")
        self.dropout = Dropout(0.5)
        self.conv1d_bn_layers = [Conv1DBN(filters=128, kernel_size=6, strides=1) for _ in range(3)]
        self.maxpooling1d_2 = MaxPooling1D(pool_size=2, strides=2, padding="same")
        self.flatten = Flatten()

    def call(self, x):
        x = self.conv1d_bn_1(x)
        x = self.maxpooling1d_1(x)
        x = self.dropout(x)
        for conv1d_bn in self.conv1d_bn_layers:
            x = conv1d_bn(x)
        x = self.maxpooling1d_2(x)
        x = self.flatten(x)
        return x


class HighFreqBlock(Model):

    def __init__(self):
        super(HighFreqBlock, self).__init__()
        self.conv1d_bn_1 = Conv1DBN(filters=64, kernel_size=50, strides=6)
        self.maxpooling1d_1 = MaxPooling1D(pool_size=8, strides=8, padding="same")
        self.dropout = Dropout(0.5)
        self.conv1d_bn_layers = [Conv1DBN(filters=128, kernel_size=8, strides=1) for _ in range(3)]
        self.maxpooling1d_2 = MaxPooling1D(pool_size=4, strides=4, padding="same")
        self.flatten = Flatten()

    def call(self, x):
        x = self.conv1d_bn_1(x)
        x = self.maxpooling1d_1(x)
        x = self.dropout(x)
        for conv1d_bn in self.conv1d_bn_layers:
            x = conv1d_bn(x)
        x = self.maxpooling1d_2(x)
        x = self.flatten(x)
        return x


class DeepStageNet(Model):

    def __init__(self, params, name="deepstagenet"):
        super(DeepStageNet, self).__init__(name=name)
        self.params = params
        self.low_freq_block = LowFreqBlock()
        self.high_freq_block = HighFreqBlock()
        self.concatenate = Concatenate(axis=1)
        self.dropout = Dropout(0.5)
        self.softmax = tf.keras.layers.Dense(5)

    def call(self, x):
        low_freq = self.low_freq_block(x)
        high_freq = self.high_freq_block(x)
        freqs = self.concatenate([low_freq, high_freq])
        x = self.dropout(freqs)
        x = self.softmax(x)
        return x

if __name__ == '__main__':
    import pdb
    net = DeepStageNet()
    variables = net.trainable_variables
    print(variables)
    pdb.set_trace()
