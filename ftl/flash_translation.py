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

class FlashTranslation:
    def __init__(self):
        self.dataCacheManage = DataCacheManage()
        self.nandController = NandController()
        self.addressTranslation = AddressTranslation()
        self.garbageCollection = GarbageCollection(self.nandController, self.addressTranslation)
    
    def GetBlockType(self, request):
        if ACTION_TYPE == 'All':
            action = ACTION_SPACE[0]
        elif ACTION_TYPE == 'Random':
            action = random.choice(ACTION_SPACE)
        elif ACTION_TYPE == 'Statistic':
            action = ACTION_SPACE[request.action]
        return action
    
    # return actual write bytes
    def Write(self, request):
        totalWriteBytes = 0
        self.dataCacheManage.WriteCache(request)
        writeType = self.GetBlockType(request)
        while True:
            # page 有可能是 1 ~ 4個lba
            page = self.dataCacheManage.GetCache()
            if not page: break
            lbas = ([self.addressTranslation[address] for address in page])
            programPage, writeBytes = self.nandController.Program(lbas, writeType)
            self.addressTranslation.Update(page, programPage)
            totalWriteBytes += writeBytes
        writeBytes, gcValid = self.garbageCollection.AutoCheck()
        totalWriteBytes += writeBytes
        return totalWriteBytes, gcValid