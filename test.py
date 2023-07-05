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
    plt.savefig('reward_curve.png', dpi=300)

def DrawingWeightFunctionCurve():
    ESTIMATED_BITS = int(os.getenv('ESTIMATED_BITS'))
    N = 10**ESTIMATED_BITS
    EPSILON = float(os.getenv('EPSILON'))
    EPSILON_MIN = float(os.getenv('EPSILON_MIN'))
    EPSILON_DECAY = float(os.getenv('EPSILON_DECAY'))
    delta = EPSILON - EPSILON_MIN
    weight_function = [EPSILON_MIN + delta * np.exp(-i / EPSILON_DECAY) for i in range(N)]
    plt.plot(weight_function)
    plt.savefig('test.png', dpi=300)

def DrawingEstimatedWAFDistribution():
    x = [1.31, 1.27, 1.23, 1.21, 1.2, 1.19, 1.17, 1.33, 1.28, 1.25, 1.24, 1.16, 1.14, 1.18, 1.15, 1.13, 1.3, 1.45, 1.42, 1.41, 1.39, 1.37, 1.12, 1.35, 1.34, 1.7, 1.68, 1.66, 1.65, 1.64, 1.6, 1.57, 1.55, 1.54, 1.38, 1.26, 1.53, 1.52, 1.32, 1.51, 1.29, 1.22, 1.36, 1.5, 1.63, 1.62, 1.49, 1.59, 1.56, 1.69, 1.48, 1.47, 1.82, 1.81, 1.8, 1.44, 1.43, 1.78, 1.77, 1.4, 1.74, 1.71, 1.58, 1.67, 1.61, 1.46, 1.11, 1.95, 2.0, 1.94, 1.93, 1.92, 1.91, 1.89, 1.84, 1.83, 1.79, 1.88, 1.76, 1.75, 1.99, 1.9, 1.72, 1.1, 1.73, 1.87, 1.09, 1.08, 1.07, 1.06, 1.04, 1.03, 1.05, 1.01, 1.0, 1.02, 1.86, 1.98, 1.97, 1.96, 1.85]
    y = [1407, 3470, 10352, 16996, 15840, 21871, 75102, 2765, 2221, 2574, 3696, 114802, 76228, 43946, 67641, 26280, 3713, 1697, 1837, 1747, 3902, 5109, 30348, 2406, 3451, 201, 413, 1708, 452, 1588, 566, 2080, 2218, 3817, 4027, 2097, 1377, 2357, 2901, 4137, 3288, 10177, 3244, 4880, 1575, 1720, 3475, 702, 2124, 289, 2395, 2532, 202, 29, 113, 427, 2898, 129, 27, 3946, 372, 1344, 824, 110, 3147, 3793, 16037, 17, 6741, 94, 2914, 6, 329, 2028, 1581, 670, 39, 3878, 394, 147, 1381, 2757, 52, 3177, 1183, 1279, 6444, 132, 2415, 912, 6803, 6906, 3986, 75323, 259885, 35873, 3552, 11, 3151, 1, 156]
    # plot the bar chart
    plt.bar(x, y, width=0.005)
    # set the x-label and y-label
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    # show the plot
    plt.savefig('test.png', dpi=300)

