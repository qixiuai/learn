from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


import contextlib
import copy
import os
import sys

from tensor2tensor import models
from tensor2tensor import problems as problems_lib
from tensor2tensor.utils import mlperf_log
from tensor2tensor.utils import usr_dir
from tensor2tensor.utils import trainer_lib

import tensorflow as tf


def generate_data(problem, data_dir, tmp_dir):
    problem.generate_data(data_dir, tmp_dir)


@contextlib.contextmanager
def profile_context():
    with tf.contrib.tfprof.ProfileContext(
            "t2tprof", trace_steps=range(100), dump_steps=range(100)) as pctx:
        opts = tf.profiler.ProfileOptionBuilder.time_and_memory()
        pctx.add_audio_profiling("op", opts, range(100))
        yield

