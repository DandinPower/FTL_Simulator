from ..nand.block import BlockType
from dotenv import load_dotenv
import os
load_dotenv()

AUTO_GC_RATIO = float(os.getenv('AUTO_GC_RATIO'))
NUMS_OF_PAGE_IN_BLOCK = int(os.getenv('NUMS_OF_PAGE_IN_BLOCK'))

class GarbageCollection:
    def __init__(self, nandController, addressTranslation):
        self.count = 0
        self.gcFailCount = 0
        self.nandController = nandController
        self.addressTranslation = addressTranslation

    # use in passive gc, it will only run when free space is less than setting free ratio -- version 1
    # when there is an full invalid block do garbage collection, besides don't do -- version 2
    def AutoCheck(self):
        # if self.nandController.GetFreeSpaceRatio() < (1 - AUTO_GC_RATIO): 
        if self.nandController.IsFullInvalidBlock():
            return self.Run()
        else:
            return 0, None
        # return 0, None

    # implement gc because of free space is less than setting ratio
    def Run(self):
        totalWriteBytes = 0
        # find the highest invalid num block to gc
        blockIdx = self.nandController.GetHighestInvalidsBlockIdx()
        gcValid = NUMS_OF_PAGE_IN_BLOCK - self.nandController.blocks[blockIdx].invalidPage
        blockType = self.nandController.blocks[blockIdx].type
        if blockType == BlockType.NONE:
            self.gcFailCount += 1
            # print('There is no more invalid block can erase')
            return 0, None
        self.count += 1
        for page in self.nandController.blocks[blockIdx].pages:
            lbaAddresses = ([lba.address for lba in page.storeLbas])
            programPage, writeBytes = self.nandController.Program(page.storeLbas, blockType)
            self.addressTranslation.Update(lbaAddresses, programPage)
            totalWriteBytes += writeBytes
        self.nandController.EraseBlock(blockIdx)
        return totalWriteBytes, gcValid