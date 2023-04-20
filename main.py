from host.host_interface import HostInterface
from libs.history import History
import multiprocessing
from tqdm import tqdm
from dotenv import load_dotenv
import os
load_dotenv()

TRACE_LENGTH = int(os.getenv('TRACE_LENGTH'))

ESTIMATE_PERIOD = int(os.getenv('ESTIMATE_PERIOD'))
STRATEGY_TYPES = os.getenv('STRATEGY_TYPES')
GC_DISTRIBUTION_RESULT = os.getenv('GC_DISTRIBUTION_RESULT') 
WAF_DISTRIBUTION_RESULT = os.getenv('WAF_DISTRIBUTION_RESULT')
SIMULATE_PROGRESS_RESULT = os.getenv('SIMULATE_PROGRESS_RESULT')
CHANGE_RATIO_PROGRESS_RESULT = os.getenv('CHANGE_RATIO_PROGRESS_RESULT')
MA_PERIOD = int(os.getenv('MA_PERIOD'))
CHANGE_RATIO_REWARD = bool(int(os.getenv('CHANGE_RATIO_REWARD')))

def strategy(strategyType):
    hostInterface = HostInterface()
    hostInterface.SetStrategyType(strategyType)
    history = History()
    for i in tqdm(range(TRACE_LENGTH)):
        request, writeBytes = hostInterface.Step()
        if i % ESTIMATE_PERIOD == 0:
            hostInterface.EstimateStatus()
            if CHANGE_RATIO_REWARD and i >= MA_PERIOD * ESTIMATE_PERIOD:
                changeRatioReward = hostInterface.GetChangeRatioReward()
                history.AddChangeRatioReward(i, changeRatioReward)
            reward = hostInterface.GetReward()
            waf = hostInterface.GetWaf()
            freeSpaceRatio = hostInterface.GetFreeSpaceRatio()
            history.AddRewardAndWaf(i, reward, waf, freeSpaceRatio)
    history.ShowBlockWAFDistribution(f'{WAF_DISTRIBUTION_RESULT}/{strategyType}.png', hostInterface.GetDistributionCounter())
    history.ShowRewardAndWafHistory(f'{SIMULATE_PROGRESS_RESULT}/{strategyType}.png')
    history.ShowGCDistribution(f'{GC_DISTRIBUTION_RESULT}/{strategyType}.png', hostInterface.GetGCSuccessEpisodes())
    if CHANGE_RATIO_REWARD:
        history.ShowChangeRatioReward(f'{CHANGE_RATIO_PROGRESS_RESULT}/{strategyType}.png')

def main():
    strategyTypes = STRATEGY_TYPES.split(',')
    processes = []

    # Create a process for each strategy type and start it
    for strategyType in strategyTypes:
        process = multiprocessing.Process(target=strategy, args=(strategyType,))
        processes.append(process)
        process.start()

    # Wait for all the processes to finish
    for process in processes:
        process.join()

if __name__ == "__main__":
    main()