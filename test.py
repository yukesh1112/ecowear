import torch

model_path = "D:/mini_project/HACKATHON/GreenStyle-main/model1.pth"
checkpoint = torch.load(model_path, map_location=torch.device("cpu"))

# Print the keys and layer shapes in the saved model
for key, value in checkpoint.items():
    print(f"{key} -> Shape: {value.shape}")
