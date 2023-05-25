from host.host_interface import HostInterface
from libs.history import History
from libs.report import WriteReport
import multiprocessing
from tqdm import tqdm
from dotenv import load_dotenv
import os
load_dotenv()
import torch

TRACE_LENGTH = int(os.getenv('TRACE_LENGTH'))
TRACE_RUN_LENGTH = int(os.getenv('TRACE_RUN_LENGTH'))
ESTIMATE_PERIOD = int(os.getenv('ESTIMATE_PERIOD'))
STRATEGY_TYPES = os.getenv('STRATEGY_TYPES')
GC_DISTRIBUTION_RESULT = os.getenv('GC_DISTRIBUTION_RESULT') 
WAF_DISTRIBUTION_RESULT = os.getenv('WAF_DISTRIBUTION_RESULT')
SIMULATE_PROGRESS_RESULT = os.getenv('SIMULATE_PROGRESS_RESULT')
CHANGE_RATIO_PROGRESS_RESULT = os.getenv('CHANGE_RATIO_PROGRESS_RESULT')
MA_PERIOD = int(os.getenv('MA_PERIOD'))
CHANGE_RATIO_REWARD = bool(int(os.getenv('CHANGE_RATIO_REWARD')))
REPORT_RESULT = os.getenv('REPORT_RESULT')

MODEL_INDEX_START = int(os.getenv('MODEL_INDEX_START'))
MODEL_INDEX_END = int(os.getenv('MODEL_INDEX_END'))
MODEL_BASE_PATH = os.getenv('MODEL_BASE_PATH')

def strategy(strategyType):
    hostInterface = HostInterface()
    hostInterface.SetStrategyType(strategyType)
    history = History()
    for i in tqdm(range(TRACE_RUN_LENGTH)):
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
    if CHANGE_RATIO_REWARD:
        history.ShowChangeRatioReward(f'{CHANGE_RATIO_PROGRESS_RESULT}/{strategyType}.png')
    # write simulation report 
    gcCount = len(hostInterface.GetGCSuccessEpisodes().keys())
    rewardSum = hostInterface.GetTotalReward()
    coldCount, hotCount = hostInterface.GetColdHotCount()
    WriteReport(f'{REPORT_RESULT}/{strategyType}.txt', TRACE_RUN_LENGTH, gcCount, rewardSum, coldCount, hotCount)
    history.ShowBlockWAFDistribution(f'{WAF_DISTRIBUTION_RESULT}/{strategyType}.png', hostInterface.GetDistributionCounter())
    history.ShowRewardAndWafHistory(f'{SIMULATE_PROGRESS_RESULT}/{strategyType}.png')
    history.ShowGCDistribution(f'{GC_DISTRIBUTION_RESULT}/{strategyType}.png', hostInterface.GetGCSuccessEpisodes())

def PretrainStrategy(modelIndex, basicPath: str):
    print(f'Nowe evaluate on Model: {modelIndex}')
    hostInterface = HostInterface()
    hostInterface.flashTranslation.valueNet.qModel.load_state_dict(torch.load(basicPath.replace('modelIndex', f'{modelIndex}')))
    hostInterface.SetStrategyType('PreTrain')
    history = History()
    for i in tqdm(range(TRACE_RUN_LENGTH)):
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
    if CHANGE_RATIO_REWARD:
        history.ShowChangeRatioReward(f'{CHANGE_RATIO_PROGRESS_RESULT}/{modelIndex}.png')
    # write simulation report 
    gcCount = len(hostInterface.GetGCSuccessEpisodes().keys())
    rewardSum = hostInterface.GetTotalReward()
    coldCount, hotCount = hostInterface.GetColdHotCount()
    WriteReport(f'{REPORT_RESULT}/{modelIndex}.txt', TRACE_RUN_LENGTH, gcCount, rewardSum, coldCount, hotCount)
    history.ShowBlockWAFDistribution(f'{WAF_DISTRIBUTION_RESULT}/{modelIndex}.png', hostInterface.GetDistributionCounter())
    history.ShowRewardAndWafHistory(f'{SIMULATE_PROGRESS_RESULT}/{modelIndex}.png')
    history.ShowGCDistribution(f'{GC_DISTRIBUTION_RESULT}/{modelIndex}.png', hostInterface.GetGCSuccessEpisodes())
    
def main():
    strategyTypes = STRATEGY_TYPES.split(',')
    processes = []
    for strategyType in strategyTypes:
        process = multiprocessing.Process(target=strategy, args=(strategyType,))
        processes.append(process)
        process.start()
    for process in processes:
        process.join()

def MultiEvaluation():
    for modelIndex in range(MODEL_INDEX_START, MODEL_INDEX_END + 1):
        PretrainStrategy(modelIndex, MODEL_BASE_PATH)

if __name__ == "__main__":
    MultiEvaluation()
    # main()