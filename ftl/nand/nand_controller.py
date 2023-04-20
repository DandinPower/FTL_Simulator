from libs.logs import PrintLog
from .block import Block, BlockType
from libs.distribution import MultiplyRewardFunction
from collections import deque, Counter
from tqdm import tqdm
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt
load_dotenv()

LBA_BYTES = int(os.getenv('LBA_BYTES'))
BLOCK_NUM = int(os.getenv('BLOCK_NUM'))
NUMS_OF_PAGE_IN_BLOCK = int(os.getenv('NUMS_OF_PAGE_IN_BLOCK'))
ACTIVE_GC_WAF_FULL_RATIO = float(os.getenv('ACTIVE_GC_WAF_FULL_RATIO'))
MA_PERIOD = int(os.getenv('MA_PERIOD'))
CHANGE_RATIO_ALPHA = float(os.getenv('CHANGE_RATIO_ALPHA'))

class RewardRecorder:
    def __init__(self):
        self.history = []

    def Reset(self):
        self.history.clear()
    
    def Add(self, reward):
        self.history.append(reward)
    
    # 取得考慮了ma變化率的reward
    def GetChangeRatioReward(self,):
        if len(self.history) < MA_PERIOD + 1:
            raise MemoryError('The length of reward history is not long enough to calculate.')
        prevRewardMA = sum(self.history[-MA_PERIOD - 1 : -1]) / MA_PERIOD
        currentRewardMA = sum(self.history[-MA_PERIOD :]) / MA_PERIOD 
        changeRatio = abs((prevRewardMA - currentRewardMA) / prevRewardMA)
        # print(f'prev: {prevRewardMA}, current:{currentRewardMA}, changeRatio: {changeRatio}')
        return self.history[-1] * (1 / (1 + CHANGE_RATIO_ALPHA * changeRatio))

    def GetReward(self,):
        return self.history[-1]

class WafRecorder:
    def __init__(self):
        self.history = []
    
    def Reset(self):
        self.history.clear() 
    
    def Add(self, waf):
        self.history.append(waf)

    def GetWaf(self):
        return self.history[-1]

class NandController:
    def __init__(self):
        self.blocks = []
        self.freeBlockIndexes = deque([i for i in range(BLOCK_NUM)]) #寫滿pop掉, gc後append
        self.currentHotBlockIndex = None 
        self.currentColdBlockIndex = None 
        self.distributionCounter = Counter()
        self.rewardRecorder = RewardRecorder()
        self.wafRecorder = WafRecorder()
        self.InitializeBlocks()

    def Reset(self):
        for block in self.blocks:
            block.Reset()
        self.freeBlockIndexes = deque([i for i in range(BLOCK_NUM)])
        self.currentHotBlockIndex = None 
        self.currentColdBlockIndex = None 
        self.distributionCounter = Counter()
        self.rewardRecorder.Reset()
        self.wafRecorder.Reset()

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
    
    # not inefficient 或許改成每Estimate waf step去檢查一次 然後清掉所有符合條件的block
    def GetGCBLock(self):
        fullInvalidBlockIndexes = [item for i, item in enumerate(range(BLOCK_NUM)) if i not in self.freeBlockIndexes and self.blocks[i].invalidPage / NUMS_OF_PAGE_IN_BLOCK >= ACTIVE_GC_WAF_FULL_RATIO] 
        return fullInvalidBlockIndexes

    # 計算目前狀態的reward跟waf
    def GetRewardAndWAF(self, blockIndexes):
        tempWAFs = []
        rewards = []
        for blockIndex in blockIndexes:
            waf = self.blocks[blockIndex].GetTempWAF()
            tempWAFs.append(waf)
            rewards.append(MultiplyRewardFunction(waf))
        waf = 1.5
        reward = 0
        if len(tempWAFs) != 0: 
            # 計算現在所有已滿的block的waf估計值
            waf =  sum(tempWAFs) / len(tempWAFs)
            reward = sum(rewards) / len(rewards)
        return reward, waf
    
    # 計算現在所有已滿的block的WAF分布
    def UpdateBlockWAFDistribution(self, blockIndexes):
        tempInvalidNums = [str(round((2 - (self.blocks[blockIndex].invalidPage / NUMS_OF_PAGE_IN_BLOCK)), 2)) for blockIndex in blockIndexes]
        self.distributionCounter.update(tempInvalidNums)

    # 更新目前的reward資訊
    def UpdateReward(self, reward):
        self.rewardRecorder.Add(reward)

    # 更新目前的waf資訊
    def UpdateWaf(self, waf):
        self.wafRecorder.Add(waf)
    
    # 每一個Estimate週期執行一次
    def EstimateStatus(self):
        # 取得所有寫滿的blockIndex
        fullBlockIndexes = [item for i, item in enumerate(range(BLOCK_NUM)) if i not in self.freeBlockIndexes]
        self.UpdateBlockWAFDistribution(fullBlockIndexes)
        reward, waf = self.GetRewardAndWAF(fullBlockIndexes)
        self.UpdateReward(reward)
        self.UpdateWaf(waf)

    # 取得reward
    def GetReward(self):
        return self.rewardRecorder.GetReward()

    # 取得考慮變化率的reward
    def GetChangeRatioReward(self):
        return self.rewardRecorder.GetChangeRatioReward()
    
    # 取得waf
    def GetWaf(self):
        return self.wafRecorder.GetWaf()