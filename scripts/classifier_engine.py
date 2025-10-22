from keras.models import load_model
from keras.preprocessing.image import img_to_array
from PIL import Image
import numpy as np

class BaseClassifier:
    MODEL_PATH: str = ""
    CLASS_NAMES: list[str] = []
    
    def __init__(self):
        """Initializes the classifier by loading the specific model."""
        if not self.MODEL_PATH or not self.CLASS_NAMES:
            raise NotImplementedError(
                f"Class {self.__class__.__name__} must define MODEL_PATH and CLASS_NAMES."
            )
        
        print(f"Loading model from: {self.MODEL_PATH}...")
        try:
            self.model = load_model(self.MODEL_PATH)
            print("Model loaded successfully.")
        except Exception as e:
            print(f"Error loading model: {e}")
            raise
    
    @staticmethod
    def _preprocess_image(image_path: str) -> np.ndarray:
        """Preprocesses an image from a file path for model prediction."""
        try:
            img = Image.open(image_path).convert("RGB").resize((224, 224))
            img_array = img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0) # Add batch dimension
            return img_array
        except FileNotFoundError:
            raise FileNotFoundError(f"Image file not found at: {image_path}")
        except Exception as e:
            raise IOError(f"Error processing image: {e}")
    
    def predict(self, image_path: str) -> tuple[str, float]:
        """
        Predicts the class and confidence for a given image.

        Args:
            image_path (str): The file path to the image to classify.

        Returns:
            tuple[str, float]: The predicted class name and its confidence score.
        """
        img_data = self._preprocess_image(image_path)
        
        # Get predictions
        predictions = self.model.predict(img_data, verbose=0)
        
        # Extract results
        predicted_index = np.argmax(predictions)
        predicted_class = self.CLASS_NAMES[predicted_index]
        confidence = np.max(predictions)
        
        return predicted_class, float(confidence)

class TomatoLeafDiseaseClassifier(BaseClassifier):
    """Classifier specifically for Tomato leaf diseases."""
    
    MODEL_PATH = "models/tomato_disease_classifier/tomato.keras"
    CLASS_NAMES = [
        'Tomato___Bacterial_Spot', 'Tomato___Early_Blight', 'Tomato___Healthy', 
        'Tomato___Late_Blight', 'Tomato___Leaf_Mold', 'Tomato___Mosaic_Virus', 
        'Tomato___Powdery_Mildew', 'Tomato___Septoria_Leaf_Spot', 
        'Tomato___Spider_Mites_Two-Spotted', 'Tomato___Target_Spot', 
        'Tomato___Yellow_Leaf_Curl_Virus'
    ]

class AgriculturePestClassifier(BaseClassifier):
    """Classifier specifically for agriculture pests."""
    
    MODEL_PATH = "models/pest_classifier/pest_classifier_final.keras"
    CLASS_NAMES = ['ants', 'bees', 'beetle', 'catterpillar',
        'earthworms', 'earwig', 'grasshopper', 'moth', 'slug',
        'snail', 'wasp', 'weevil'
    ]