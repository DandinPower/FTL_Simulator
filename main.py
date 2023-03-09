from host.host_interface import HostInterface
from libs.history import WAFHistory
from tqdm import tqdm
from dotenv import load_dotenv
import os
load_dotenv()

TRACE_LENGTH = int(os.getenv('TRACE_LENGTH'))
WAF_RESULT = os.getenv('WAF_RESULT')
ESTIMATE_WAF_PERIOD = int(os.getenv('ESTIMATE_WAF_PERIOD'))

def main():
    hostInterface = HostInterface()
    history = WAFHistory()
    for i in tqdm(range(TRACE_LENGTH)):
        request, writeBytes, gcValid = hostInterface.Step()
        if (gcValid): history.AddGC(gcValid)
        history.AddHistory(i, request.bytes, writeBytes, hostInterface.flashTranslation.nandController.GetFreeSpaceRatio())
        if i % ESTIMATE_WAF_PERIOD == 0:
            tempWAF = hostInterface.flashTranslation.nandController.GetTempWAF()
            hostInterface.flashTranslation.nandController.UpdateBlockWAFDistribution()
            history.AddEstimateWAF(i, tempWAF, hostInterface.flashTranslation.nandController.GetFreeSpaceRatio())
    history.Finish(hostInterface.flashTranslation.garbageCollection.count, hostInterface.flashTranslation.garbageCollection.gcFailCount)
    #history.ShowHistory(WAF_RESULT)
    history.ShowEstimateWAFHistory(WAF_RESULT)
    hostInterface.flashTranslation.nandController.ShowBlockWAFDistribution()
    
if __name__ == "__main__":
    main()