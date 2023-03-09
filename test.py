import matplotlib.pyplot as plt
import numpy as np
N = 100
EPSILON = 10
EPSILON_MIN = 1
EPSILON_DECAY = 11
delta = EPSILON - EPSILON_MIN
a = [EPSILON_MIN + delta * np.exp(-i / EPSILON_DECAY) for i in range(N)]

decay_rate = delta / (N - 1) # linear decay rate

a = [EPSILON - decay_rate * i for i in range(N)]

delta = EPSILON - EPSILON_MIN
a = [EPSILON_MIN + delta * np.exp(-i / EPSILON_DECAY) for i in range(N//2)]
b = [EPSILON_MIN + delta * np.exp(-i / EPSILON_DECAY) for i in range(N//2,-1,-1)]
a.extend(b)
plt.plot(a)
plt.savefig('test.png')
