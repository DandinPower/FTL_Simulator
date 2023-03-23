from libs.logs import PrintLog
from .block import Block, BlockType
from libs.distribution import MultiplyWeight
from collections import deque, Counter
from tqdm import tqdm
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt
load_dotenv()

LBA_BYTES = int(os.getenv('LBA_BYTES'))
BLOCK_NUM = int(os.getenv('BLOCK_NUM'))
NUMS_OF_PAGE_IN_BLOCK = int(os.getenv('NUMS_OF_PAGE_IN_BLOCK'))
WAF_DISTRIBUTION = os.getenv('WAF_DISTRIBUTION')
ACTIVE_GC_WAF_FULL_RATIO = float(os.getenv('ACTIVE_GC_WAF_FULL_RATIO'))

class NandController:
    def __init__(self):
        self.blocks = []
        self.freeBlockIndexes = deque([i for i in range(BLOCK_NUM)]) #寫滿pop掉, gc後append
        self.currentHotBlockIndex = None 
        self.currentColdBlockIndex = None 
        self.distributionCounter = Counter()
        self.InitializeBlocks()

    def InitializeBlocks(self):
        PrintLog('Build Virtual Blocks...')
        for i in tqdm(range(BLOCK_NUM)):
            self.blocks.append(Block(i))

    def ClearFreeBlockIndex(self, type):
        if (type == BlockType.HOT):
            self.currentHotBlockIndex = None
        elif (type == BlockType.COLD):
            self.currentColdBlockIndex = None
        else:
            raise TypeError('unknown block type')
        
    def GetHighestInvalidsBlockIdx(self):
        tempBlocks = sorted(self.blocks, reverse= True)
        return tempBlocks[0].blockIndex
    
    def GetFreeSpaceRatio(self):
        return len(self.freeBlockIndexes) / BLOCK_NUM
        
    # lbas為取出來的single logical Page, type為寫入的Block種類 (需使用BlockType Enum)
    def Program(self, lbas, type):
        programBlockIndex = self.GetFreeBlock(type)
        programPage = self.blocks[programBlockIndex].Program(lbas, type)
        if self.blocks[programBlockIndex].IsFull():
            self.freeBlockIndexes.remove(programBlockIndex)
            self.ClearFreeBlockIndex(type)
        if len(self.freeBlockIndexes) == 0:
            raise IndexError('no free block')
        return programPage, len(lbas) * LBA_BYTES

    def EraseBlock(self, blockIndex):
        # RemoveFromFreeBlockIfAlreadyFree
        if not self.blocks[blockIndex].IsFull():
            self.freeBlockIndexes.remove(blockIndex)
        # AddFreeBlock
        self.freeBlockIndexes.append(blockIndex)
        self.blocks[blockIndex].Erase()
   
    # 欲取得符合該type的block index
    def GetFreeBlock(self, type):
        if (type == BlockType.HOT):
            if self.currentHotBlockIndex:
                return self.currentHotBlockIndex
            if self.currentColdBlockIndex == self.freeBlockIndexes[0]:
                if len(self.freeBlockIndexes) == 1:
                    raise IndexError('no free hot block')
                else:
                    self.currentHotBlockIndex = self.freeBlockIndexes[1]
                    return self.currentHotBlockIndex
            self.currentHotBlockIndex = self.freeBlockIndexes[0]
            return self.currentHotBlockIndex
        elif (type == BlockType.COLD):
            if self.currentColdBlockIndex:
                return self.currentColdBlockIndex
            if self.currentHotBlockIndex == self.freeBlockIndexes[0]:
                if len(self.freeBlockIndexes) == 1:
                    raise IndexError('no free cold block')
                else:
                    self.currentColdBlockIndex = self.freeBlockIndexes[1]
                    return self.currentColdBlockIndex
            self.currentColdBlockIndex = self.freeBlockIndexes[0]
            return self.currentColdBlockIndex
        else:
            raise TypeError('unknown block type')
        
    def SelfCheck(self):
        for block in self.blocks:
            block.SelfCheck()

    def GetTempWAF(self):
        # 計算現在所有已滿的block的waf估計值
        fullBlockIndexes = [item for i, item in enumerate(range(BLOCK_NUM)) if i not in self.freeBlockIndexes]
        tempWAFs = [MultiplyWeight(self.blocks[blockIndex].GetTempWAF()) for blockIndex in fullBlockIndexes]
        # tempWAFs = [self.blocks[blockIndex].GetTempWAF() for blockIndex in fullBlockIndexes]
        if len(tempWAFs) != 0: return sum(tempWAFs) / len(tempWAFs)
        return 2
    
    def UpdateBlockWAFDistribution(self):
        # 計算現在所有已滿的block的WAF分布
        fullBlockIndexes = [item for i, item in enumerate(range(BLOCK_NUM)) if i not in self.freeBlockIndexes]
        tempInvalidNums = [str(round((2 - (self.blocks[blockIndex].invalidPage / NUMS_OF_PAGE_IN_BLOCK)), 2)) for blockIndex in fullBlockIndexes]
        self.distributionCounter.update(tempInvalidNums)

    # not inefficient 或許改成每Estimate waf step去檢查一次 然後清掉所有符合條件的block
    def IsFullInvalidBlock(self):
        fullInvalidBlockIndexes = [item for i, item in enumerate(range(BLOCK_NUM)) if i not in self.freeBlockIndexes and self.blocks[i].invalidPage / NUMS_OF_PAGE_IN_BLOCK > ACTIVE_GC_WAF_FULL_RATIO] 
        return bool(fullInvalidBlockIndexes)

    def ShowBlockWAFDistribution(self):
        x = list(self.distributionCounter.keys())
        x = [float(i) for i in x]
        y = list(self.distributionCounter.values())
        plt.bar(x, y, width=0.005)
        plt.xlabel("Estimated WAF")
        plt.ylabel("Times")
        plt.title("Estimated WAF Distribution")
        plt.savefig(WAF_DISTRIBUTION)
        plt.clf()