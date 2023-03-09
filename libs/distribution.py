import numpy as np
from dotenv import load_dotenv
import os
load_dotenv()

N = 100

EPSILON = float(os.getenv('EPSILON'))
EPSILON_MIN = float(os.getenv('EPSILON_MIN'))
EPSILON_DECAY = float(os.getenv('EPSILON_DECAY'))

delta = EPSILON - EPSILON_MIN
weight_function = [EPSILON_MIN + delta * np.exp(-i / EPSILON_DECAY) for i in range(N)]

def MultiplyWeight(waf):
    index = int(waf * 100) - 100 - 1
    return (waf - 1) * weight_function[index] + 1