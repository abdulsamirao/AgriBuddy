from keras.models import load_model
from keras.preprocessing.image import img_to_array
from PIL import Image
import numpy as np

model = load_model("models/tomato.keras")

def preprocess_image(image_path: str):
    img = Image.open(image_path).convert("RGB").resize((224, 224))
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

class_names = ['Tomato___Bacterial_Spot', 'Tomato___Early_Blight', 'Tomato___Healthy', 'Tomato___Late_Blight', 'Tomato___Leaf_Mold', 'Tomato___Mosaic_Virus', 'Tomato___Powdery_Mildew', 'Tomato___Septoria_Leaf_Spot', 'Tomato___Spider_Mites_Two-Spotted', 'Tomato___Target_Spot', 'Tomato___Yellow_Leaf_Curl_Virus']

def predict_leaf_disease(image_path: str) -> tuple[str, float]:
    predictions = model.predict(preprocess_image(image_path))
    predicted_class = class_names[np.argmax(predictions)]
    confidence = np.max(predictions)
    return predicted_class, confidence
    
