from .buffer.data_cache_manage import DataCacheManage
from .nand.block import BlockType
from .nand.nand_controller import NandController
from .address.address_translation import AddressTranslation
from .gc.garbage_collection import GarbageCollection
from .pretrain.value_net import ValueNet
import random
from dotenv import load_dotenv
import os
load_dotenv()

NUMS_OF_LBA_IN_PAGE = int(os.getenv('NUMS_OF_LBA_IN_PAGE'))
ACTION_SPACE = [BlockType.COLD, BlockType.HOT]
ACTION_TYPE = os.getenv('ACTION_TYPE')
ACTIVE_GC_PERIOD = int(os.getenv('ACTIVE_GC_PERIOD'))

class FlashTranslation:
    def __init__(self, hostInterface):
        self.hostInterface = hostInterface
        self.dataCacheManage = DataCacheManage()
        self.nandController = NandController()
        self.addressTranslation = AddressTranslation()
        self.garbageCollection = GarbageCollection(self.nandController, self.addressTranslation)
        self.valueNet = ValueNet()
        self.strategyType = None

    def Reset(self):
        self.dataCacheManage.Reset()
        self.nandController.Reset()
        self.addressTranslation.Reset()
        self.garbageCollection.Reset()

    # oonly work for testing strategy
    def SetStrategyType(self, strategyType):
        self.strategyType = strategyType

    # only work for testing strategy
    def GetBlockType(self, request):
        if self.strategyType == 'All':
            action = ACTION_SPACE[0]
        elif self.strategyType == 'Random':
            action = random.choices(ACTION_SPACE, weights = [1, 1], k = 1)
            action = action[0]
        elif self.strategyType == 'Statistic':
            action = ACTION_SPACE[request.action]
        elif self.strategyType == 'PreTrain':
            predict = self.valueNet.NewReq(request)
            action = ACTION_SPACE[predict]
        return action
    
    # return actual write bytes
    def Write(self, request, step):
        totalWriteBytes = 0
        self.dataCacheManage.WriteCache(request)
        writeType = self.GetBlockType(request)
        if writeType == BlockType.COLD:
            self.hostInterface.coldActionCount += 1
        else:
            self.hostInterface.hotActionCount += 1
        while True:
            page = self.dataCacheManage.GetCache()
            if not page: break
            lbas = ([self.addressTranslation[address] for address in page])
            programPage, writeBytes = self.nandController.Program(lbas, writeType)
            self.addressTranslation.Update(page, programPage)
            totalWriteBytes += writeBytes
        if step % ACTIVE_GC_PERIOD == 0:
            totalWriteBytes += self.garbageCollection.AutoCheckByFullInvalid(step)
        return totalWriteBytes
    
    # work for RL strategy
    def WriteByAction(self, request, step, action):
        totalWriteBytes = 0
        self.dataCacheManage.WriteCache(request)
        writeType = ACTION_SPACE[action]
        while True:
            page = self.dataCacheManage.GetCache()
            if not page: break
            lbas = ([self.addressTranslation[address] for address in page])
            programPage, writeBytes = self.nandController.Program(lbas, writeType)
            self.addressTranslation.Update(page, programPage)
            totalWriteBytes += writeBytes
        if step % ACTIVE_GC_PERIOD == 0:
            totalWriteBytes += self.garbageCollection.AutoCheckByFullInvalid(step)
        return totalWriteBytes