'''
This code downloads the resnet-50 model from the Hugging Face model hub and saves it locally.
'''

import torch
import os
from transformers import AutoModel

model_folder_path = "/home/maver02/Projects/Infrastructure_suite_project/Development/find-the-dog-project/models/"
model_name = "microsoft/resnet-50"

try:
    # Download the ResNet-50 model from Hugging Face model hub and save it locally
    model = AutoModel.from_pretrained(model_name)
    torch.save(model.state_dict(), os.path.join(model_folder_path, model_name, "resnet50_model.pth"))
except Exception as e:
    print(f"Error while loading the model: {e}")