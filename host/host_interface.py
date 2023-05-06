from .host_request_queue import HostRequestQueue, HostRequestQueueAction
from ftl.flash_translation import FlashTranslation
from dotenv import load_dotenv
import os
load_dotenv()

TRACE_PATH = os.getenv('TRACE_PATH')
TRACE_LENGTH = int(os.getenv('TRACE_LENGTH'))
START_POINT = int(os.getenv('START_POINT'))

class HostInterface: 
    def __init__(self):
        #self.hostRequestQueue = HostRequestQueue()
        self.episode = 0
        self.step = 0
        self.hostRequestQueueAction = HostRequestQueueAction()
        self.hostRequestQueueAction.LoadTrace(TRACE_PATH, TRACE_LENGTH)
        self.hostRequestQueueAction._idx = START_POINT
        self.flashTranslation = FlashTranslation()
        self.currentRequest = None

    # reset everything
    def Reset(self):
        self.flashTranslation.Reset()
        self.hostRequestQueueAction.Reset()
        self.episode = 0 
        self.step = 0
        self.currentRequest = self.hostRequestQueueAction.GetWriteRequest()
        return self.currentRequest

    # only reset flash translation and set environment for new episode
    def NewEpisode(self):
        self.flashTranslation.Reset()
        self.episode += 1
        self.step = 0
        self.currentRequest = self.hostRequestQueueAction.GetWriteRequest()
        return self.currentRequest

    # only work for testing strategy
    def SetStrategyType(self, strategyType):
        self.flashTranslation.SetStrategyType(strategyType)

    def GetFreeSpaceRatio(self):
        return self.flashTranslation.nandController.GetFreeSpaceRatio()

    def GetDistributionCounter(self):
        return self.flashTranslation.nandController.distributionCounter

    def GetGCSuccessEpisodes(self):
        return self.flashTranslation.garbageCollection.gcHistory.gcSuccessEpisodes        

    def EstimateStatus(self):
        self.flashTranslation.nandController.EstimateStatus()

    def GetReward(self):
        return self.flashTranslation.nandController.GetReward()

    def GetWaf(self):
        return self.flashTranslation.nandController.GetWaf()
    
    def GetChangeRatioReward(self):
        return self.flashTranslation.nandController.GetChangeRatioReward()

    # environment step for testing strategy
    def Step(self):
        writeRequest = self.hostRequestQueueAction.GetWriteRequest()
        totalWriteBytes = self.Fio(writeRequest)
        self.step += 1
        return writeRequest, totalWriteBytes

    def Fio(self, request):
        return self.flashTranslation.Write(request, self.step)
    
    # environment step for RL strategy
    def StepByAction(self, action):
        totalWriteBytes = self.FioByAction(self.currentRequest, action)
        self.step += 1
        self.currentRequest = self.hostRequestQueueAction.GetWriteRequest()
        self.EstimateStatus()
        reward = self.GetReward()
        return reward, self.currentRequest
    
    def FioByAction(self, request, action):
        return self.flashTranslation.WriteByAction(request, self.step, action)