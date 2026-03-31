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

# Add backend folder to path
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

# --------------------------------------------------
# Logging
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

# --------------------------------------------------
# Flask App
# --------------------------------------------------

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH
app.config["JSON_SORT_KEYS"] = False

CORS(app, resources={
    r"/api/*": {
        "origins": CORS_ORIGINS,
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --------------------------------------------------
# Helpers
# --------------------------------------------------

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def handle_errors(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(str(e), exc_info=True)
            return jsonify({
                "success": False,
                "error": "Internal server error",
                "message": str(e)
            }), 500
    return decorated

# --------------------------------------------------
# API ROUTES
# --------------------------------------------------

@app.route(f"{API_PREFIX}/health")
def health():
    return jsonify({
        "status": "healthy",
        "service": "Plant Disease Detection API",
        "time": datetime.utcnow().isoformat()
    })


@app.route(f"{API_PREFIX}/classes")
def classes():
    return jsonify({
        "success": True,
        "count": len(DISEASE_CLASSES),
        "classes": DISEASE_CLASSES
    })


@app.route(f"{API_PREFIX}/disease/<path:name>")
def disease_info(name):

    info = get_disease_info(name)

    if info is None:
        return jsonify({
            "success": False,
            "error": "Disease not found"
        }), 404

    return jsonify({
        "success": True,
        "disease": name,
        "info": info
    })


@app.route(f"{API_PREFIX}/predict", methods=["POST"])
@handle_errors
def predict():

    if "image" not in request.files:
        return jsonify({
            "success": False,
            "error": "No image provided"
        }), 400

    file = request.files["image"]

    if file.filename == "":
        return jsonify({
            "success": False,
            "error": "Empty filename"
        }), 400

    if not allowed_file(file.filename):
        return jsonify({
            "success": False,
            "error": "Invalid file type"
        }), 400

    filename = secure_filename(file.filename)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"{timestamp}_{filename}"

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    file.save(filepath)

    logger.info(f"Saved image {filepath}")

    predictor = get_predictor()

    result = predictor.predict(filepath)

    result["image"] = filename

    return jsonify(result)


@app.route(f"{API_PREFIX}/model/info")
@handle_errors
def model_info():

    predictor = get_predictor()

    return jsonify({
        "success": True,
        "model_loaded": predictor.model is not None,
        "num_classes": predictor.get_num_classes(),
        "classes": predictor.get_class_names()
    })

# --------------------------------------------------
# Error handlers
# --------------------------------------------------

@app.errorhandler(413)
def file_too_large(e):
    return jsonify({
        "success": False,
        "error": "File too large"
    }), 413


@app.errorhandler(404)
def not_found(e):
    return jsonify({
        "success": False,
        "error": "Route not found"
    }), 404


@app.errorhandler(500)
def internal_error(e):
    return jsonify({
        "success": False,
        "error": "Server error"
    }), 500

# --------------------------------------------------
# Serve frontend (optional)
# --------------------------------------------------

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path):

    frontend_dist = os.path.join(
        os.path.dirname(__file__),
        "..",
        "frontend",
        "dist"
    )

    if path and os.path.exists(os.path.join(frontend_dist, path)):
        return send_from_directory(frontend_dist, path)

    return send_from_directory(frontend_dist, "index.html")

# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__ == "__main__":

    print("\n===================================")
    print("Plant Disease Detection API")
    print("===================================\n")

    print("Endpoints:")
    print(f"GET  {API_PREFIX}/health")
    print(f"GET  {API_PREFIX}/classes")
    print(f"POST {API_PREFIX}/predict")
    print(f"GET  {API_PREFIX}/model/info\n")

    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True
    )