import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader, random_split
import os
import time

# --- Configuration ---
# Set the path to your main dataset directory
DATA_DIR = 'dataset/train'
# Name for the saved model file
MODEL_SAVE_PATH = 'clothing_model_v1.pth'
# The number of classes in your dataset. You have 10 directories.
NUM_CLASSES = 10
# Training parameters
BATCH_SIZE = 32
NUM_EPOCHS = 15 # You can increase this for better accuracy if needed
LEARNING_RATE = 0.001

# --- 1. Data Preparation ---

# Define transformations for your images
# We apply data augmentation to the training set to make the model more robust
train_transforms = transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# For validation, we only resize and normalize
val_transforms = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# Load the dataset using ImageFolder
full_dataset = datasets.ImageFolder(DATA_DIR, transform=train_transforms)

# Split the dataset into training and validation sets (80% train, 20% val)
train_size = int(0.8 * len(full_dataset))
val_size = len(full_dataset) - train_size
train_dataset, val_dataset = random_split(full_dataset, [train_size, val_size])

# Apply the correct transformations to the validation dataset split
val_dataset.dataset.transform = val_transforms

# Create DataLoaders
train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False)

# Get class names from the dataset folders
class_names = full_dataset.classes
print(f"Dataset classes found: {class_names}")
print(f"Number of classes: {len(class_names)}")
if len(class_names) != NUM_CLASSES:
    print(f"Warning: NUM_CLASSES is set to {NUM_CLASSES}, but found {len(class_names)} folders.")


# --- 2. Model Definition ---

# Load a pre-trained ResNet-18 model
model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)

# Freeze all the parameters in the pre-trained model
for param in model.parameters():
    param.requires_grad = False

# Replace the final fully connected layer to match your number of classes
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, NUM_CLASSES)

# --- 3. Training Setup ---

# Set the device (use GPU if available, otherwise CPU)
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model = model.to(device)
print(f"Training on device: {device}")

# Define Loss Function and Optimizer
criterion = nn.CrossEntropyLoss()
# We only train the parameters of the final layer (the one we replaced)
optimizer = optim.Adam(model.fc.parameters(), lr=LEARNING_RATE)


# --- 4. Training and Validation Loop ---
start_time = time.time()

for epoch in range(NUM_EPOCHS):
    # --- Training Phase ---
    model.train()
    running_loss = 0.0
    running_corrects = 0

    for inputs, labels in train_loader:
        inputs = inputs.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        _, preds = torch.max(outputs, 1)
        loss.backward()
        optimizer.step()

        running_loss += loss.item() * inputs.size(0)
        running_corrects += torch.sum(preds == labels.data)

    train_loss = running_loss / len(train_dataset)
    train_acc = running_corrects.double() / len(train_dataset)

    # --- Validation Phase ---
    model.eval()
    val_loss = 0.0
    val_corrects = 0

    with torch.no_grad():
        for inputs, labels in val_loader:
            inputs = inputs.to(device)
            labels = labels.to(device)

            outputs = model(inputs)
            loss = criterion(outputs, labels)
            _, preds = torch.max(outputs, 1)

            val_loss += loss.item() * inputs.size(0)
            val_corrects += torch.sum(preds == labels.data)

    val_loss = val_loss / len(val_dataset)
    val_acc = val_corrects.double() / len(val_dataset)

    print(f'Epoch {epoch+1}/{NUM_EPOCHS} | Train Loss: {train_loss:.4f} Acc: {train_acc:.4f} | Val Loss: {val_loss:.4f} Acc: {val_acc:.4f}')

# --- 5. Save the Final Model ---
torch.save(model.state_dict(), MODEL_SAVE_PATH)
time_elapsed = time.time() - start_time
print(f"\nTraining complete in {time_elapsed // 60:.0f}m {time_elapsed % 60:.0f}s")
print(f"Model saved to '{MODEL_SAVE_PATH}'")