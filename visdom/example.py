import visdom
import numpy as np
import torch

vis = visdom.Visdom(use_incoming_socket=True)
vis.image(torch.from_numpy(np.random.random((3,100,100))))
vis.text("Hello")
