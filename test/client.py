
import numpy as np
import requests

from absl import app

import pdb


def main(unused_args):
    del unused_args
    signal = np.loadtxt("/home/guo/gitlab/test.txt", delimiter=',')
    #print("signal dur: {}".format(len(signal) / 500 / 60))
    server = True
    if server:
        #signal = ",".join(map(str, signal.tolist()))
        #print(signal.shape)
        signal = signal.tolist()
        resp = requests.post("http://47.110.8.224:5010", json={'signal':signal})
        print(resp.json())
    else:
        signal = signal[:500*30]
        list(map(obj.findpeaks, signal))
        #print(obj.peak_intervals)
    
if __name__ == '__main__':
    app.run(main)
