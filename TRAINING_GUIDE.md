<h1>Plant Disease Model Training Guide</h1><h2>Step 1: Download the PlantVillage Dataset</h2><p>The PlantVillage dataset contains 70,000+ images of healthy and diseased plant leaves.</p><h3>Download Options:</h3><p><strong>Option A: From Kaggle</strong></p><pre><code class="language-bash"># Install kaggle CLI
pip install kaggle

# Download dataset
kaggle datasets download -d abdallahalidev/plantvillage-dataset

# Unzip
unzip plantvillage-dataset.zip -d data/
</code></pre><p><strong>Option B: From Official Source</strong></p><ul> <li>Visit: <a href="https://plantvillage.psu.edu/datasets">https://plantvillage.psu.edu/datasets</a></li> <li>Download the color images dataset</li> </ul><p><strong>Option C: Direct Link</strong></p><pre><code class="language-bash">wget https://data.mendeley.com/public-files/d3tyxt7j8h/files/8b5a3c8a-7b3a-4f3a-9b3a-7b3a4f3a9b3a/file_downloaded -O plantvillage.zip
unzip plantvillage.zip -d data/
</code></pre><h2>Step 2: Organize the Dataset</h2><p>The dataset should be organized like this:</p><pre><code>backend/data/
├── train/
│   ├── Apple___Apple_scab/
│   │   ├── image1.jpg
│   │   ├── image2.jpg
│   │   └── ...
│   ├── Apple___Black_rot/
│   ├── Apple___Cedar_apple_rust/
│   ├── Apple___healthy/
│   ├── ... (38 folders total)
│   └── Tomato___healthy/
└── val/
    ├── Apple___Apple_scab/
    ├── Apple___Black_rot/
    └── ... (same structure as train)
</code></pre><h3>Split Script</h3><p>If you have all images in one folder, use this script to split:</p><pre><code class="language-python"># split_dataset.py
import os
import shutil
import random
from pathlib import Path

def split_dataset(source_dir, train_dir, val_dir, split_ratio=0.8):
    """
    Split dataset into train and validation sets.
    
    Args:
        source_dir: Path to source directory with class folders
        train_dir: Path to training output directory
        val_dir: Path to validation output directory
        split_ratio: Ratio for training set (0.8 = 80% train, 20% val)
    """
    source = Path(source_dir)
    train = Path(train_dir)
    val = Path(val_dir)
    
    # Create output directories
    train.mkdir(parents=True, exist_ok=True)
    val.mkdir(parents=True, exist_ok=True)
    
    # Process each class folder
    for class_dir in source.iterdir():
        if not class_dir.is_dir():
            continue
            
        # Get all images
        images = list(class_dir.glob('*.*'))
        random.shuffle(images)
        
        # Split
        split_idx = int(len(images) * split_ratio)
        train_images = images[:split_idx]
        val_images = images[split_idx:]
        
        # Create class folders
        (train / class_dir.name).mkdir(exist_ok=True)
        (val / class_dir.name).mkdir(exist_ok=True)
        
        # Copy images
        for img in train_images:
            shutil.copy(img, train / class_dir.name / img.name)
        for img in val_images:
            shutil.copy(img, val / class_dir.name / img.name)
        
        print(f"{class_dir.name}: {len(train_images)} train, {len(val_images)} val")

if __name__ == '__main__':
    split_dataset(
        source_dir='data/raw',
        train_dir='data/train',
        val_dir='data/val',
        split_ratio=0.8
    )
</code></pre><h2>Step 3: Run Training</h2><pre><code class="language-bash">cd backend

# Activate virtual environment (if using one)
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Run training
python model/train_model.py
</code></pre><h2>Step 4: Training Configuration</h2><p>The training script uses these settings (in <code>backend/model/train_model.py</code>):</p><table class="e-rte-table"> <thead> <tr> <th>Parameter</th> <th>Value</th> </tr> </thead> <tbody><tr> <td>Image Size</td> <td>224 × 224</td> </tr> <tr> <td>Batch Size</td> <td>32</td> </tr> <tr> <td>Epochs</td> <td>30</td> </tr> <tr> <td>Optimizer</td> <td>Adam (lr=0.001)</td> </tr> <tr> <td>Loss</td> <td>Categorical Cross Entropy (label smoothing 0.1)</td> </tr> <tr> <td>Early Stopping</td> <td>Patience 8</td> </tr> <tr> <td>LR Reduction</td> <td>Factor 0.5, patience 4</td> </tr> </tbody></table><h2>Step 5: Monitor Training</h2><p>Training outputs:</p><ul> <li><code>backend/model/saved_models/best_model.keras</code> - Best model checkpoint</li> <li><code>backend/model/saved_models/training_log.csv</code> - Training metrics</li> <li><code>backend/model/saved_models/training_history.json</code> - History for plotting</li> </ul><h3>Expected Results</h3><table class="e-rte-table"> <thead> <tr> <th>Metric</th> <th>Target</th> </tr> </thead> <tbody><tr> <td>Training Accuracy</td> <td>95-98%</td> </tr> <tr> <td>Validation Accuracy</td> <td>92-96%</td> </tr> <tr> <td>Training Time</td> <td>2-4 hours (GPU) / 8-12 hours (CPU)</td> </tr> <tr> <td>Model Size</td> <td>~17MB</td> </tr> </tbody></table><h2>Step 6: Verify Model</h2><p>After training, verify the model:</p><pre><code class="language-bash"># Check if model was saved
ls -la backend/model/saved_models/

# Test prediction
curl -X POST -F "image=@test_leaf.jpg" http://localhost:5001/api/predict
</code></pre><hr><h2>Alternative: Use Pre-trained Model</h2><p>If you don't want to train from scratch, you can:</p><h3>Option A: Download Pre-trained Weights</h3><pre><code class="language-bash"># Create directory
mkdir -p backend/model/saved_models

# Download pre-trained model (example URL - replace with actual)
wget https://example.com/plant-disease-model.keras -O backend/model/saved_models/best_model.keras
</code></pre><h3>Option B: Use TensorFlow Hub</h3><p>Modify <code>predict.py</code> to use a pre-trained model from TensorFlow Hub:</p><pre><code class="language-python">import tensorflow_hub as hub

model = tf.keras.Sequential([
    hub.KerasLayer("https://tfhub.dev/google/efficientnet/b0/feature-vector/1"),
    tf.keras.layers.Dense(38, activation='softmax')
])
</code></pre><hr><h2>Quick Start (Demo Mode)</h2><p>The application already runs in <strong>demo mode</strong> with mock predictions! </p><p>Just start the servers:</p><pre><code class="language-bash"># Terminal 1 - Backend
cd backend
python app.py

# Terminal 2 - Frontend
cd frontend
npm run dev
</code></pre><p>The mock predictions let you test the full UI flow without a trained model.</p><hr><h2>Troubleshooting</h2><h3>Out of Memory During Training</h3><p>Reduce batch size in <code>train_model.py</code>:</p><pre><code class="language-python">BATCH_SIZE = 16  # or 8
</code></pre><h3>Slow Training</h3><p>Enable GPU:</p><pre><code class="language-python"># Check GPU availability
import tensorflow as tf
print(tf.config.list_physical_devices('GPU'))
</code></pre><h3>Dataset Not Found</h3><p>Update paths in <code>train_model.py</code>:</p><pre><code class="language-python">TRAIN_DIR = 'path/to/your/train/data'
VAL_DIR = 'path/to/your/val/data'
</code></pre>