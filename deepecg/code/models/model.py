
import tensorflow as tf
from pai.models.metrics import cross_entropy_loss
#from pai.models.deepsleepnet import DeepStageNet
from pai.models.deepstagenet import DeepStageNet
from pai.models.metrics import SigmoidFocalClassificationLoss
from pai.models.metrics import MetricLayer, MetricLayerF1


def create_model(params, is_train):
    with tf.name_scope("model"):
        if is_train:
            #inputs = tf.keras.layers.Input((6000,3), dtype="float32", name="inputs")
            inputs_signals = tf.keras.layers.Input((5000,12), dtype="float32", name="inputs_signals")
            inputs_anno = tf.keras.layers.Input((3,), dtype="float32", name="inputs_anno")
            targets = tf.keras.layers.Input((55,), dtype="float32", name="targets")
            #internal_model = BaseModel(params, name="base_model")
            internal_model = DeepStageNet(params, name="deepsleepnet")
            #probs = internal_model([inputs_signals, inputs_anno], training=is_train)
            probs = internal_model(inputs_signals, training=is_train)
            probs = MetricLayerF1()([probs, targets])
            probs = tf.keras.layers.Lambda(lambda x: x, name="probs", dtype=tf.float32)(probs)
            #model = tf.keras.Model([inputs,targets], logits)
            model = tf.keras.Model([inputs_signals, inputs_anno, targets], probs)
            #model.add_loss(cross_entropy_loss(logits, targets, 0.1, 55))
            #cce = tf.keras.losses.BinaryCrossentropy(reduction=tf.keras.losses.Reduction.NONE)
            #loss_fn = tf.nn.sigmoid_cross_entropy_with_logits
            loss_fn = SigmoidFocalClassificationLoss(alpha=None, reduction=tf.keras.losses.Reduction.NONE)
            loss = tf.nn.compute_average_loss(loss_fn(tf.reshape(probs, [-1]), tf.reshape(targets, [-1])), global_batch_size=params["batch_size"])
            model.add_loss(loss)
            return model
        else:
            inputs = tf.keras.layers.Input((6000,3), dtype="float32", name="inputs")
            #internal_model = BaseModel(params, name="base_model")
            internal_model = DeepStageNet(params, name="deepsleepnet")
            outputs = internal_model(inputs, training=is_train)
            return tf.keras.Model(inputs, outputs)



