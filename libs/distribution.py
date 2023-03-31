import numpy as np
from dotenv import load_dotenv
import os
load_dotenv()

ESTIMATED_BITS = int(os.getenv('ESTIMATED_BITS'))
N = 10 ** ESTIMATED_BITS
EPSILON = float(os.getenv('EPSILON'))
EPSILON_RIGHT = float(os.getenv('EPSILON_RIGHT'))
EPSILON_MIN = float(os.getenv('EPSILON_MIN'))
EPSILON_DECAY = float(os.getenv('EPSILON_DECAY'))

def GetRewardFunction():
    delta = EPSILON - EPSILON_MIN
    left = [EPSILON_MIN + delta * np.exp(-i / EPSILON_DECAY) for i in range(N//2)]
    delta_right = EPSILON_RIGHT - EPSILON_MIN
    right = [EPSILON_MIN + delta_right * np.exp(-i / EPSILON_DECAY) for i in range(N//2)]
    right.sort()
    left.extend(right)
    return left

def MultiplyRewardFunction(waf):
    reward_function = GetRewardFunction()
    index = int(waf * N) - N - 1
    # return waf * reward_function[index]
    return reward_function[index]