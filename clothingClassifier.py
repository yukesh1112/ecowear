import torch.nn as nn
from torchvision import models

def create_model(num_classes=10):
    """
    Creates a model instance with a pre-trained ResNet-18 base
    and a final layer adapted for the specified number of classes.
    """
    # Load a ResNet-18 model structure. 
    # weights=None because we will load our own trained weights, not pre-trained ones.
    model = models.resnet18(weights=None)

    # Get the number of input features for the classifier layer (fc).
    num_ftrs = model.fc.in_features
    
    # Replace the final layer to have the correct number of outputs (10).
    model.fc = nn.Linear(num_ftrs, num_classes)
    
    return model