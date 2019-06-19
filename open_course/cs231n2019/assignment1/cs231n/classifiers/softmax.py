from builtins import range
import numpy as np
from random import shuffle
from past.builtins import xrange

def softmax_loss_naive(W, X, y, reg):
    """
    Softmax loss function, naive implementation (with loops)

    Inputs have dimension D, there are C classes, and we operate on minibatches
    of N examples.

    Inputs:
    - W: A numpy array of shape (D, C) containing weights.
    - X: A numpy array of shape (N, D) containing a minibatch of data.
    - y: A numpy array of shape (N,) containing training labels; y[i] = c means
      that X[i] has label c, where 0 <= c < C.
    - reg: (float) regularization strength

    Returns a tuple of:
    - loss as single float
    - gradient with respect to weights W; an array of same shape as W
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)
    
    #############################################################################
    # TODO: Compute the softmax loss and its gradient using explicit loops.     #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization!                                                           #
    #############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    num_train = X.shape[0]
    for ind in range(num_train):
        x = X[ind]
        s = np.dot(x, W)
        s_exp = np.exp(s)
        pred = s_exp / np.sum(s_exp)
        loss += -1*np.log(pred[y[ind]])
        dW += np.dot(x.reshape(-1,1), pred.reshape(1,-1))
        dW[:,y[ind]] -= x
    loss /= num_train
    dW /= num_train
    loss += reg*np.sum(W*W)
    dW += 2*reg*W    
    
    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
    """
    Softmax loss function, vectorized version.

    Inputs and outputs are the same as softmax_loss_naive.
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)

    #############################################################################
    # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization!                                                           #
    #############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    num_train = X.shape[0]
    S = np.matmul(X, W)
    S_exp = np.exp(S)
    Pred = S_exp / np.sum(S_exp, axis=1).reshape(-1,1)
    Pred_log = -1 * np.log(Pred)
    onehot_y = np.zeros((num_train, W.shape[1]))
    onehot_y[np.arange(num_train), y] = 1
    loss = np.sum(Pred_log * onehot_y)
    loss /= num_train
    loss += reg*np.sum(W*W)

    dW = np.matmul(X.T, Pred)
    dW -= np.matmul(X.T, onehot_y)
    dW /= num_train
    dW += 2*reg*W
    
    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    return loss, dW
