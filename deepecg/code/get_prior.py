
import numpy as np
import data_pipeline

import plotly.graph_objs as go
from plotly.offline import plot

def prior():
    train_ds = data_pipeline.train_input_fn({"batch_size":512})
    valid_ds = data_pipeline.eval_input_fn({"batch_size":512})
    ds = train_ds.concatenate(valid_ds)
    annos = [y.numpy() for _, y in ds]
    anno = np.vstack(annos)
    return np.mean(anno, axis=0)

def get_weights():
    train_ds = data_pipeline.train_input_fn({"batch_size":512})
    valid_ds = data_pipeline.eval_input_fn({"batch_size":512})
    ds = train_ds.concatenate(valid_ds)
    annos = [y.numpy() for _, y in ds]
    anno = np.vstack(annos)
    return 1 / np.log(np.sum(anno, axis=0))


if __name__ == "__main__":
    p = prior()
    np.save("../user_data/classes_prior", p)
    w = get_weights()
    np.save("../user_data/classes_weights", w)
    #p.sort()
    #plot([go.Scatter(y=p,mode="markers+lines")])

