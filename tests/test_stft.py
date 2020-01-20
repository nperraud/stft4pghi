import sys
sys.path.append('../')

import numpy as np


from stft import GaussTF


def test_stft_different_length():
    a = 128
    M = 1024
    tfsystem = GaussTF(a,M)
    L = 128*1024
    x = np.random.rand(L)*2-1
    x = x/np.linalg.norm(x)
    x[:8*M] = 0
    x[-8*M:] = 0
    x2 = np.pad(x.copy(), L)[L:]
    X = tfsystem.dgt(x)
    xdot = tfsystem.idgt(X)
    X2 = tfsystem.dgt(x2)
    x2dot = tfsystem.idgt(X2)
    assert(np.linalg.norm(xdot-x)<1e-12)
    assert(np.linalg.norm(x2dot-x2)<1e-12)
    assert(np.sum(np.abs(X2[:, :X.shape[1]] - X))<1e-6)


def test_stft_different_a():
    a = 128
    M = 1024
    tfsystem = GaussTF(a,M)
    L = 128*1024
    x = np.random.rand(L)*2-1
    x = x/np.linalg.norm(x)
    X128 = tfsystem.dgt(x, a=128)
    X256 = tfsystem.dgt(x, a=256)
    assert(np.sum(np.abs(X256-X128[:,::2]))<1e-12)
    x256dot = tfsystem.idgt(X256, a=256)
    x128dot = tfsystem.idgt(X128, a=128)
    assert(np.linalg.norm(x128dot-x)<1e-12)
    assert(np.linalg.norm(x256dot-x)<1e-12)

if __name__ == "__main__":
    test_stft_different_length()
    test_stft_different_a()