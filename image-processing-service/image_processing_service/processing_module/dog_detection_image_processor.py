import torch
import torchvision.transforms as transforms
from PIL import Image
# import os
import io
import base64
import urllib.request
import json
import torchvision.models as models


# Load the ResNet-50 model pre-trained on ImageNet
model = models.resnet50(pretrained=True)

model.eval()  # Set the model to evaluation mode


# Download the ImageNet labels if not already present
url = "https://raw.githubusercontent.com/anishathalye/imagenet-simple-labels/master/imagenet-simple-labels.json"
response = urllib.request.urlopen(url)
labels = json.loads(response.read())

# Define image preprocessing steps
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def bytes_to_image(image_bytes):
    """
    This function converts the image bytes to a PIL image.
    Args:
        image_bytes (string): The image bytes to convert
    Returns:
        PIL image
    """
    decoded_bytes = base64.b64decode(image_bytes)
    image = Image.open(io.BytesIO(decoded_bytes))
    return image

def process_image(image_bytes):
    """
    This function processes the image by detecting the presence of a dog in the image.
    It uses the ResNet-50 model to classify the image and returns the result.
    Args:
        image_bytes (string): The image bytes to process
    Returns:
        Top class prediction
    """
    # Convert the image bytes to a PIL image
    image = bytes_to_image(image_bytes)

    image = preprocess(image).unsqueeze(0)  # Preprocess and add batch dimension
    
    # Forward pass through the model
    with torch.no_grad():
        outputs = model(image)

    # Get the top predicted class
    _, predicted_class = torch.max(outputs, 1)
    predicted_label = predicted_class.item()

    # Map the class to the label
    class_label = labels[predicted_label]
    
    print(f"The predicted class is: {predicted_label}, Label: {class_label}")

    return class_label.encode('utf-8')

# Example usage:
# load iamge bytes from /home/maver02/Projects/Infrastructure_suite_project/Development/find-the-dog-project/processed_images/image_bytes
# with open("/home/maver02/Projects/Infrastructure_suite_project/Development/find-the-dog-project/processed_images/image_bytes", "rb") as file:
#    image_bytes = file.read()

#processed_image = process_image(image_bytes)

