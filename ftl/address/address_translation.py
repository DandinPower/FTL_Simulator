from .lba import Lba

class AddressTranslation:
    def __init__(self):
        self.map = dict()

    def __getitem__(self, address):
        temp = self.map.get(address)
        if temp == None:
            self.map[address] = Lba(address)
        return self.map[address]

    def Update(self, lbas, page):
        for lba in lbas:
            self.map[lba].Update(page)

    def SelfCheck(self):
        for _, value in self.map.items():
            value.SelfCheck()