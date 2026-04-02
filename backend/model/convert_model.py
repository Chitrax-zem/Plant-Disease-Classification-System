"""
Script to convert Keras model to a compatible format.
Run this locally if you encounter model loading issues on Render.

The issue: Keras 3.x models may not load correctly on different TensorFlow versions.

Solutions:
1. Save model as .keras format (recommended)
2. Save model as .h5 format (legacy)
3. Export as SavedModel format
"""

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
from tensorflow.keras.models import load_model

MODEL_DIR = 'model/saved_models'
MODEL_PATH = os.path.join(MODEL_DIR, 'best_model.keras')

def convert_to_h5():
    """Convert .keras model to .h5 format for better compatibility"""
    print(f"Loading model from {MODEL_PATH}...")
    
    try:
        model = load_model(MODEL_PATH)
        print("Model loaded successfully!")
        
        # Save as h5
        h5_path = os.path.join(MODEL_DIR, 'best_model.h5')
        model.save(h5_path)
        print(f"Model saved as {h5_path}")
        
        # Also save weights only
        weights_path = os.path.join(MODEL_DIR, 'best_model.weights.h5')
        model.save_weights(weights_path)
        print(f"Weights saved as {weights_path}")
        
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        print("\nTrying alternative method...")
        return None

def create_model_from_weights():
    """Recreate model architecture and load weights"""
    from tensorflow.keras import layers, models, regularizers
    from tensorflow.keras.applications import EfficientNetB0
    
    print("Creating model architecture...")
    
    # Load base model
    base_model = EfficientNetB0(
        weights=None,  # Don't load ImageNet weights
        include_top=False,
        input_shape=(224, 224, 3)
    )
    
    # Build model
    inputs = layers.Input(shape=(224, 224, 3))
    x = base_model(inputs, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.3)(x)
    x = layers.Dense(256, activation='relu', kernel_regularizer=regularizers.l2(0.001))(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.3)(x)
    outputs = layers.Dense(38, activation='softmax')(x)
    
    model = models.Model(inputs, outputs)
    
    # Load weights
    weights_path = os.path.join(MODEL_DIR, 'best_model.weights.h5')
    if os.path.exists(weights_path):
        model.load_weights(weights_path)
        print(f"Weights loaded from {weights_path}")
    
    return model

if __name__ == '__main__':
    print("="*60)
    print("Model Conversion Script")
    print("="*60)
    
    # Try to convert model
    model = convert_to_h5()
    
    if model is None:
        print("\nCould not convert model. Please check the model file.")
    else:
        print("\nModel conversion complete!")
        print("Use best_model.h5 for better compatibility on Render.")     