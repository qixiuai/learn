import pdb
import datetime
import tensorflow as tf

from tensorflow.keras.callbacks import Callback


class DebugCallback(Callback):

    def __init__(self):
        super(DebugCallback, self).__init__()
        
    def on_train_batch_begin(self, batch, logs=None):
        pass

    def on_train_batch_end(self, batch, logs=None):
        tf.print("in debug callbacks train batch end:")
        tf.print(self.model)
        try:
            tf.print(self.model.layers[-1].output)
        except:
            pass


    def on_epoch_begin(self, epoch, logs=None):
        pass

    def on_epoch_end(self, epoch, logs=None):
        pass
        #tf.print(self.model.layers[-1].output)
        #tf.print(self.model.layers[-1].output.shape)


        
