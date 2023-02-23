from .host_request_queue import HostRequestQueue
from ftl.flash_translation import FlashTranslation
from dotenv import load_dotenv
import os
load_dotenv()

TRACE_PATH = os.getenv('TRACE_PATH')
TRACE_LENGTH = int(os.getenv('TRACE_LENGTH'))

class HostInterface:
    def __init__(self):
        self.hostRequestQueue = HostRequestQueue()
        self.hostRequestQueue.LoadTrace(TRACE_PATH, TRACE_LENGTH)
        self.flashTranslation = FlashTranslation()

    # environment step
    def Step(self):
        writeRequest = self.hostRequestQueue.GetWriteRequest()
        totalWriteBytes = self.Fio(writeRequest)
        return writeRequest, totalWriteBytes

    def Fio(self, request):
        return self.flashTranslation.Write(request)