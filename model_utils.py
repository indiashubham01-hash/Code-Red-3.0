import torch
import torch.nn as nn

class CardioNN(nn.Module):
    def __init__(self, input_dim):
        super(CardioNN, self).__init__()
        self.layer1 = nn.Linear(input_dim, 64)
        self.relu1 = nn.ReLU()
        self.dropout1 = nn.Dropout(0.3)
        self.layer2 = nn.Linear(64, 32)
        self.relu2 = nn.ReLU()
        self.dropout2 = nn.Dropout(0.3)
        self.layer3 = nn.Linear(32, 16)
        self.relu3 = nn.ReLU()
        self.output = nn.Linear(16, 1)
        
    def forward(self, x):
        x = self.relu1(self.layer1(x))
        x = self.dropout1(x)
        x = self.relu2(self.layer2(x))
        x = self.dropout2(x)
        x = self.relu3(self.layer3(x))
        x = self.output(x) # return logits
        return x
