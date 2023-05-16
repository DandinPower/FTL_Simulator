import torch.nn as nn
from dotenv import load_dotenv
import os
load_dotenv()

INPUT_SIZE = int(os.getenv('INPUT_SIZE'))
HIDDEN_SIZE = int(os.getenv('HIDDEN_SIZE'))
ACTION_SIZE = int(os.getenv('ACTION_SIZE'))
    
class QModel(nn.Module):
    def __init__(self):
        super(QModel, self).__init__()
        self.hiddenLayer1 = nn.Linear(INPUT_SIZE, HIDDEN_SIZE)
        self.hiddenLayer2 = nn.Linear(HIDDEN_SIZE, HIDDEN_SIZE)
        self.outputLayer = nn.Linear(HIDDEN_SIZE, ACTION_SIZE)
        self.activation = nn.ReLU()

    def forward(self, inputs):
        x = self.activation(self.hiddenLayer1(inputs))
        x = self.activation(self.hiddenLayer2(x))
        x = self.outputLayer(x)
        return x
    
class QModel_Deep(nn.Module):
    def __init__(self):
        super(QModel_Deep, self).__init__()
        self.hiddenLayer1 = nn.Linear(INPUT_SIZE, HIDDEN_SIZE)
        self.hiddenLayer2 = nn.Linear(HIDDEN_SIZE, HIDDEN_SIZE)
        self.hiddenLayer3 = nn.Linear(HIDDEN_SIZE, HIDDEN_SIZE)
        self.outputLayer = nn.Linear(HIDDEN_SIZE, ACTION_SIZE)
        self.activation = nn.ReLU()

    def forward(self, inputs):
        x = self.activation(self.hiddenLayer1(inputs))
        x = self.activation(self.hiddenLayer2(x))
        x = self.activation(self.hiddenLayer3(x))
        x = self.outputLayer(x)
        return x