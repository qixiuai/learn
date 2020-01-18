
import os
import pdb
from datetime import datetime
import numpy as np
from absl import app as absl_app
from absl import logging

import tensorflow as tf

import data_pipeline
from metrics import SigmoidFocalClassificationLoss, f1score, precision, recall
from models.deepstagenet import DeepStageNet

from tensorflow.keras.callbacks import LambdaCallback
from ecg import Encoder, ECG



class PaiTask(object):

    def __init__(self, params):
        self.params = params
        params["num_parallel_calls"] = tf.data.experimental.AUTOTUNE
        self.test_ds = data_pipeline.test_input_fn(params)
        
    def predict(self, latest_checkpoint):
        params = self.params
        model = DeepStageNet(params)
        opt = tf.keras.optimizers.Adam(params["learning_rate"])
        model.compile(opt,
                      loss="binary_crossentropy",
                      #loss=SigmoidFocalClassificationLoss(gamma=0, alpha=None),
                      metrics=[f1score, tf.keras.metrics.Precision(), tf.keras.metrics.Recall(), "binary_accuracy"])
        
        ckpt = tf.train.Checkpoint(step=tf.Variable(0), net=model, optimizer=opt)
        #latest_checkpoint = "/home/guo/FlowTensor/tianchi/data/03 16:49:42/ckpt-739"
        ckpt.restore(latest_checkpoint)
        logging.info("Loaded checkpoint %s", latest_checkpoint)
        preds = model.predict(self.test_ds)
        return preds
        
    def submit(self):
        params = self.params
        logging.debug("Running FlowTensor with submit mode")
        #model_dir = params["model_dir"]
        #"ckpt-350", "ckpt-352"
        #model_dir = "/home/guo/FlowTensor/tianchi/data/" + '04 12:52:53' +"/ckpt-" #0.86 ckpt-399
        #model_dir = "/home/guo/Tianchi/data/" + '07 18:28:11' +"/ckpt-" #0.83-4
        #model_dir = "/home/guo/FlowTensor/tianchi/data/09 01:42:43/ckpt-" # leaderboard 0.9309
        #model_dir = "/home/guo/FlowTensor/tianchi/data/09 22:12:42/ckpt-"
        #model_dir = "/home/guo/FlowTensor/tianchi/data/" + "final2" + "/ckpt-"
        model_dir = "../user_data/" + "final" + "/ckpt-"
        #ckpts = [model_dir+str(i) for i in range(601, 633)]
        #ckpts = [model_dir+str(i) for i in range(601, 661)]
        #ckpts = [model_dir+str(i) for i in range(730, 741)]
        ckpts = [model_dir+str(i) for i in range(240, 307)]
        probs = []
        #num_model = len(ckpts)
        for ckpt in ckpts:
            prob = self.predict(ckpt)
            probs.append(prob)
        probs = np.stack(probs, axis=0)
        probs = np.median(probs, axis=0)
        test_ds = ECG("test")
        encoder = Encoder()
        samples = test_ds.samples_data
        #annos = test_ds.annotations
        results = {}
        for ind, sample_id in enumerate(samples):
            pred = probs[ind]
            names = []
            for id, p in enumerate(pred.tolist()):
                if p >= 0.5:
                    name = encoder.decode(id)
                    names.append(name)
            results[sample_id] = names

        in_file = open("../data/hf_round1_subB_noDup_rename.txt")
        #out = open("sub_86_all_data_continue_train_1830epochs.txt", "w")
        #out = open("sub_test_data_60ckpts_0.1lbsmoomthing_with_class_weights_307.txt", "w")
        out = open("../prediction_result/result.txt", "w")
        for line in in_file:
            line = line[:-1]
            record = line.strip().split("\t")
            id = record[0]
            names = results[id]
            out_line = line
            pred_str = "\t".join(names)
            if not names:
                out_line += '\t\n'
            else:
                out_line = out_line + "\t" + pred_str + "\t\n"
            out.write(out_line)
        in_file.close()
        out.close()


def main(_):
    params = {}
    params["batch_size"] = 256
    #params["model_dir"] = "/home/guo/FlowTensor/tianchi/data/" + datetime.now().strftime("%d %H:%M:%S")
    #params["model_dir"] = "/home/guo/FlowTensor/tianchi/data/" + "03 16:49:42"
    #params["model_dir"] = "/home/guo/FlowTensor/tianchi/data/07 21:16:37" # 
    params["model_dir"] = "../user_data/" + "final"
    params["learning_rate"] = 1e-3
    params["hidden_size"] = 64
    params["learning_rate_warmup_steps"] = 100
    task = PaiTask(params)
    task.submit()

if __name__ == "__main__":
    logging.set_verbosity(logging.DEBUG)
    absl_app.run(main)
