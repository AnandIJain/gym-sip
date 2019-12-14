import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchvision.transforms as T

class DQN(nn.Module):

    def __init__(self, in_shape, num_actions):
        super(DQN, self).__init__()
        self.layer1 = nn.Linear(in_shape, in_shape // 2)
        self.layer2 = nn.Linear(in_shape // 2, in_shape // 2)
        self.layer3 = nn.Linear(in_shape // 2, in_shape // 2)
        self.layer4 = nn.Linear(in_shape // 2, num_actions)

    # Called with either one element to determine next action, or a batch
    # during optimization. Returns tensor([[left0exp,right0exp]...]).
    def forward(self, x):
        x = F.relu(self.layer1(x))
        x = F.relu(self.layer2(x))
        x = F.relu(self.layer3(x))
        x = F.relu(self.layer4(x))
        return x
