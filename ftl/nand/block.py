from .page import Page, PageStatus
import enum
from dotenv import load_dotenv
import os
load_dotenv()

NUMS_OF_PAGE_IN_BLOCK = int(os.getenv('NUMS_OF_PAGE_IN_BLOCK'))

class BlockType(enum.Enum):
    NONE = 1
    HOT = 2
    COLD = 3

class Block:
    def __init__(self, blockIndex):
        self.blockIndex = blockIndex
        self.pages = [Page(blockIndex * NUMS_OF_PAGE_IN_BLOCK + i, self) for i in range(NUMS_OF_PAGE_IN_BLOCK)]
        self.invalidPage = 0
        self.currentPageIndex = 0
        self.type = BlockType.NONE

    def IsFull(self):
        return self.currentPageIndex == NUMS_OF_PAGE_IN_BLOCK

    def Program(self, lbas, type):
        # 設定初始化Type
        if (self.type == BlockType.NONE):
            self.type = type
        # 檢查是否寫在正確的Block Type上 
        if self.type != type:
            raise TypeError('program on different type block')
        # Program在一個已經滿的Block上
        if self.currentPageIndex == NUMS_OF_PAGE_IN_BLOCK: 
            raise MemoryError('insufficent space to program')
        # Program在滿的Page Index上
        if self.pages[self.currentPageIndex].GetStatus() != PageStatus.FREE: 
            raise MemoryError('program on not free page')
        # 標示該Page的狀態以及紀錄寫入的LBA數量
        programPage = self.pages[self.currentPageIndex]
        programPage.Program(lbas) 
        self.currentPageIndex += 1
        return programPage
    
    def PageInvalid(self):
        self.invalidPage += 1
    
    def SelfCheck(self):
        for page in self.pages:
            page.SelfCheck()

    def Erase(self):
        self.invalidPage = 0
        self.currentPageIndex = 0
        self.type = BlockType.NONE
        for page in self.pages:
            page.Erase()

    def __getitem__(self, index):
        return self.pages[index]
    
    def __repr__(self):
        return f'Block: {self.blockIndex} Invalid: {self.invalidPage} Current: {self.currentPageIndex} Type: {self.type}\n'
    
    def __lt__(self, other):
        return self.invalidPage < other.invalidPage