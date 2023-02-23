from ..nand.page import PageStatus
from dotenv import load_dotenv
import os
load_dotenv()

AUTO_GC_RATIO = float(os.getenv('AUTO_GC_RATIO'))

class GarbageCollection:
    def __init__(self, nandController, addressTranslation):
        self.count = 0
        self.nandController = nandController
        self.addressTranslation = addressTranslation

    # use in passive gc, it will only run when free space is less than setting free ratio
    def AutoCheck(self):
        if self.nandController.GetFreeSpaceRatio() < (1 - AUTO_GC_RATIO): 
            return self.Run()
        else:
            return 0

    # implement gc because of free space is less than setting ratio
    def Run(self):
        self.count += 1
        totalWriteBytes = 0
        # find the highest invalid num block to gc
        blockIdx = self.nandController.GetHighestInvalidsBlockIdx()
        blockType = self.nandController.blocks[blockIdx].type
        print(self.nandController.blocks[blockIdx])
        for page in self.nandController.blocks[blockIdx].pages:
            lbaAddresses = ([lba.address for lba in page.storeLbas])
            programPage, writeBytes = self.nandController.Program(page.storeLbas, blockType)
            self.addressTranslation.Update(lbaAddresses, programPage)
            totalWriteBytes += writeBytes
        self.nandController.EraseBlock(blockIdx)
        return totalWriteBytes