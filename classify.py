import torch
from torchvision import transforms
from PIL import Image
from clothingClassifier import create_model # Import the new model creator

# --- CONFIGURATION (This section runs only once when the app starts) ---

# 1. CREATE THE MODEL STRUCTURE
# Create an instance of our new 10-class model.
model = create_model(num_classes=10)


# 2. LOAD THE TRAINED WEIGHTS
# Load the dictionary of weights (the state_dict) into the model structure.
MODEL_PATH = 'clothing_model_v1.pth' # The new 10-class model you trained
model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device('cpu')))

# Set the model to evaluation mode (very important for accurate predictions).
model.eval()


# 3. DEFINE IMAGE TRANSFORMATIONS
# These must be the same as the validation transformations from your training script.
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])


# --- CLASSIFICATION FUNCTION (This is called for each prediction) ---

def classify_image(image_path):
    """
    Takes an image path, processes it using the globally loaded model,
    and returns the predicted class index.
    """
    try:
        # Open the image file and ensure it's in RGB format.
        image = Image.open(image_path).convert('RGB')

        # Apply the transformations and add a batch dimension for the model.
        image_tensor = transform(image).unsqueeze(0)

        # Make a prediction with the model.
        with torch.no_grad(): # Disables gradient calculation for speed.
            outputs = model(image_tensor)
            # Get the index of the class with the highest score.
            _, predicted_index = torch.max(outputs, 1)

        # Return the predicted index as a simple number (e.g., 0, 1, 2...).
        return predicted_index.item()

    except Exception as e:
        print(f"Error classifying image: {e}")
        return None