"""
Plant Disease Classification System - Flask Backend
REST API for plant disease prediction from leaf images
"""

import os
import sys
from datetime import datetime
from functools import wraps
from typing import Dict, Any

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import logging

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import (
    UPLOAD_FOLDER, 
    ALLOWED_EXTENSIONS, 
    MAX_CONTENT_LENGTH,
    API_PREFIX,
    CORS_ORIGINS
)
from model.disease_data import DISEASE_CLASSES, get_disease_info
from model.predict import get_predictor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)

# Configuration
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
app.config['JSON_SORT_KEYS'] = False

# Enable CORS
CORS(app, resources={
    r"/api/*": {
        "origins": CORS_ORIGINS,
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename: str) -> bool:
    """Check if file has allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def handle_errors(f):
    """Decorator for error handling"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {f.__name__}: {str(e)}", exc_info=True)
            return jsonify({
                'success': False,
                'error': 'Internal server error',
                'message': str(e)
            }), 500
    return decorated_function


# ==================== API Routes ====================

@app.route(f'{API_PREFIX}/health', methods=['GET'])
@handle_errors
def health_check() -> Dict[str, Any]:
    """
    Health check endpoint.
    
    Returns:
        JSON with health status
    """
    return jsonify({
        'status': 'healthy',
        'service': 'Plant Disease Classification API',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    })


@app.route(f'{API_PREFIX}/classes', methods=['GET'])
@handle_errors
def get_classes() -> Dict[str, Any]:
    """
    Get list of all plant disease classes.
    
    Returns:
        JSON with list of disease classes
    """
    return jsonify({
        'success': True,
        'count': len(DISEASE_CLASSES),
        'classes': DISEASE_CLASSES
    })


@app.route(f'{API_PREFIX}/disease/<path:disease_name>', methods=['GET'])
@handle_errors
def get_disease_details(disease_name: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific disease.
    
    Args:
        disease_name: Name of the disease
        
    Returns:
        JSON with disease information
    """
    disease_info = get_disease_info(disease_name)
    
    if disease_info:
        return jsonify({
            'success': True,
            'disease': disease_name,
            'info': disease_info
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Disease not found',
            'message': f'No information found for disease: {disease_name}'
        }), 404


@app.route(f'{API_PREFIX}/predict', methods=['POST'])
@handle_errors
def predict() -> Dict[str, Any]:
    """
    Predict plant disease from uploaded image.
    
    Accepts:
        multipart/form-data with 'image' field
        
    Returns:
        JSON with prediction results
    """
    # Check if image was uploaded
    if 'image' not in request.files:
        return jsonify({
            'success': False,
            'error': 'No image provided',
            'message': 'Please upload an image file with the key "image"'
        }), 400
    
    file = request.files['image']
    
    # Check if file was selected
    if file.filename == '':
        return jsonify({
            'success': False,
            'error': 'No file selected',
            'message': 'Please select a file to upload'
        }), 400
    
    # Validate file type
    if not allowed_file(file.filename):
        return jsonify({
            'success': False,
            'error': 'Invalid file type',
            'message': f'Allowed file types: {", ".join(ALLOWED_EXTENSIONS)}'
        }), 400
    
    # Save file
    filename = secure_filename(file.filename)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_filename = f"{timestamp}_{filename}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
    
    file.save(filepath)
    logger.info(f"Saved uploaded image: {filepath}")
    
    try:
        # Get predictor
        predictor = get_predictor()
        
        # Make prediction
        result = predictor.predict(filepath, top_k=5)
        
        # Add file info to result
        result['image_info'] = {
            'filename': unique_filename,
            'original_filename': filename
        }
        
        logger.info(f"Prediction complete: {result['primary_prediction']['disease']} "
                   f"({result['primary_prediction']['confidence_percentage']})")
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'Prediction failed',
            'message': str(e)
        }), 500


@app.route(f'{API_PREFIX}/predict/base64', methods=['POST'])
@handle_errors
def predict_base64() -> Dict[str, Any]:
    """
    Predict plant disease from base64 encoded image.
    
    Accepts:
        JSON with 'image' field containing base64 encoded image
        
    Returns:
        JSON with prediction results
    """
    import base64
    import numpy as np
    import cv2
    
    data = request.get_json()
    
    if not data or 'image' not in data:
        return jsonify({
            'success': False,
            'error': 'No image provided',
            'message': 'Please provide a base64 encoded image in the "image" field'
        }), 400
    
    try:
        # Decode base64 image
        image_data = data['image']
        
        # Remove data URL prefix if present
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        
        # Decode
        image_bytes = base64.b64decode(image_data)
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            return jsonify({
                'success': False,
                'error': 'Invalid image data',
                'message': 'Could not decode the provided image'
            }), 400
        
        # Get predictor
        predictor = get_predictor()
        
        # Make prediction
        result = predictor.predict_from_array(image, top_k=5)
        
        logger.info(f"Prediction complete: {result['primary_prediction']['disease']} "
                   f"({result['primary_prediction']['confidence_percentage']})")
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Base64 prediction error: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'Prediction failed',
            'message': str(e)
        }), 500


@app.route(f'{API_PREFIX}/model/info', methods=['GET'])
@handle_errors
def model_info() -> Dict[str, Any]:
    """
    Get information about the loaded model.
    
    Returns:
        JSON with model information
    """
    predictor = get_predictor()
    
    info = {
        'success': True,
        'model_type': 'EfficientNetB0 Transfer Learning',
        'input_shape': [224, 224, 3],
        'num_classes': predictor.get_num_classes(),
        'classes': predictor.get_class_names(),
        'model_loaded': predictor.model is not None
    }
    
    if predictor.model is not None:
        info['total_params'] = predictor.model.count_params()
        info['input_shape'] = list(predictor.model.input_shape[1:])
        info['output_shape'] = list(predictor.model.output_shape[1:])
    
    return jsonify(info)


# ==================== Error Handlers ====================

@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error"""
    return jsonify({
        'success': False,
        'error': 'File too large',
        'message': f'Maximum file size is {MAX_CONTENT_LENGTH / (1024*1024):.0f}MB'
    }), 413


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Not found',
        'message': 'The requested resource was not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500


# ==================== Root Route ====================

@app.route('/')
def index():
    """Root route - API info"""
    return jsonify({
        'service': 'Plant Disease Classification API',
        'version': '1.0.0',
        'status': 'running',
        'endpoints': {
            'health': f'{API_PREFIX}/health',
            'classes': f'{API_PREFIX}/classes',
            'predict': f'{API_PREFIX}/predict',
            'predict_base64': f'{API_PREFIX}/predict/base64',
            'disease_info': f'{API_PREFIX}/disease/<name>',
            'model_info': f'{API_PREFIX}/model/info'
        }
    })


# ==================== Main ====================

if __name__ == '__main__':
    # Get port from environment variable (required for Render)
    port = int(os.environ.get('PORT', 5001))
    
    print("\n" + "="*60)
    print("Plant Disease Classification API")
    print("="*60)
    print(f"\nAPI Prefix: {API_PREFIX}")
    print(f"Upload Folder: {UPLOAD_FOLDER}")
    print(f"Allowed Extensions: {ALLOWED_EXTENSIONS}")
    print(f"Max File Size: {MAX_CONTENT_LENGTH / (1024*1024):.0f}MB")
    print(f"Port: {port}")
    print("\nEndpoints:")
    print(f"  GET  {API_PREFIX}/health       - Health check")
    print(f"  GET  {API_PREFIX}/classes      - Get disease classes")
    print(f"  GET  {API_PREFIX}/disease/<name> - Get disease info")
    print(f"  POST {API_PREFIX}/predict      - Predict from image")
    print(f"  POST {API_PREFIX}/predict/base64 - Predict from base64")
    print(f"  GET  {API_PREFIX}/model/info   - Model information")
    print("\n" + "="*60 + "\n")
    
    # Run app
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False
    )