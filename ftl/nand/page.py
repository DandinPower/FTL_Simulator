import enum
from dotenv import load_dotenv
import os
load_dotenv()

class PageStatus(enum.Enum):
    FREE = 1
    VALID = 2
    INVALID = 3

NUMS_OF_LBA_IN_PAGE = int(os.getenv('NUMS_OF_LBA_IN_PAGE'))

# 流程Flow -> 先將lba program進空的page, 再在lba那邊Update page address, 如果lba已經有的話就會覆蓋掉page並且呼叫原始的page去刪掉lba對應關係, 在GC的時候由於會把所有valid的搬走, 所以原本的page會全部變invalid

# 應定時check page跟lba有無相互對應 以及PageStatus跟storeLba是否對應
class Page:
    def __init__(self, address, block):
        self.blockRef = block  #parent block的reference
        self.address = address #page的address
        self.storeLbas = []
        self.isFree = True

    def Program(self, lbas) -> None:
        # 如果欲寫入的lba數量超過總容量
        if len(lbas) > NUMS_OF_LBA_IN_PAGE - len(self.storeLbas):
            raise MemoryError('Exceeds Capacity')
        for lba in lbas:
            self.storeLbas.append(lba)

    # 只能由lba呼叫
    def Override(self, lba):
        self.storeLbas.remove(lba)
        if len(self.storeLbas) == 0:
            self.isFree = False
            # 全部都invalid通知上層block將invalid num += 1
            self.blockRef.PageInvalid()
        
    # 回傳0 -> free, 回傳1 -> invalid, 回傳-1 -> valid
    def GetStatus(self) -> int:
        if len(self.storeLbas) > 0:
            return PageStatus.VALID
        if self.isFree:
            return PageStatus.FREE
        return PageStatus.INVALID

    # 檢查lba有無儲存起來
    def CheckLba(self, lba):
        return (lba in self.storeLbas)

    # can only access by block
    def Erase(self):
        # 因為invalid的早就更新掉了 然後valid也搬走了也就變相全部invalid了因此應該要檢查是否是空得
        if self.GetStatus() == PageStatus.VALID:
            raise MemoryError('Erase a Block still have valid data')
        self.isFree = True

    def SelfCheck(self):
        for lba in self.storeLbas:
            if lba.pageRef != self:
                raise MemoryError('Page Self Check Error')

    def __eq__(self, other):
        if isinstance(other, Page):
            return self.address == other.address
        return False

    def __repr__(self):
        return f'{self.address}; {self.storeLbas}; {self.GetStatus()}'