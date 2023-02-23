from ..nand.page import Page

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