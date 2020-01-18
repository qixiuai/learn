
import os
import pdb
from datetime import datetime
import numpy as np
from absl import app as absl_app
from absl import logging

import tensorflow as tf

import data_pipeline
from metrics import SigmoidFocalClassificationLoss, f1score, precision, recall, BalancedFocalLoss, BalancedCrossEntropy
from models.deepstagenet import DeepStageNet

from tensorflow.keras.callbacks import LambdaCallback

import warnings
warnings.filterwarnings("ignore")

from get_prior import get_weights

class PaiTask(object):

    def __init__(self, params):
        self.params = params
        params["num_parallel_calls"] = tf.data.experimental.AUTOTUNE
        
    def train(self):
        params = self.params
        logging.debug("Running FlowTensor with train mode")
        model_dir = params["model_dir"]
        _ensure_dir(model_dir)
        
        #mirrored_strategy = tf.distribute.MirroredStrategy()
        #with mirrored_strategy.scope():
        model = DeepStageNet(params)
        opt = tf.keras.optimizers.Adam(params["learning_rate"])
        model.compile(opt,
                      #loss="binary_crossentropy",
                      #loss=tf.keras.losses.BinaryCrossentropy(label_smoothing=0.1),
                      loss=BalancedCrossEntropy(),
                      #loss=SigmoidFocalClassificationLoss(gamma=2.5, alpha=None),
                      #loss=BalancedFocalLoss(SigmoidFocalClassificationLoss(gamma=1.0, alpha=None)),
                      metrics=[f1score, tf.keras.metrics.Precision(), tf.keras.metrics.Recall(), "binary_accuracy"])
        
        ckpt = tf.train.Checkpoint(step=tf.Variable(0), net=model, optimizer=opt)
        manager = tf.train.CheckpointManager(ckpt, model_dir, max_to_keep=30000)
        latest_checkpoint = manager.latest_checkpoint
        #latest_checkpoint = "/home/guo/FlowTensor/tianchi/data/" + '04 12:52:53' + "/ckpt-399"
        #latest_checkpoint = "/home/guo/FlowTensor/tianchi/data/" + '09 22:12:42' + "/ckpt-715"
        if latest_checkpoint:
            ckpt.restore(latest_checkpoint)
            logging.info("Loaded checkpoint %s", latest_checkpoint)

        train_ds = data_pipeline.train_input_fn(params)
        valid_ds = data_pipeline.eval_input_fn(params)
        callbacks = []

        callbacks.append(
            tf.keras.callbacks.TensorBoard(
                log_dir=model_dir, histogram_freq=0, write_grads=False,
                write_images=False, embeddings_freq=0, update_freq="epoch"))
        """
        sfunc = optimizer.LearningRateFn(1e-1, 32, 30*37)
        scheduler_callback = optimizer.LearningRateScheduler(sfunc, verbose=0)
        callbacks.append(scheduler_callback)        
        """
        manager_callback = LambdaCallback(on_epoch_end=lambda epoch, logs: manager.save())
        callbacks.append(manager_callback)
        # learning rate scheduler
        def scheduler(epoch):
            lr = 1e-5 # 320 - 700
            if epoch <= 160: 
                lr = 1e-3 # 0 - 160
            elif epoch <= 320: 
                lr = 1e-4 # 160 - 320
            tf.print("learning_rate:", lr)
            return lr
        lr_scheduer = tf.keras.callbacks.LearningRateScheduler(scheduler)
        callbacks.append(lr_scheduer)
        start_epoch = opt.iterations.numpy()
        train_ds = train_ds.concatenate(valid_ds)
        #print(start_epoch)
        history = model.fit(train_ds,
                            #validation_data=valid_ds,
                            #validation_freq=2,
                            #initial_epoch=start_epoch,
                            shuffle=True,
                            epochs=310,
                            callbacks=callbacks,
                            workers=4,
                            use_multiprocessing=True,
                            verbose=1)
        return history

def _ensure_dir(log_dir):
    if not tf.io.gfile.exists(log_dir):
        tf.io.gfile.makedirs(log_dir)


def main(_):
    params = {}
    params["mode"] = "train"
    params["batch_size"] = 64
    #params["model_dir"] = "/home/guo/FlowTensor/tianchi/data/" + datetime.now().strftime("%d %H:%M:%S")
    #params["model_dir"] = "/home/guo/FlowTensor/tianchi/data/" + '03 22:27:15' val 0.85 leader: 0.8143
    #params["model_dir"] = "/home/guo/FlowTensor/tianchi/data/" + '04 12:52:53' #0.86 ckpt-399 leader: 0.829
    #params["model_dir"] = "/home/guo/FlowTensor/tianchi/data/" + '08 17:23:57' with data augmentation ~0.82
    #params["model_dir"] = "/home/guo/FlowTensor/tianchi/data/" + '09 01:42:43' best leaderboard
    #params["model_dir"] = "/home/guo/FlowTensor/tianchi/data/" + '09 22:12:42'
    #params["model_dir"] = "/home/guo/FlowTensor/tianchi/data/" + "final2" B board 0.8305
    params["model_dir"] = "../user_data/" + "final"
    params["learning_rate"] = 1e-3
    params["hidden_size"] = 64
    params["learning_rate_warmup_steps"] = 100
    task = PaiTask(params)
    task_mode = params["mode"]
    if task_mode == "train":
        task.train()
    elif task_mode == "submit":
        task.predict()
    else:
        raise ValueError("Invalid mode {}".format(task_mode))

if __name__ == "__main__":
    logging.set_verbosity(logging.DEBUG)
    absl_app.run(main)
