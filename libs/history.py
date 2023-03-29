import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from dotenv import load_dotenv
import os
load_dotenv()

NUMS_OF_PAGE_IN_BLOCK = int(os.getenv('NUMS_OF_PAGE_IN_BLOCK'))
TRACE_LENGTH = int(os.getenv('TRACE_LENGTH'))

class History:
    def __init__(self):
        self.rewardWafEpisodes = []
        self.rewardWafFreeRatios = []
        self.rewards = []
        self.wafs = []

    def AddRewardAndWaf(self, episode, reward, waf, freeRatio):
        self.rewardWafEpisodes.append(episode)
        self.rewards.append(reward)
        self.wafs.append(waf)
        self.rewardWafFreeRatios.append(freeRatio)
    
    def ShowRewardAndWafHistory(self, path):
        # Assuming self.rewards and self.rewardWafEpisodes are lists of rewards and episodes
        # with the same length, and window_size is the number of episodes to use for the MA
        window_size = 500

        # Calculate the MA using Pandas
        ma_rewards = pd.Series(self.rewards).rolling(window_size, min_periods=1).mean()

        # Create the plot
        plt.title(f'Reward And WAF Progress')
        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()
        ax1.set_xlabel('Episodes')
        ax1.set_ylabel('Reward')
        ax2.set_ylabel('WAF')
        ax1.set_ylim(-12, 12)
        ax2.set_ylim(0.8, 2.5)
        # ax1.set_yscale('log')
        # Plot the reward and WAF data
        ax1.plot(self.rewardWafEpisodes, self.rewards, label='Reward', color='red')
        ax2.plot(self.rewardWafEpisodes, self.wafs, label='WAF', color='blue')

        # Plot the MA line
        ax1.plot(self.rewardWafEpisodes, ma_rewards, label=f'{window_size}-episode MA', color='green')

        # Add legend and save the plot
        fig.legend(loc='upper right')
        plt.savefig(path)
        plt.clf()

    def ShowBlockWAFDistribution(self, WAF_DISTRIBUTION, counter):
        x = list(counter.keys())
        x = [float(i) for i in x]
        y = list(counter.values())
        plt.bar(x, y, width=0.005)
        plt.xlabel("Estimated WAF")
        plt.ylabel("Times")
        plt.title("Estimated WAF Distribution")
        plt.savefig(WAF_DISTRIBUTION)
        plt.clf()
    
    def ShowGCDistribution(self, path, gcCounter):
        values = list(gcCounter.keys())
        counts = list(gcCounter.values())
        total = 0
        for count in counts: total += count
        plt.title(f'GC Distribution Count : {total}')
        plt.hist(values, weights=counts, width= 100, bins=len(values))
        plt.xlabel('Episodes')
        plt.xlim(0, TRACE_LENGTH)
        plt.ylabel('Counts')
        plt.savefig(path)
        plt.clf()