
from tensorflow.keras.layers import Dense, Flatten
import tensorflow as tf



class BaseModel(tf.keras.Model):

    def __init__(self, params, name="base_model"):
        super(BaseModel, self).__init__(name)
        self.params = params

    def build(self, shape):
        del shape
        self.flatten = Flatten()
        self.dense = Dense(55, activation="sigmoid")
        
    def call(self, inputs):
        x = inputs[0]
        x = self.flatten(x)
        logits = self.dense(x)
        return logits

    def get_config(self):
        return {"params": ""}





