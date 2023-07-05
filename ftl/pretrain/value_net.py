from sklearn.preprocessing import StandardScaler
from .lba_dict import GetLbaFreqDict
from .q_model import QModel, QModel_Deep
import torch
from torch import autocast
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import os
load_dotenv()

MODEL_WEIGHT_PATH = os.getenv('MODEL_WEIGHT_PATH')
TRACE_PATH = os.getenv('TRACE_PATH')
MODEL_TYPE = os.getenv('MODEL_TYPE')
PRECISION = os.getenv('PRECISION')

def GetModelPrecision(type):
    if type == 'fp32':
        return torch.float32 
    elif type == 'fp16':
        return torch.float16 
    elif type == 'bp16':
        return torch.bfloat16

class ValueNet:
    def __init__(self) -> None:
        self.Initialize()
    
    def Initialize(self):
        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        if MODEL_TYPE == 'deep':
            self.qModel = QModel_Deep().to(self.device)
        elif MODEL_TYPE == 'normal':
            self.qModel = QModel().to(self.device)
        self.scalerLbaDiff = StandardScaler()
        self.scalerBytes = StandardScaler()
        self.prevLba = 0
        self.qModel.load_state_dict(torch.load(MODEL_WEIGHT_PATH))
        # self.qModel.half()
        # self.qModel.bfloat16()
        self.lbaFreqDict = GetLbaFreqDict()
        self.Standardize()

    def Standardize(self):
        data = pd.read_csv(TRACE_PATH, header=None, dtype=np.float64).values
        data[1:, 2] = np.diff(data[:, 2])
        data[0, 2] = 0
        data[:, 2] = self.scalerLbaDiff.fit_transform(data[:, 2].reshape(-1, 1)).flatten()
        data[:, 3] = self.scalerBytes.fit_transform(data[:, 3].reshape(-1, 1)).flatten()

    def NewReq(self, request):
        lbaDiff = request.lba - self.prevLba
        self.prevLba = request.lba
        bytes = request.bytes
        standardized_lba_diff = self.scalerLbaDiff.transform(np.array(lbaDiff).reshape(1, -1))
        standardized_bytes = self.scalerBytes.transform(np.array(bytes).reshape(1, -1))
        standardized_lba = np.array(self.lbaFreqDict[str(request.lba)]).reshape(1, -1)
        input_data = np.concatenate((standardized_lba, standardized_lba_diff, standardized_bytes), axis=1)
        with torch.no_grad():
            input_data = torch.tensor(input_data, dtype=torch.float32, device=self.device)
            with autocast(device_type='cuda', dtype=GetModelPrecision(PRECISION)):
                output = self.qModel(input_data)
                _, predicted_labels = torch.max(output, dim=1)
        return predicted_labels[0].cpu().numpy()