import numpy as np
from dotenv import load_dotenv
import os
import math
load_dotenv()

ESTIMATED_BITS = int(os.getenv('ESTIMATED_BITS'))
N = 10 ** ESTIMATED_BITS
EPSILON = float(os.getenv('EPSILON'))
EPSILON_RIGHT = float(os.getenv('EPSILON_RIGHT'))
EPSILON_MIN = float(os.getenv('EPSILON_MIN'))
EPSILON_DECAY = float(os.getenv('EPSILON_DECAY'))

PENALTY_BASE = float(os.getenv('PENALTY_BASE'))
PENALTY_ALPHA = float(os.getenv('PENALTY_ALPHA'))

delta = EPSILON - EPSILON_MIN
reward_function = [EPSILON_MIN + delta * np.exp(-i / EPSILON_DECAY) for i in range(N//2)]
delta_right = EPSILON_RIGHT - EPSILON_MIN
right = [EPSILON_MIN + delta_right * np.exp(-i / EPSILON_DECAY) for i in range(N//2)]
right.sort()
reward_function.extend(right)

def MultiplyRewardFunction(waf):
    index = int(waf * N) - N - 1
    reward = reward_function[index] 
    return reward

def MultiplyPenalty(reward, penaltyCount):
    # original 
    # return reward * (1 / (1 + PENALTY_ALPHA * penaltyCount))
    # log
    return reward * (1 / (1 + PENALTY_ALPHA * math.pow(PENALTY_BASE, penaltyCount)))
