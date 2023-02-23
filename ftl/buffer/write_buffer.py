from collections import deque
from dotenv import load_dotenv
import os
load_dotenv()

NUMS_OF_LBA_IN_PAGE = int(os.getenv('NUMS_OF_LBA_IN_PAGE'))

class WriteBuffer:
    def __init__(self):
        self._buffer = deque()
    
    def AddLba(self, lba):
        self._buffer.append(lba)
    
    def GetPage(self):
        if len(self._buffer) == 0:
            return None 
        if len(self._buffer) < NUMS_OF_LBA_IN_PAGE:
            return tuple(self._buffer.popleft() for _ in range(len(self._buffer)))
        # return (lba_1, lba_2, ..., lba_N)
        return tuple(self._buffer.popleft() for _ in range(NUMS_OF_LBA_IN_PAGE))