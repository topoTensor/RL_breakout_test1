import torch
import torch.nn as nn

class NN(nn.Module):
    def __init__(self, ch_in, hid1, hid2, ch_out):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(ch_in, hid1), nn.ReLU(),
            nn.Linear(hid1, hid2), nn.ReLU(),
            nn.Linear(hid2, ch_out), nn.Tanh(),
        )

    def forward(self,x ):
        return self.net(x)

    
    def mutate(self, mutation_rate=0.1, mutation_strength=0.1):
        with torch.no_grad():
            for param in self.parameters():
                if torch.rand(1).item() < mutation_rate:
                    noise = torch.randn_like(param) * mutation_strength
                    param += noise