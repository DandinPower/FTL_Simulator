import matplotlib.pyplot as plt
import numpy as np
from dotenv import load_dotenv
import os
load_dotenv()

def DrawingDoubleCurve():
    ESTIMATED_BITS = int(os.getenv('ESTIMATED_BITS'))
    N = 10 ** ESTIMATED_BITS
    EPSILON = float(os.getenv('EPSILON'))
    EPSILON_RIGHT = float(os.getenv('EPSILON_RIGHT'))
    EPSILON_MIN = float(os.getenv('EPSILON_MIN'))
    EPSILON_DECAY = float(os.getenv('EPSILON_DECAY'))
    delta = EPSILON - EPSILON_MIN
    left = [EPSILON_MIN + delta * np.exp(-i / EPSILON_DECAY) for i in range(N//2)]
    delta_right = EPSILON_RIGHT - EPSILON_MIN
    right = [EPSILON_MIN + delta_right * np.exp(-i / EPSILON_DECAY) for i in range(N//2)]
    right.sort()
    left.extend(right)
    plt.plot(left)
    plt.savefig('test.png')

def DrawingWeightFunctionCurve():
    ESTIMATED_BITS = int(os.getenv('ESTIMATED_BITS'))
    N = 10**ESTIMATED_BITS
    EPSILON = float(os.getenv('EPSILON'))
    EPSILON_MIN = float(os.getenv('EPSILON_MIN'))
    EPSILON_DECAY = float(os.getenv('EPSILON_DECAY'))
    delta = EPSILON - EPSILON_MIN
    weight_function = [EPSILON_MIN + delta * np.exp(-i / EPSILON_DECAY) for i in range(N)]
    plt.plot(weight_function)
    plt.savefig('test.png')

def DrawingEstimatedWAFDistribution():
    x = [1.31, 1.27, 1.23, 1.21, 1.2, 1.19, 1.17, 1.33, 1.28, 1.25, 1.24, 1.16, 1.14, 1.18, 1.15, 1.13, 1.3, 1.45, 1.42, 1.41, 1.39, 1.37, 1.12, 1.35, 1.34, 1.7, 1.68, 1.66, 1.65, 1.64, 1.6, 1.57, 1.55, 1.54, 1.38, 1.26, 1.53, 1.52, 1.32, 1.51, 1.29, 1.22, 1.36, 1.5, 1.63, 1.62, 1.49, 1.59, 1.56, 1.69, 1.48, 1.47, 1.82, 1.81, 1.8, 1.44, 1.43, 1.78, 1.77, 1.4, 1.74, 1.71, 1.58, 1.67, 1.61, 1.46, 1.11, 1.95, 2.0, 1.94, 1.93, 1.92, 1.91, 1.89, 1.84, 1.83, 1.79, 1.88, 1.76, 1.75, 1.99, 1.9, 1.72, 1.1, 1.73, 1.87, 1.09, 1.08, 1.07, 1.06, 1.04, 1.03, 1.05, 1.01, 1.0, 1.02, 1.86, 1.98, 1.97, 1.96, 1.85]
    y = [1407, 3470, 10352, 16996, 15840, 21871, 75102, 2765, 2221, 2574, 3696, 114802, 76228, 43946, 67641, 26280, 3713, 1697, 1837, 1747, 3902, 5109, 30348, 2406, 3451, 201, 413, 1708, 452, 1588, 566, 2080, 2218, 3817, 4027, 2097, 1377, 2357, 2901, 4137, 3288, 10177, 3244, 4880, 1575, 1720, 3475, 702, 2124, 289, 2395, 2532, 202, 29, 113, 427, 2898, 129, 27, 3946, 372, 1344, 824, 110, 3147, 3793, 16037, 17, 6741, 94, 2914, 6, 329, 2028, 1581, 670, 39, 3878, 394, 147, 1381, 2757, 52, 3177, 1183, 1279, 6444, 132, 2415, 912, 6803, 6906, 3986, 75323, 259885, 35873, 3552, 11, 3151, 1, 156]
    # plot the bar chart
    plt.bar(x, y, width=0.005)
    # set the x-label and y-label
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    # show the plot
    plt.savefig('test.png')

def DrawingGCDistribution():
    x = [42169, 42256, 42431, 42575, 42721, 42889, 43084, 43302, 43425, 43854, 44025, 44261, 44380, 44507, 44594, 44755, 44915, 45095, 45234, 45390, 45586, 45816, 45962, 46453, 46596, 46856, 46997, 47206, 47483, 47680, 47928, 48101, 48254, 48489, 48701, 48905, 49133, 49276, 49517, 49559, 49733, 49960, 50158, 50333, 50473, 50681, 50882, 51078, 51243, 51329, 51484, 51621, 51781, 51982, 52148, 52325, 52451, 52733, 52923, 53228, 53440, 53594, 53715, 53896, 54059, 54181, 54404, 54562, 54751, 54920, 55130, 55303, 55476, 55641, 55788, 55937, 56135, 56296, 56406, 56555, 56779, 56980, 58621, 58892, 59346, 59566, 59838, 59983, 60207, 60535, 60848, 61077, 61274, 61602, 61884, 62162, 62329, 62504, 62593, 62725, 62889, 63019, 63287, 63482, 63684, 63855, 64044, 64211, 64452, 64707, 65062, 65252, 65455, 65695, 65862, 66040, 66136, 66293, 66468, 66604, 66820, 66934, 67012, 67277, 67590, 67728, 67967, 68128, 68289, 68952, 69111, 69213, 69457, 69699, 69960, 70149, 70292, 70464, 70676, 71002, 71225, 71497, 71734, 72026, 72246, 72547, 72844, 73049, 73251, 73431, 73550, 73834, 74127, 74510, 74783, 75285, 75547, 75757, 76149, 76535, 76669, 76956, 77160, 77359, 77592, 77829, 78012, 78611, 80020, 83702, 93730, 94101, 94396, 94478, 96042, 96100, 97246, 97488, 99614]
    plt.hist(x, width= 100, bins = len(x))
    # set the x-label and y-label
    plt.xlabel('Values')
    plt.ylabel('Frequency')
    plt.xlim(0, 100000)
    # show the plot
    plt.savefig('test.png')
    plt.clf()

if __name__ == "__main__":
    DrawingDoubleCurve()