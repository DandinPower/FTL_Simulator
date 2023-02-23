from libs.logs import PrintLog
from .block import Block, BlockType
from collections import deque
from tqdm import tqdm
from dotenv import load_dotenv
import os
load_dotenv()

LBA_BYTES = int(os.getenv('LBA_BYTES'))
BLOCK_NUM = int(os.getenv('BLOCK_NUM'))

class NandController:
    def __init__(self):
        self.blocks = []
        self.freeBlockIndexes = deque([i for i in range(BLOCK_NUM)]) #寫滿pop掉, gc後append
        self.currentHotBlockIndex = None 
        self.currentColdBlockIndex = None 
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