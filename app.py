from flask import Flask, request, render_template
import os
from PIL import Image
import torch
import torchvision.transforms as T
from torchvision.models import efficientnet_b0
from torch.serialization import safe_globals

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
from torch.serialization import safe_globals
from torchvision.models import efficientnet_b0
import torch

with safe_globals({'torchvision.models.efficientnet.EfficientNet': efficientnet_b0}):
    model = torch.load('skin-model-pokemon.pt', map_location='cpu', weights_only=True)

model = torch.load('skin-model-pokemon.pt', map_location='cpu', weights_only=False)
model.eval()
classes = [
    'acanthosis-nigricans', 'acne', 'acne-scars',
    'alopecia-areata', 'dry', 'melasma',
    'oily', 'vitiligo', 'warts'
]
transform = get_transforms()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict_image():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    
    image_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(image_path)

    image = Image.open(image_path).convert('RGB')
    prediction = predict(model, image, transform, classes)

    return render_template('result.html', prediction=prediction, image_url=image_path)

