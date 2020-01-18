import os
import numpy as np
import tensorflow as tf

from tensorflow.python.keras import backend as K
from tensorflow.python.framework import ops
from tensorflow.python.framework import smart_cond
from tensorflow.python.ops import array_ops
from tensorflow.python.ops import math_ops


class SigmoidFocalClassificationLoss(tf.keras.losses.Loss):

    def __init__(self, gamma=2.0, alpha=0.25, **kwargs):
        super(SigmoidFocalClassificationLoss, self).__init__(**kwargs)
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        p = np.load(root+"/user_data/classes_weights.npy")
        self.weights = -np.log(p)
        self._gamma = gamma
        self._alpha = alpha

    def call(self, targets, preds):
        per_entry_corss_ent = tf.keras.backend.binary_crossentropy(targets, preds)
        if self.weights is not None:
            per_entry_corss_ent = per_entry_corss_ent * self.weights
        p_t = targets * preds + (1 - targets) * (1 - preds)
        modulating_factor = 1.0
        if self._gamma:
            modulating_factor = tf.pow(1.0 - p_t, self._gamma)
        alpha_weight_factor = 1.0
        if self._alpha is not None:
            alpha_weight_factor = (targets * self._alpha +
                                   (1 - targets) * (1 - self._alpha))
        focal_cross_entropy_loss = (modulating_factor * alpha_weight_factor *
                                    per_entry_corss_ent)
        return tf.reduce_mean(focal_cross_entropy_loss)


class BalancedFocalLoss(tf.keras.losses.Loss):

    def __init__(self, focal_loss_fn, **kwargs):
        super(BalancedFocalLoss, self).__init__(**kwargs)
        self.loss_fn = focal_loss_fn
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        p = np.load(root + "/user_data/classes_weights.npy")
        self.weights = -np.log(p)
        
        
    def call(self, targets, preds):
        losses = []
        for ind in range(55):
            loss = self.loss_fn(targets[:,ind], preds[:, ind])
            loss *= self.weights[ind]
            losses.append(loss)
        return tf.reduce_mean(losses)


def binary_crossentropy(y_true, y_pred, from_logits=False, label_smoothing=0):  # pylint: disable=missing-docstring
    y_pred = ops.convert_to_tensor(y_pred)
    y_true = math_ops.cast(y_true, y_pred.dtype)
    label_smoothing = ops.convert_to_tensor(label_smoothing, dtype=K.floatx())

    def _smooth_labels():
        return y_true * (1.0 - label_smoothing) + 0.5 * label_smoothing

    y_true = smart_cond.smart_cond(label_smoothing,
                                   _smooth_labels, lambda: y_true)
    return K.binary_crossentropy(y_true, y_pred, from_logits=from_logits)


class BalancedCrossEntropy(tf.keras.losses.Loss):

    def __init__(self):
        super(BalancedCrossEntropy, self).__init__()
        #self.cross_entropy = tf.keras.losses.BinaryCrossentropy(label_smoothing=0.1, reduction=tf.keras.losses.Reduction.NONE)
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        weights = np.load(root + "/user_data/classes_weights.npy")
        self.weights = weights
        
    def call(self, targets, preds):
        entropy = binary_crossentropy(targets, preds, label_smoothing=0.1)
        loss = entropy * self.weights
        return tf.reduce_mean(loss)


def accuracy(logits, labels):
    labels = tf.keras.backend.flatten(labels)
    outputs = tf.cast(tf.argmax(logits, axis=-1), tf.int32)
    labels = tf.cast(labels, tf.int32)
    return tf.reduce_mean(tf.cast(tf.equal(outputs, labels), tf.float32))

def single_class_accuracy(logits, labels, klass=0):
    labels = tf.keras.backend.flatten(labels)
    outputs = tf.cast(tf.argmax(logits, axis=-1), tf.int32)
    outputs = tf.cast(tf.equal(outputs, klass), tf.int32)
    labels = tf.cast(tf.equal(labels, klass), tf.int32)
    return tf.cast(tf.reduce_sum(tf.multiply(outputs, labels)), tf.float32) / (tf.cast(tf.reduce_sum(labels), tf.float32) - 1e-6)

def f1score(targets, preds):
    #preds = tf.nn.sigmoid(preds)
    #tf.print(preds[0], targets[0])
    preds = tf.cast(tf.greater_equal(preds, 0.5), tf.float32)
    targets = tf.cast(tf.greater_equal(targets, 0.5), tf.float32)
    num_preds = tf.reduce_sum(preds)
    num_truth = tf.reduce_sum(targets)
    preds = preds - 1 # (-1, 0)
    targets = targets * -1 + 1 # (1, 0)
    num_correct_pred = tf.reduce_sum(tf.cast(tf.equal(preds, targets), tf.float32)) 
    #tf.print("f1score:", num_correct_pred, num_preds, num_truth)
    p = num_correct_pred / (num_preds + 1e-5)
    r = num_correct_pred / (num_truth + 1e-5)
    return (2 * p * r) / (p + r)

def precision(targets, preds):
    preds = tf.nn.sigmoid(preds)
    preds = tf.cast(tf.greater_equal(preds, 0.5), tf.float32)
    targets = tf.cast(tf.greater_equal(targets, 0.5), tf.float32)
    num_preds = tf.reduce_sum(preds)
    preds = preds - 1 # (-1, 0)
    targets = targets * -1 + 1 # (1, 0)
    num_correct_pred = tf.reduce_sum(tf.cast(tf.equal(preds, targets), tf.float32))
    p = num_correct_pred / (num_preds + 1e-5)
    return p

def recall(targets, preds):
    preds = tf.nn.sigmoid(preds)
    preds = tf.cast(tf.greater_equal(preds, 0.5), tf.float32)
    targets = tf.cast(tf.greater_equal(targets, 0.5), tf.float32)
    num_truth = tf.reduce_sum(targets)
    preds = preds - 1 # (-1, 0)
    targets = targets * -1 + 1 # (1, 0)
    num_correct_pred = tf.reduce_sum(tf.cast(tf.equal(preds, targets), tf.float32))
    r = num_correct_pred / (num_truth + 1e-5)
    return r

