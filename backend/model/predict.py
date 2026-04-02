""" 
Prediction module for Plant Disease Classification
"""

import os
import json
import numpy as np
from typing import List, Dict, Tuple, Optional

# TensorFlow imports
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from tensorflow.keras.applications.efficientnet import preprocess_input

from config import MODEL_PATH, CLASS_NAMES_PATH, IMAGE_SIZE, INPUT_SHAPE
from model.disease_data import get_disease_info, DISEASE_CLASSES


class DiseasePredictor:
    """
    Plant disease prediction class using EfficientNetB0 model
    """
    
    def __init__(self):
        """Initialize the predictor by loading model and class names"""
        self.model = None
        self.class_names = None
        self._load_model()
        self._load_class_names()
    
    def _load_model(self):
        """Load the trained Keras model"""
        # Try different model formats in order of preference
        model_paths = [
            MODEL_PATH,  # .keras format
            MODEL_PATH.replace('.keras', '.h5'),  # .h5 format (better compatibility)
        ]
        
        for model_path in model_paths:
            if os.path.exists(model_path):
                print(f"Loading model from {model_path}")
                try:
                    self.model = load_model(model_path)
                    print("Model loaded successfully")
                    return
                except Exception as e:
                    print(f"Error loading model from {model_path}: {e}")
                    continue
        
        print(f"Model not found. Tried: {model_paths}")
        print("Using placeholder mode for development")
        self.model = None
    
    def _load_class_names(self):
        """Load class names from JSON file or use defaults"""
        if os.path.exists(CLASS_NAMES_PATH):
            with open(CLASS_NAMES_PATH, 'r') as f:
                self.class_names = json.load(f)
        else:
            self.class_names = DISEASE_CLASSES
        
        print(f"Loaded {len(self.class_names)} disease classes")
    
    def preprocess_image(self, image_path: str) -> np.ndarray:
        """
        Preprocess image for model prediction.
        
        IMPORTANT: Uses EfficientNet's preprocess_input for proper normalization.
        This MUST match the preprocessing used during training!
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Preprocessed image as numpy array
        """
        # Load image with target size
        img = load_img(image_path, target_size=IMAGE_SIZE)
        
        # Convert to array
        img_array = img_to_array(img)
        
        # Expand dimensions to create batch
        img_array = np.expand_dims(img_array, axis=0)
        
        # CRITICAL: Use EfficientNet's preprocess_input (NOT / 255.0)
        # This matches the training preprocessing in train_fixed.py
        img_array = preprocess_input(img_array)
        
        return img_array
    
    def preprocess_image_array(self, image_array: np.ndarray) -> np.ndarray:
        """
        Preprocess image array for model prediction.
        
        IMPORTANT: Uses EfficientNet's preprocess_input for proper normalization.
        This MUST match the preprocessing used during training!
        
        Args:
            image_array: Image as numpy array
            
        Returns:
            Preprocessed image as numpy array
        """
        # Resize if needed
        import cv2
        if image_array.shape[:2] != IMAGE_SIZE:
            image_array = cv2.resize(image_array, IMAGE_SIZE)
        
        # Expand dimensions
        if len(image_array.shape) == 3:
            image_array = np.expand_dims(image_array, axis=0)
        
        # Convert to float32
        image_array = image_array.astype(np.float32)
        
        # CRITICAL: Use EfficientNet's preprocess_input (NOT / 255.0)
        # This matches the training preprocessing in train_fixed.py
        image_array = preprocess_input(image_array)
        
        return image_array
    
    def predict(self, image_path: str, top_k: int = 5) -> Dict:
        """
        Predict plant disease from image.
        
        Args:
            image_path: Path to the image file
            top_k: Number of top predictions to return
            
        Returns:
            Dictionary containing predictions and confidence scores
        """
        if self.model is None:
            # Return mock prediction for development
            return self._mock_prediction(top_k)
        
        # Preprocess image
        processed_image = self.preprocess_image(image_path)
        
        # Get predictions
        predictions = self.model.predict(processed_image, verbose=0)[0]
        
        # Get top-k predictions
        top_indices = np.argsort(predictions)[::-1][:top_k]
        
        all_predictions = []
        for idx in top_indices:
            all_predictions.append({
                "disease": self.class_names[idx],
                "confidence": float(predictions[idx]),
                "confidence_percentage": f"{predictions[idx] * 100:.2f}%"
            })
        
        # Get primary prediction
        primary = all_predictions[0]
        
        # Get treatment info for primary prediction
        treatment_info = get_disease_info(primary["disease"])
        
        return {
            "success": True,
            "primary_prediction": {
                "disease": primary["disease"],
                "confidence": primary["confidence"],
                "confidence_percentage": primary["confidence_percentage"]
            },
            "all_predictions": [
                {
                    "disease": p["disease"],
                    "confidence": p["confidence"],
                    "confidence_percentage": p["confidence_percentage"]
                }
                for p in all_predictions
            ],
            "treatment": treatment_info
        }
    
    def predict_from_array(self, image_array: np.ndarray, top_k: int = 5) -> Dict:
        """
        Predict plant disease from image array.
        
        Args:
            image_array: Image as numpy array
            top_k: Number of top predictions to return
            
        Returns:
            Dictionary containing predictions and confidence scores
        """
        if self.model is None:
            return self._mock_prediction(top_k)
        
        # Preprocess
        processed_image = self.preprocess_image_array(image_array)
        
        # Predict
        predictions = self.model.predict(processed_image, verbose=0)[0]
        
        # Get top-k
        top_indices = np.argsort(predictions)[::-1][:top_k]
        
        all_predictions = []
        for idx in top_indices:
            all_predictions.append({
                "disease": self.class_names[idx],
                "confidence": float(predictions[idx]),
                "confidence_percentage": f"{predictions[idx] * 100:.2f}%"
            })
        
        primary = all_predictions[0]
        treatment_info = get_disease_info(primary["disease"])
        
        return {
            "success": True,
            "primary_prediction": {
                "disease": primary["disease"],
                "confidence": primary["confidence"],
                "confidence_percentage": primary["confidence_percentage"]
            },
            "all_predictions": [
                {
                    "disease": p["disease"],
                    "confidence": p["confidence"],
                    "confidence_percentage": p["confidence_percentage"]
                }
                for p in all_predictions
            ],
            "treatment": treatment_info
        }
    
    def _mock_prediction(self, top_k: int = 5) -> Dict:
        """Generate mock prediction for development/testing"""
        import random
        
        # Generate random but plausible confidence scores
        scores = np.random.dirichlet(np.ones(len(self.class_names)))
        top_indices = np.argsort(scores)[::-1][:top_k]
        
        all_predictions = []
        for idx in top_indices:
            all_predictions.append({
                "disease": self.class_names[idx],
                "confidence": float(scores[idx]),
                "confidence_percentage": f"{scores[idx] * 100:.2f}%"
            })
        
        primary = all_predictions[0]
        treatment_info = get_disease_info(primary["disease"])
        
        return {
            "success": True,
            "primary_prediction": {
                "disease": primary["disease"],
                "confidence": primary["confidence"],
                "confidence_percentage": primary["confidence_percentage"]
            },
            "all_predictions": [
                {
                    "disease": p["disease"],
                    "confidence": p["confidence"],
                    "confidence_percentage": p["confidence_percentage"]
                }
                for p in all_predictions
            ],
            "treatment": treatment_info
        }
    
    def get_class_names(self) -> List[str]:
        """Return list of all disease classes"""
        return self.class_names
    
    def get_num_classes(self) -> int:
        """Return number of disease classes"""
        return len(self.class_names)


# Singleton instance
_predictor = None


def get_predictor() -> DiseasePredictor:
    """Get or create the predictor singleton"""
    global _predictor
    if _predictor is None:
        _predictor = DiseasePredictor()
    return _predictor