
import tensorflow as tf

from tensorflow.keras import Model, Sequential
from tensorflow.keras.layers import Layer, Dense, Conv1D, MaxPool1D, UpSamping1D
from tensorflow.keras.layers import BatchNormalization, Dropout


class Convolution(tf.keras.layers.Layer):

    def __init__(self, out_dim, kernel_size=3, strides=1,
                 with_bn=True, name="Convolution", padding="same"):
        super(Convolution, self).__init__(name=name)
        self._with_bn = with_bn
        self._conv = Conv1D(filters=out_dim, kernel_size=kernel_size, strides=strides,
                            padding=padding, use_bias=not with_bn)
        self._bn = BatchNormalization()

    def call(self, x):
        x = self._conv(x)
        if self._with_bn:
            x = self._bn(x)
        return tf.nn.relu(x)


class ConvBlock(tf.keras.layers.Layer):

    def __init__(self, num_out, padding="same"):
        self._conv1 = Conv1D(filters=int(num_out/2), kernel_size=1, strides=1, padding=padding)
        self._conv2 = Conv1D(filters=int(num_out/2), kernel_size=3, strides=1, padding=padding)
        self._conv3 = Conv1D(filters=num_out, kernel_size=1, strides=1, padding=padding)
        self._bn1 = BatchNormalization()
        self._bn2 = BatchNormalization()
        self._bn3 = BatchNormalization()

    def call(self, x):
        x = self._bn1(x)
        x = tf.nn.relu(x)
        x = self._conv1(x)
        x = self._bn2(x)
        x = tf.nn.relu(x)
        x = self._conv2(x)
        x = self._bn3(x)
        x = tf.nn.relu(x)
        x = self._conv3(x)
        return x


class SkipBlock(tf.keras.layers.Layer):

    def __init__(self, num_out):
        self._num_out = num_out

    def build(self, input_shape):
        num_out = self._num_out
        if input_shape[-1] == num_out:
            self.conv = None
        else:
            self.conv = Conv1D(filters=num_out, kernel_size=1, strides=1, padding="valid")

    def call(self, x):
        if self.conv:
            x = self.conv(x)
        return x


class ResidualBlock(tf.keras.layers.Layer):

    def __init__(self, num_out):
        self._conv_block = ConvBlock(num_out)
        self._skip = SkipBlock(num_out)

    def call(self, x):
        conv = self._conv_block(x)
        skip = self._skip(x)
        x = conv + skip
        return x


class Hourglass(tf.keras.Model):

    def __init__(self, n, num_out):
        self._up1 = ResidualBlock(num_out)
        self._low_down = MaxPool1D(pool_size=2, strides=2, padding="same")
        self._low1 = ResidualBlock(num_out)
        if n > 1:
            self._low2 = Hourglass(n-1, num_out)
        else:
            self._low2 = ResidualBlock(num_out)
        self._low3 = ResidualBlock(num_out)
        self._low_up = UpSamping1D(size=2)

        def call(self, x):
            up = self._up1(x)
            low_down = self._low_down(x)
            low1 = self._low1(low_down)
            low2 = self._low2(low1)
            low3 = self._low3(low2)
            low_up = self._low_up(low3)
            merge = tf.add_n([up, low_up])
            return merge


class Resnet(tf.keras.Model):
    pass

class SENet(tf.keras.Model):
    pass

class Inception(tf.keras.Model):
    pass

class DenseNet(tf.keras.Model):

    def __init__(self, params):
        pass

class HourglassNet(tf.keras.Model):

    def __init__(self, n, n_modules, layer):
        pass




    