def DrawingGCDistribution():
    counter = {402: 1, 960: 1, 1537: 1, 2175: 1, 2887: 1, 3672: 1, 5218: 1, 5779: 1, 6372: 1, 7108: 1, 7629: 1, 8222: 1, 8800: 1, 9420: 1, 10378: 1, 10456: 1, 10963: 1, 11542: 1, 12105: 1, 12928: 1, 13394: 1, 13967: 1, 14533: 1, 15105: 1, 15744: 1, 16335: 1, 16921: 1, 17493: 1, 18075: 1, 19127: 1, 19131: 1, 19660: 1, 20232: 1, 21797: 1, 22374: 1, 23014: 1, 23601: 1, 24207: 1, 24797: 1, 25489: 1, 26196: 1, 26649: 1, 27265: 1, 27814: 1, 28449: 1, 29039: 1, 29784: 1, 29960: 1, 30262: 1, 31455: 1, 31740: 1, 33909: 1, 34631: 1, 35264: 1, 35817: 1, 36397: 1, 36979: 1, 37632: 1, 38297: 1, 38419: 1, 38861: 1, 39453: 1, 40021: 1, 40794: 1, 41306: 1, 41868: 1, 42466: 1, 42998: 1, 43026: 1, 43688: 1, 44274: 1, 44590: 1, 44829: 1, 44846: 1, 45210: 1, 45426: 1, 45966: 1, 46474: 1, 46966: 1, 47003: 1, 47627: 1, 48201: 1, 48220: 1, 48789: 1, 49144: 1, 49436: 1, 49712: 1, 50110: 1, 50679: 1, 50813: 1, 51257: 1, 51402: 1, 51877: 1, 52279: 1, 52434: 1, 53221: 1, 53568: 1, 53731: 1, 54181: 1, 54310: 1, 54882: 1, 55246: 1, 55474: 1, 55792: 1, 56110: 1, 56658: 1, 56731: 1, 57918: 1, 58087: 1, 59605: 1, 59905: 1, 59984: 1, 60205: 1, 61113: 1, 61522: 1, 61870: 1, 62392: 1, 62585: 1, 62974: 1, 62992: 1, 63565: 1, 64145: 1, 64170: 1, 64804: 1, 65272: 1, 65433: 1, 66028: 1, 66102: 1, 66413: 1, 66629: 1, 66680: 1, 67012: 1, 67201: 1, 67959: 1, 67960: 1, 68291: 1, 69345: 1, 69622: 1, 69939: 1, 70153: 1, 70499: 1, 71115: 1, 71225: 1, 71704: 1, 72304: 1, 72721: 1, 72908: 1, 73431: 1, 73453: 1, 74142: 1, 74685: 1, 74757: 1, 75006: 1, 76137: 1, 76580: 1, 77183: 1, 77265: 1, 77710: 1, 78257: 1, 78682: 1, 78899: 1, 79488: 1, 80057: 1, 80656: 1, 81206: 1, 82033: 1, 82513: 1, 83084: 1, 83685: 1, 84261: 1, 84887: 1, 85531: 1, 86056: 1, 86631: 1, 87191: 1, 87989: 1, 88493: 1, 89066: 1, 89217: 1, 89642: 1, 90230: 1, 91036: 1, 91582: 1, 92114: 1, 92700: 1, 93275: 1, 93966: 1, 94077: 1, 94403: 1, 94653: 1, 95231: 1, 95804: 1, 96317: 1, 96400: 1, 97054: 1, 97634: 1, 98215: 1, 98781: 1, 99672: 1, 99860: 1, 99995: 1, 100033: 1, 100735: 1, 101260: 1, 101839: 1, 102422: 1, 103013: 1, 103652: 1, 104231: 1, 104830: 1, 105403: 1, 106079: 1, 106757: 1, 107248: 1, 108504: 1, 108703: 1, 109227: 1, 109825: 1, 110423: 1, 111074: 1, 111648: 1, 112224: 1, 112920: 1, 113005: 1, 113516: 1, 114055: 1, 114666: 1, 115238: 1, 115448: 1, 115904: 1, 116556: 1, 117153: 1, 117841: 1, 118394: 1, 118651: 1, 119164: 1, 119752: 1, 120289: 1, 120887: 1, 121196: 1, 121447: 1, 122045: 1, 122669: 1, 122962: 1, 123263: 1, 123849: 1, 124406: 1, 125177: 1, 125692: 1, 126201: 1, 126261: 1, 126843: 1, 127430: 1, 127607: 1, 128059: 1, 128663: 1, 128916: 1, 129560: 1, 130150: 1, 130451: 1, 130836: 1, 131709: 1, 131759: 1, 132311: 1, 132904: 1, 132917: 1, 133484: 1, 134086: 1, 134691: 1, 136153: 1, 136719: 1, 136777: 1, 137338: 1, 138102: 1, 139094: 1, 139331: 1, 139776: 1, 139887: 1, 140511: 1, 141095: 1, 141218: 1, 141685: 1, 142307: 1, 143089: 1, 143578: 1, 145262: 1, 145338: 1, 145905: 1, 147866: 1, 148118: 1, 148284: 1, 148418: 1, 148688: 1, 149867: 1, 150294: 1, 150973: 1, 151364: 1, 151543: 1, 152121: 1, 152765: 1, 152784: 1, 153358: 1, 153933: 1, 154507: 1, 154557: 1, 155156: 1, 155513: 1, 155841: 1, 156013: 1, 156724: 1, 157291: 1, 157863: 1, 158460: 1, 158994: 1, 159144: 1, 159730: 1, 160323: 1, 160936: 1, 161487: 1, 161931: 1, 162169: 1, 162782: 1, 163368: 1, 163558: 1, 164078: 1, 164635: 1, 165252: 1, 165878: 1, 166494: 1, 167075: 1, 167642: 1, 168292: 1, 168325: 1, 169074: 1, 169844: 1, 169923: 1, 170386: 1, 170414: 1, 170470: 1, 171113: 1, 171290: 1, 171321: 1, 171887: 1, 172509: 1, 173464: 1, 173528: 1, 173661: 1, 174001: 1, 174056: 1, 174539: 1, 174641: 1, 175307: 1, 175532: 1, 175636: 1, 175650: 1, 175967: 1, 176164: 1, 176187: 1, 176220: 1, 176254: 1, 176269: 1, 176358: 1, 176375: 1, 176843: 1, 177091: 1, 177185: 1, 177711: 1, 178282: 1, 178868: 1, 179487: 1, 180081: 1, 180192: 1, 180683: 1, 181060: 1, 181293: 1, 181838: 1, 182533: 1, 183179: 1, 183808: 1, 184385: 1, 184954: 1, 185567: 1, 186157: 1, 186746: 1, 187353: 1, 187907: 1, 188236: 1, 188732: 1, 188734: 1, 189208: 1, 189763: 1, 190368: 1, 190932: 1, 191608: 1, 191694: 1, 192224: 1, 192747: 1, 193316: 1, 193915: 1, 194008: 1, 194675: 1, 195091: 1, 195191: 1, 195759: 1, 196344: 1, 196979: 1, 197055: 1, 197750: 1, 198236: 1, 198791: 1, 199371: 1, 199552: 1, 199943: 1}
    values = list(counter.keys())
    counts = list(counter.values())
    total = 0
    for count in counts: total += count
    plt.title(f'GC Distribution Count : {total}')
    plt.hist(values, weights=counts, width= 400, bins=len(values))
    plt.xlabel('Episodes')
    plt.xlim(0, 200000)
    plt.ylabel('Counts')
    plt.savefig('test2.png', dpi=300)
    plt.clf()

