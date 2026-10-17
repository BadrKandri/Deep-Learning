import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from fastapi import APIRouter, UploadFile, File
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf


router = APIRouter()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "../models/model_v1.keras")
MODEL = tf.keras.models.load_model(MODEL_PATH)


CLASS_NAMES = ['Early Blight', 'Late Blight', 'Healthy']

@router.get("/ping")
async def ping():
    return "hello, potato"

def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)).convert("RGB"))
    return image

@router.post("/predict")
async def potato_predict(file: UploadFile = File(...)):
    image= read_file_as_image(await file.read())
    img_batch = np.expand_dims(image, 0)
    
    predictions = MODEL.predict(img_batch)
    
    index = int(np.argmax(predictions[0]))
    raw_confidence = float(np.max(predictions[0]))
    confidence = f"{raw_confidence * 100:.2f}%"
    predicted_class = CLASS_NAMES[index]
    
    return {
        "filename": file.filename,
        "class": predicted_class,
        "confidence": confidence
    }