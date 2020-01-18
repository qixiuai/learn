
import os
import tensorflow as tf

from absl import logging
from absl import app as absl_app

from plotly.offline import plot
import plotly.graph_objs as go

import sys
sys.path.append("/home/guo/ECGTianchi/dataset")
from ecg import ECG

_READ_RECORD_BUFFER = 8 * 1000 * 1000


def train_input_fn(params):
    batch_size = params["batch_size"]
    dataset = tf.data.Dataset.from_generator(
        ECG(mode="train"),
        output_types=((tf.float32, tf.float32), tf.float32),
        output_shapes=(((5000, 12), (3,)), (55,)),
    )
    dataset = dataset.batch(batch_size, drop_remainder=False)
    return dataset

def eval_input_fn(params):
    batch_size = params["batch_size"]
    dataset = tf.data.Dataset.from_generator(
        ECG(mode="minival"),
        output_types=((tf.float32, tf.float32), tf.float32),
        output_shapes=(((5000, 12), (3,)), (55,)),
    )
    dataset = dataset.batch(batch_size, drop_remainder=False)
    return dataset

def test_input_fn(params):
    batch_size = params["batch_size"]
    dataset = tf.data.Dataset.from_generator(
        ECG(mode="test"),
        output_types=((tf.float32, tf.float32), tf.float32),
        output_shapes=(((5000, 12), (3,)), (55,)),
    )
    dataset = dataset.batch(batch_size, drop_remainder=False)
    return dataset


def main(_):
    params = {}
    params["batch_size"] = 64
    params["num_parallel_calls"] = 12
    params["repeat_dataset"] = 1
    dataset = train_input_fn(params)
    for input in dataset:
        (x, y) = input
        print(x.shape,y.shape)


if __name__ == "__main__":
    absl_app.run(main)