def WriteReport(path, length, gcCount, rewardSum, coldCount, hotCount):
    report = f'Simulation Report\n'
    report += '-' * 35 + '\n'
    report += '{:35s} {:20d}\n'.format('Simulate Length:', length)
    report += '{:35s} {:20d}\n'.format('Total Gc Times:', gcCount)
    report += '{:35s} {:20.2f}\n'.format('Total Reward:', rewardSum)
    report += '{:35s} {:20d}\n'.format('Cold Action Count:', coldCount)
    report += '{:35s} {:20d}\n'.format('Hot Action Count:', hotCount)
    report += '{:35s} {:20.2f}\n'.format('Cold Action Ratio:', (coldCount / length))
    report += '{:35s} {:20.2f}\n'.format('Hot Action Ratio:', (hotCount / length))
    with open(path, 'w') as file:
        file.write(report)

def test_quantization():
    import torch
    import torch.nn as nn
    import torch.quantization as quantization

    # Define a simple class model
    class MyModel(nn.Module):
        def __init__(self):
            super(MyModel, self).__init__()
            self.fc = nn.Linear(10, 1)

        def forward(self, x):
            return self.fc(x)

    # Create a random float32 tensor as input
    input_tensor = torch.randn(1, 10)
    # Create an instance of the model
    model = MyModel()

    # Perform a forward pass to initialize the model's parameters
    output_tensor = model(input_tensor)

    # Convert the model to qint8 format using quantization
    quantized_model = quantization.QuantWrapper(model)
    quantized_model.qconfig = quantization.default_qconfig
    quantized_model = quantization.quantize_dynamic(quantized_model, {nn.Linear}, dtype=torch.qint8)

    # Perform a forward pass with the quantized model and input tensor
    output_tensor_qint8 = quantized_model(input_tensor)
    # Print the original output and quantized output
    print("Original Output:\n", output_tensor)
    print("Quantized Output:\n", output_tensor_qint8.dequantize().to(torch.float))

if __name__ == "__main__":
    # DrawingDoubleCurve()
    WriteReport('test.txt', 100000, 243, 122308.15021111527, 19399, 80601)