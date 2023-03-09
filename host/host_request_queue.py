from collections import namedtuple
from libs.logs import PrintLog
from tqdm import tqdm
import pandas as pd

Request = namedtuple('Request', ['op_code', 'fid', 'lba', 'bytes'])

class HostRequestQueue:
    def __init__(self):
        self._requests = []
        self._idx = 0

    def Reset(self):
        self._idx = 0

    def LoadTrace(self, path, length = -1):
        PrintLog('use pandas to read csv....')
        self._requests.clear()
        df = pd.read_csv(path, header = None, delimiter=',', lineterminator='\n')
        loadCount = 0
        if length != -1: totalCount = length
        else: totalCount = len(df)
        for index, row in tqdm(df.iterrows(), total = totalCount - 1):
            loadCount += 1
            self._requests.append(Request(row[3], row[0], row[4], row[5]))
            if loadCount == length:
                break
    
    def GetRequest(self):
        if self._idx >= len(self._requests):
            self._idx = 0
        val = self._requests[self._idx]
        self._idx += 1
        return val
    
    def GetWriteRequest(self):        
        while 1:
            request = self.GetRequest()
            if request.op_code == "Write": return request

    def __len__(self):
        return len(self._requests)
    
RequestAction = namedtuple('RequestAction', ['op_code', 'fid', 'lba', 'bytes', 'action'])

class HostRequestQueueAction:
    def __init__(self):
        self._requests = []
        self._idx = 0

    def Reset(self):
        self._idx = 0

    def LoadTrace(self, path, length = -1):
        PrintLog('use pandas to read csv....')
        self._requests.clear()
        df = pd.read_csv(path, header = None, delimiter=',', lineterminator='\n')
        loadCount = 0
        if length != -1: totalCount = length
        for index, row in tqdm(df.iterrows(), total = totalCount - 1):
            loadCount += 1
            self._requests.append(RequestAction(row[0], row[1], row[2], row[3], row[4]))
            if loadCount == length:
                break
    
    def GetRequest(self):
        if self._idx >= len(self._requests):
            self._idx = 0
        val = self._requests[self._idx]
        self._idx += 1
        return val
    
    def GetWriteRequest(self):        
        while 1:
            request = self.GetRequest()
            if request.op_code == 2: return request

    def __len__(self):
        return len(self._requests)