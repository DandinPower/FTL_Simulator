from ..nand.block import BlockType
from collections import Counter
from dotenv import load_dotenv
import os
load_dotenv()

AUTO_GC_RATIO = float(os.getenv('AUTO_GC_RATIO'))
NUMS_OF_PAGE_IN_BLOCK = int(os.getenv('NUMS_OF_PAGE_IN_BLOCK'))

class GCHistory:
    def __init__(self) -> None:
        self.gcSuccessEpisodes = Counter()
        self.gcFailEpisodes = Counter()
    
    def Success(self, episode):
        self.gcSuccessEpisodes.update([episode])
    
    def Fail(self, episode):
        self.gcFailEpisodes.update([episode])

class GarbageCollection:
    def __init__(self, nandController, addressTranslation):
        self.nandController = nandController
        self.addressTranslation = addressTranslation
        self.gcHistory = GCHistory()
        
    # use in passive gc, it will only run when free space is less than setting free ratio -- version 1
    # when there is an full invalid block do garbage collection, besides don't do -- version 2
    def AutoCheckByFullInvalid(self, episode):
        fullInvalidsBlockIdxs = self.nandController.GetFullInvalidBlock()
        if fullInvalidsBlockIdxs:
            totalWriteBytes = 0
            for blockIdx in fullInvalidsBlockIdxs:
                try:
                    totalWriteBytes += self.Run(blockIdx)
                    self.gcHistory.Success(episode)
                except:
                    self.gcHistory.Fail(episode)
            return totalWriteBytes
        else:
            return 0
        
    def AutoCheckByFreeSpaceRatio(self, episode):
        if self.nandController.GetFreeSpaceRatio() < (1 - AUTO_GC_RATIO):
            # find the highest invalid num block to gc
            blockIdx = self.nandController.GetHighestInvalidsBlockIdx()
            try:
                writeBytes = self.Run(blockIdx)
                self.gcHistory.Success(episode)
                return writeBytes
            except:
                self.gcHistory.Fail(episode)
                return 0
        return 0

    # implement Garbage Collection on blockIdx
    def Run(self, blockIdx):
        totalWriteBytes = 0
        blockType = self.nandController.blocks[blockIdx].type
        if blockType == BlockType.NONE: raise MemoryError('GC on full valid Block')
        for page in self.nandController.blocks[blockIdx].pages:
            lbaAddresses = ([lba.address for lba in page.storeLbas])
            programPage, writeBytes = self.nandController.Program(page.storeLbas, blockType)
            self.addressTranslation.Update(lbaAddresses, programPage)
            totalWriteBytes += writeBytes
        self.nandController.EraseBlock(blockIdx)
        return totalWriteBytes