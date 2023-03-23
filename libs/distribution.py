import numpy as np
from dotenv import load_dotenv
import os
load_dotenv()

ESTIMATED_BITS = int(os.getenv('ESTIMATED_BITS'))
N = 10**ESTIMATED_BITS

EPSILON = float(os.getenv('EPSILON'))
EPSILON_MIN = float(os.getenv('EPSILON_MIN'))
EPSILON_DECAY = float(os.getenv('EPSILON_DECAY'))

delta = EPSILON - EPSILON_MIN
weight_function = [EPSILON_MIN + delta * np.exp(-i / EPSILON_DECAY) for i in range(N)]

def MultiplyWeight(waf):
    index = int(waf * N) - N - 1
    return waf * weight_function[index]