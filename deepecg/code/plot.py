
import numpy as np

import plotly.graph_objs as go
from plotly.offline import plot

from official.transformer.v2 import optimizer

def plot_learning_rate(lr=1e-1, hidden_size=32, warmup_steps=30*37):
    sfunc = optimizer.LearningRateFn(lr, hidden_size, warmup_steps)
    plot([go.Scatter(y=[sfunc(i) for i in range(37*500)])])


if __name__ == "__main__":
    plot_learning_rate()


