from .buffer.data_cache_manage import DataCacheManage
from .nand.block import BlockType
from .nand.nand_controller import NandController
from .address.address_translation import AddressTranslation
from .gc.garbage_collection import GarbageCollection
import random
from dotenv import load_dotenv
import os
load_dotenv()

NUMS_OF_LBA_IN_PAGE = int(os.getenv('NUMS_OF_LBA_IN_PAGE'))
ACTION_SPACE = [BlockType.COLD, BlockType.HOT]
ACTION_TYPE = os.getenv('ACTION_TYPE')
ACTIVE_GC_PERIOD = int(os.getenv('ACTIVE_GC_PERIOD'))

class FlashTranslation:
    def __init__(self):
        self.dataCacheManage = DataCacheManage()
        self.nandController = NandController()
        self.addressTranslation = AddressTranslation()
        self.garbageCollection = GarbageCollection(self.nandController, self.addressTranslation)
        self.strategyType = None

    def SetStrategyType(self, strategyType):
        self.strategyType = strategyType

    def GetBlockType(self, request):
        if self.strategyType == 'All':
            action = ACTION_SPACE[0]
        elif self.strategyType == 'Random':
            action = random.choice(ACTION_SPACE)
        elif self.strategyType == 'Statistic':
            action = ACTION_SPACE[request.action]
        return action
    
    # return actual write bytes
    def Write(self, request, episode):
        totalWriteBytes = 0
        self.dataCacheManage.WriteCache(request)
        writeType = self.GetBlockType(request)
        while True:
            page = self.dataCacheManage.GetCache()
            if not page: break
            lbas = ([self.addressTranslation[address] for address in page])
            programPage, writeBytes = self.nandController.Program(lbas, writeType)
            self.addressTranslation.Update(page, programPage)
            totalWriteBytes += writeBytes
        if episode % ACTIVE_GC_PERIOD == 0:
            totalWriteBytes += self.garbageCollection.AutoCheckByFullInvalid(episode)
        return totalWriteBytes