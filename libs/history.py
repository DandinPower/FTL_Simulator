import matplotlib.pyplot as plt
import numpy as np
from dotenv import load_dotenv
import os
load_dotenv()

WAF_AVERAGE_PERIOD = int(os.getenv('WAF_AVERAGE_PERIOD'))
NUMS_OF_PAGE_IN_BLOCK = int(os.getenv('NUMS_OF_PAGE_IN_BLOCK'))

class WAFHistory:
    def __init__(self):
        self.episodes = []
        self.writeBytes = []
        self.actualWriteBytes = []
        self.freeRatios = []
        self.wafEpisodes = []
        self.wafs = []
        self.wafFreeRatios = []
        self.gcValids = []

    def AddHistory(self, episode, writeByte, actualWriteByte, freeRatio):
        self.episodes.append(episode)
        self.writeBytes.append(writeByte)
        self.actualWriteBytes.append(actualWriteByte)
        self.freeRatios.append(freeRatio)

    # gc的那個block valid page的個數
    def AddGC(self, validNums):
        self.gcValids.append(validNums)

    def AddEstimateWAF(self, episode, tempWAF, freeRatio):
        self.wafEpisodes.append(episode)
        self.wafFreeRatios.append(freeRatio)
        self.wafs.append(tempWAF)

    def Finish(self, gc_count, gc_fail_count):
        if len(self.gcValids) != 0: actualWaf = sum([(lambda validNums: (validNums + NUMS_OF_PAGE_IN_BLOCK) / NUMS_OF_PAGE_IN_BLOCK)(validNums) for validNums in self.gcValids]) / len(self.gcValids)
        else: actualWaf = 0
        print(f'GC Count: {gc_count}')
        print(f'GC Fail Count: {gc_fail_count}')
        print(f'ActualWaf: {actualWaf}')

    @staticmethod
    def _moving_average(x_1, x_2, periods=WAF_AVERAGE_PERIOD):
        if len(x_1) < periods:
            return np.nan
        x = np.sum(x_2[-periods:]) / np.sum(x_1[-periods:])
        # print(np.sum(x_2[-periods:]), np.sum(x_1[-periods:]))
        print(f'Total WAF: {x}')
        return x

    def ShowHistory(self, path):
        ma_periods = WAF_AVERAGE_PERIOD
        ma = [self._moving_average(self.writeBytes, self.actualWriteBytes, periods=ma_periods) for self.writeBytes, self.actualWriteBytes in zip(np.array_split(self.writeBytes, len(self.writeBytes) / ma_periods), np.array_split(self.actualWriteBytes, len(self.actualWriteBytes) / ma_periods))]
        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()
        ax1.set_xlabel('X-axis Label')
        ax1.set_ylabel('WAF')
        ax2.set_ylabel('Free Space Ratio')
        ax1.plot(np.repeat(ma, ma_periods), label='WAF', color='red')
        ax2.plot(self.freeRatios, label='Free Space Ratio', color='blue')
        plt.title(f'Simulate Period: {ma_periods}')
        fig.legend(loc='upper right')
        plt.savefig(path)
        plt.clf()
    
    def ShowEstimateWAFHistory(self, path):
        plt.title(f'Estimate WAF')
        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()
        ax1.set_xlabel('Episodes')
        ax1.set_ylabel('WAF')
        ax1.set_ylim(0.8, 2.5)
        ax2.set_ylabel('Free Space Ratio')
        ax1.plot(self.wafEpisodes, self.wafs, label='WAF', color='red')
        ax2.plot(self.wafEpisodes, self.wafFreeRatios, label='Free Space Ratio', color='blue')
        fig.legend(loc='upper right')
        plt.savefig(path)
        plt.clf()