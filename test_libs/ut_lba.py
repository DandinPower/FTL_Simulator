from ftl.nand.page import Page, Lba

class MockBlock:
    def __init__(self):
        pass 
    def PageInvalid(self):
        pass 

def test_1():
    block1 = MockBlock()
    page1 = Page(0, block1)
    page2 = Page(1, block1)
    lbas = [Lba(i) for i in range(5)]
    programLba = lbas[:4]
    page1.Program(programLba)
    for lba in programLba:
        lba.Update(page1)
    programLba = lbas[1:] 
    page2.Program(programLba)
    for lba in programLba:
        lba.Update(page2)
    assert page1.CheckLba(lbas[0])
    assert len(page1._storeLbas) == 1
    assert lbas[0].pageRef == page1
    assert page2.CheckLba(lbas[1])
    assert page2.CheckLba(lbas[2])
    assert page2.CheckLba(lbas[3])
    assert page2.CheckLba(lbas[4])
    assert len(page2._storeLbas) == 4
    assert lbas[1].pageRef == page2
    assert lbas[2].pageRef == page2
    assert lbas[3].pageRef == page2
    assert lbas[4].pageRef == page2
    for lba in lbas:
        lba.SelfCheck()
    page1.SelfCheck()
    page2.SelfCheck()

def test_2():
    block1 = MockBlock()
    page1 = Page(0, block1)
    page2 = Page(1, block1)
    lbas = [Lba(i) for i in range(4)]
    page1.Program(lbas)
    for lba in lbas:
        lba.Update(page1)
    page2.Program(lbas)
    for lba in lbas:
        lba.Update(page2)
    assert len(page1._storeLbas) == 0
    assert page1.GetStatus() == 1 
    assert page2.CheckLba(lbas[0])
    assert page2.CheckLba(lbas[1])
    assert page2.CheckLba(lbas[2])
    assert page2.CheckLba(lbas[3])
    assert len(page2._storeLbas) == 4
    assert lbas[0].pageRef == page2
    assert lbas[1].pageRef == page2
    assert lbas[2].pageRef == page2
    assert lbas[3].pageRef == page2
    for lba in lbas:
        lba.SelfCheck()
    page1.SelfCheck()
    page2.SelfCheck()
    
