from libs.statistic import Entries
from host.host_request_queue import HostRequestQueue

from dotenv import load_dotenv
import os
load_dotenv()

TRACE_PATH = os.getenv('TRACE_PATH')
TRACE_LENGTH = int(os.getenv('TRACE_LENGTH'))
TARGET_PATH = os.getenv('TARGET_PATH')

def GetTargetAnswer():
    queue = HostRequestQueue()
    queue.LoadTrace(TRACE_PATH)
    entries = Entries()
    for i in range(TRACE_LENGTH):
        req = queue.GetWriteRequest()
        entries.Add(req.fid, req.lba, req.bytes)
    entries.Write(TARGET_PATH)

def main():
    GetTargetAnswer()

if __name__ == "__main__":
    main()