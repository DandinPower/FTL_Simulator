import enum
from dotenv import load_dotenv
import os
load_dotenv()

NUMS_OF_LBA_IN_PAGE = int(os.getenv('NUMS_OF_LBA_IN_PAGE'))

# 流程Flow -> 先將lba program進空的page, 再在lba那邊Update page address, 如果lba已經有的話就會覆蓋掉page並且呼叫原始的page去刪掉lba對應關係, 在GC的時候由於會把所有valid的搬走, 所以原本的page會全部變invalid

# 應定時check page跟lba有無相互對應 以及PageStatus跟storeLba是否對應
class Page:
    def __init__(self, address, block):
        self._blockRef = block  #parent block的reference
        self._address = address #page的address
        self._storeLbas = []
        self._isFree = True

    def Program(self, lbas) -> None:
        # 如果欲寫入的lba數量超過總容量
        if len(lbas) > NUMS_OF_LBA_IN_PAGE - len(self._storeLbas):
            raise MemoryError('Exceeds Capacity')
        for lba in lbas:
            self._storeLbas.append(lba)

    # 只能由lba呼叫
    def Override(self, lba):
        self._storeLbas.remove(lba)
        if len(self._storeLbas) == 0:
            self._isFree = False
            # 全部都invalid通知上層block將invalid num += 1
            self._blockRef.PageInvalid()
        
    # 回傳0 -> free, 回傳1 -> invalid, 回傳-1 -> valid
    def GetStatus(self) -> int:
        if len(self._storeLbas) > 0:
            return -1
        if self._isFree:
            return 0
        return 1 

    # 檢查lba有無儲存起來
    def CheckLba(self, lba):
        return (lba in self._storeLbas)

    # can only access by block
    def Erase(self):
        # 因為invalid的早就更新掉了 然後valid也搬走了也就變相全部invalid了因此應該要檢查是否是空得
        if self.GetStatus() != 1:
            raise MemoryError('Erase a Block still have valid data')
        self._isFree = False

    def SelfCheck(self):
        for lba in self._storeLbas:
            if lba.pageRef != self:
                raise MemoryError('Page Self Check Error')

    def __eq__(self, other):
        if isinstance(other, Page):
            return self._address == other._address
        return False

    def __repr__(self):
        return f'{self._address}, {self._storeLbas}'
    
class Lba:
    def __init__(self, address: int) -> None:
        self.address: int = address 
        self.pageRef: Page = None 

    # program後呼叫
    def Update(self, pageRef: Page):
        #要確保page跟本身是對應的
        if self.pageRef != None:
            # 讓原本的page可以知道現在該lba指到別的地方了, 讓page可以反向清掉儲存的storeLba
            self.pageRef.Override(self)
        # 檢查在page那裏是否有紀錄成功了, 因為是先Program Page再updateLba
        if not pageRef.CheckLba(self):
            raise MemoryError('Lba Update Fail because of can not find associated page')
        self.pageRef = pageRef #page那邊的對應要再page那裏的program做

    # 檢查對應關係
    def SelfCheck(self):
        if self.pageRef:
            if not self.pageRef.CheckLba(self):
                raise MemoryError('LBA Self Check Error')

    def __eq__(self, other):
        if isinstance(other, Lba):
            return self.address == other.address
        return False
    
    def __repr__(self):
        return f'{self.address}'