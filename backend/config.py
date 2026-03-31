"""
Configuration settings for Plant Disease Classification System
"""

import os

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Upload configuration
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

# Model configuration
MODEL_PATH = os.path.join(BASE_DIR, 'model', 'saved_models', 'best_model.keras')
CLASS_NAMES_PATH = os.path.join(BASE_DIR, 'model', 'saved_models', 'class_names.json')

# Image processing
IMAGE_SIZE = (224, 224)
INPUT_SHAPE = (224, 224, 3)

# API configuration
API_PREFIX = '/api'

# CORS settings
CORS_ORIGINS = ['http://localhost:5173', 'http://localhost:3000', 'http://127.0.0.1:5173']