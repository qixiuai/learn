import os
import pdb
import tensorflow as tf
import pandas as pd
import numpy as np
from tqdm import tqdm
from glob import glob
from absl import app
from absl import logging
from joblib import Parallel, delayed
from scipy.signal import resample, resample_poly

#data_dir = "/home/guo/ECGTianchi/data/"
data_dir = "../data/"

def get_signals(sample_path):
    df = pd.read_table(sample_path, sep=" ")
    df["III"] = df["II"] - df["I"]
    df["aVR"] = -(df["I"] + df["II"]) / 2
    df["aVL"] = df["I"] - df["II"] / 2
    df["aVF"] = df["II"] - df["I"] / 2
    return df.values

def get_annotations(label_path):
    annotations = {}
    encoder = Encoder()
    with open(label_path) as file:
        for line in file:
            record = line.strip().split("\t")
            id = record[0]
            if len(record) == 1:
                record.append("")
                record.append("")
            elif len(record) == 2:
                record.append("")
            else:
                pass
            age = record[1]
            if age == "":
                age = 47
                age = 0.5
            else:
                age = int(age)
                age = (age - 47) / 50
            sex = record[2]
            is_male = 1 if sex == "MALE" else 0
            is_female = 1 if sex == "FEMALE" else 0
            labels = record[3:]
            label_ids = [0 for i in range(55)]
            for lb in labels:
                label_id = encoder.encode(lb)
                label_ids[label_id]= 1
            annotations[id] = (age, is_male, is_female, label_ids)
    return annotations

class Encoder(object):

    def __init__(self):
        kclass_path = data_dir + "hf_round1_arrythmia.txt"
        self._name_id = {}
        self._id_name = {}
        id = 0
        with open(kclass_path) as file:
            for line in file:
                name = line.strip()
                self._name_id[name] = id
                self._id_name[id] = name
                id += 1
                
    def encode(self, name):
        return self._name_id[name]

    def decode(self, id):
        return self._id_name[id]


class ECG(object):

    def __init__(self, mode="train"):
        self.mode = mode
        self.train_dir = data_dir + "hf_round1_train/"
        self.valid_dir = data_dir + "hf_round1_testA/"
        self.test_dir = data_dir + "hf_round1_testB_noDup_rename/"
        self.label_path_train = data_dir + "hf_round1_label.txt"
        self.label_path_valid = data_dir + "heifei_round1_ansA_20191008.txt"
        self.label_path_test = data_dir + "hf_round1_subB_noDup_rename.txt"
        if mode == "train":
            self.data_dir = self.train_dir
            self.label_path = self.label_path_train
        elif mode == "minival":
            self.data_dir = self.valid_dir
            self.label_path = self.label_path_valid
        elif mode == "test":
            self.data_dir = self.test_dir
            self.label_path = self.label_path_test
        else:
            raise Exception("{} not supported".format(mode))

        self.annotations = self._extract_annotations()
        self.samples_data = self._extract_data()

    def _resample_sample(self, signals):
        data = [signals]
        if self.mode != "train":
            return data
        
        """
        def _resample(down):
            dt = []
            down_fns = [
                lambda x: resample(x, down),
                lambda x: resample_poly(x, up=500, down=down)
            ]
            resample(signals, )
        """
        data.append(resample(resample(signals, 6500), 5000))
        data.append(resample(resample(signals, 6000), 5000))
        data.append(resample(resample(signals, 5500), 5000))
        data.append(resample(resample(signals, 4500), 5000))
        data.append(resample(resample(signals, 4000), 5000))
        data.append(resample(resample(signals, 3500), 5000))
        return data
        
    def _extract_data(self):
        sample_paths = [self.data_dir + sample_id for sample_id in self.samples]
        data = {}
        logging.info("loading samples")
        def _read_sample(sample_path):
            signals = get_signals(sample_path)
            sample_id = os.path.basename(sample_path)
            return (sample_id, signals)
        samples = Parallel(n_jobs=-1, verbose=1)(delayed(_read_sample)(sample_path) for sample_path in sample_paths)
        for sample in samples:
            id = sample[0]
            signals = sample[1]
            #signals = (signals - np.mean(signals, axis=1, keepdims=True)) / (np.std(signals, axis=1, keepdims=True) + 1e-9)
            #signals = (signals - np.mean(signals, axis=1, keepdims=True))
            signals = signals - np.median(signals, axis=0)
            #data[id] = self._resample_sample(signals) if self.mode == "train" else [signals]
            data[id] = signals
        return data

    def _extract_annotations(self):
        logging.info("loading annotations")
        np.random.seed(1)
        annotations = get_annotations(self.label_path)
        samples = list(annotations.keys())
        np.random.shuffle(samples)
        """
        if self.mode == "train":
            ind = int(len(samples) * 0.8)
            self.samples = samples[:ind]
        elif self.mode == "minival":
            ind = int(len(samples) * 0.8)
            self.samples = samples[ind:]
        else:
            self.samples = samples
        """
        self.samples = samples
        return annotations

    def __call__(self):
        for sample in self.samples:
            signals = self.samples_data[sample]
            #data_ls = self._resample_sample(signals)
            data_ls = [signals]
            for data in data_ls:
                anno = self.annotations[sample]
                x = (data, anno[:-1])
                yield (x, anno[-1])

def split_dataset(_):
    label_path = data_dir + "hf_round1_label.txt"
    annotations = get_annotations(label_path)
    samples = list(annotations.keys())
    np.random.shuffle(samples)
    num_samples = len(samples)
    ind = int(num_samples*0.7)
    train_samples = samples[:ind]
    valid_samples = samples[ind:]


def main(_):
    #encoder = Encoder()
    #get_annotations(data_dir + "hf_round1_label.txt")
    train = ECG(mode="train")
    dataset = tf.data.Dataset.from_generator(
        train,
        output_types=((tf.float32, tf.float32), tf.int64),
        output_shapes=(((5000, 12),(3,)), (55,)))
    dataset = dataset.batch(2)
    for sample in dataset:
        print(sample)
        break

if __name__ == "__main__":
    #app.run(split_dataset)
    app.run(main)
