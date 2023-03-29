from .host_request_queue import HostRequestQueue, HostRequestQueueAction
from ftl.flash_translation import FlashTranslation
from dotenv import load_dotenv
import os
load_dotenv()

TRACE_PATH = os.getenv('TRACE_PATH')
TRACE_LENGTH = int(os.getenv('TRACE_LENGTH'))

class HostInterface:
    def __init__(self):
        #self.hostRequestQueue = HostRequestQueue()
        self.count = 0
        self.hostRequestQueueAction = HostRequestQueueAction()
        self.hostRequestQueueAction.LoadTrace(TRACE_PATH, TRACE_LENGTH)
        self.flashTranslation = FlashTranslation()

    # environment step
    def Step(self):
        writeRequest = self.hostRequestQueueAction.GetWriteRequest()
        totalWriteBytes = self.Fio(writeRequest)
        self.count += 1
        return writeRequest, totalWriteBytes

    def Fio(self, request):
        return self.flashTranslation.Write(request, self.count)