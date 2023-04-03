from .host_request_queue import HostRequestQueue, HostRequestQueueAction
from ftl.flash_translation import FlashTranslation
from dotenv import load_dotenv
import os
load_dotenv()

TRACE_PATH = os.getenv('TRACE_PATH')
TRACE_LENGTH = int(os.getenv('TRACE_LENGTH'))

class HostInterface:
    def __init__(self):
        #self.hostRequestQueue = HostRequestQueue()
        self.episode = 0
        self.step = 0
        self.hostRequestQueueAction = HostRequestQueueAction()
        self.hostRequestQueueAction.LoadTrace(TRACE_PATH, TRACE_LENGTH)
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

    def GetRewardAndWAF(self):
        return self.flashTranslation.nandController.GetRewardAndWAF()
    
    def UpdateBlockWAFDistribution(self):
        self.flashTranslation.nandController.UpdateBlockWAFDistribution()

    def GetDistributionCounter(self):
        return self.flashTranslation.nandController.distributionCounter

    def GetGCSuccessEpisodes(self):
        return self.flashTranslation.garbageCollection.gcHistory.gcSuccessEpisodes        

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
        reward, waf = self.GetRewardAndWAF()
        return reward, self.currentRequest
    
    def FioByAction(self, request, action):
        return self.flashTranslation.WriteByAction(request, self.step, action)