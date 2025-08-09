import torch
import torch.nn as nn
import torchvision.models as models


class TransferNet(nn.Module):
    def __init__(self):
        super(TransferNet, self).__init__()
        
        # Use pretrained ResNet18 and modify first conv layer if needed
        self.base_model = models.resnet18(pretrained=False)
        
        # Adjust conv1 to match shape (256 channels input instead of 3)
        self.base_model.conv1 = nn.Conv2d(256, 64, kernel_size=3, stride=1, padding=1)
        
        # Modify fully connected layers to match shapes from checkpoint
        self.base_model.fc = nn.Sequential(
            nn.Linear(1536, 80),
            nn.ReLU(),
            nn.Linear(80, 4)  # 4 classes as output
        )

    def forward(self, x):
        return self.base_model(x)
