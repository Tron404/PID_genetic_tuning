import numpy as np

def cosine_sig(size):
    def compute_cosine_sig(amp, freq, phase, t):
        return amp*np.cos(2*np.pi*freq*t + phase*np.pi)
    
    sine = []
    inv = np.linspace(0, size, num=size)
    for time in inv:
        sine.append(compute_cosine_sig(1, 10, 0.0, time))

    return sine

def constant_sig(size):
    return np.full((size,), 1.0)

def custom_sig(size):
    sub_size = int(size/5)
    signal = []

    signal.append(np.full((sub_size,), 1.0+0.5))
    signal.append(np.full((sub_size,), 1.0+1))
    signal.append(np.full((sub_size,), 1.0+0.2))
    signal.append(np.full((sub_size,), 1.0-1.5))
    signal.append(np.full((sub_size,), 1.0-2))

    signal = np.concatenate(signal)

    return signal