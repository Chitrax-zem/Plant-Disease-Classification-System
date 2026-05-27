<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/TensorFlow-2.15-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white" />
  <img src="https://img.shields.io/badge/EfficientNetB0-Transfer%20Learning-34A853?style=for-the-badge&logo=google&logoColor=white" />
  <img src="https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white" />
  <img src="https://img.shields.io/badge/React-18+-61DAFB?style=for-the-badge&logo=react&logoColor=black" />
</p>

<h1 align="center">🌿 PlantMD — Plant Disease Classification System</h1>

<p align="center">
  Upload a leaf photo. Get an instant diagnosis across 38 disease categories, 14 plant species, and actionable treatment recommendations — powered by EfficientNetB0 transfer learning.
</p>

<p align="center">
  <strong>98.2% validation accuracy · ~200ms inference · 43,455-image PlantVillage dataset</strong>
</p>

<p align="center">
  <a href="#-quick-start"><strong>Quick Start →</strong></a> &nbsp;·&nbsp;
  <a href="#-model-architecture"><strong>Model →</strong></a> &nbsp;·&nbsp;
  <a href="#-api-reference"><strong>API →</strong></a> &nbsp;·&nbsp;
  <a href="#-training-pipeline"><strong>Training →</strong></a> &nbsp;·&nbsp;
  <a href="DEPLOYMENT.md"><strong>Deploy →</strong></a>
</p>

---

## What is Plant Disease Classification?

PDC is a full-stack deep learning web app that classifies plant leaf diseases from photos. Drag and drop a leaf image and the system:

1. Preprocesses it through EfficientNetB0's input pipeline
2. Runs a forward pass through the fine-tuned classification head
3. Returns the **top-5 predictions** with confidence scores
4. Surfaces **treatment and prevention recommendations** for the detected disease

It covers **38 disease categories** (including healthy classes) across **14 plant species**: Apple, Blueberry, Cherry, Corn, Grape, Orange, Peach, Pepper, Potato, Raspberry, Soybean, Squash, Strawberry, and Tomato.

---

## Architecture

```
┌──────────────────────────────────────┐
│  React + TypeScript (Vite)           │
│  Drag-and-drop upload · Recharts     │
└─────────────────┬────────────────────┘
                  │ HTTP/REST (multipart or base64)
                  ▼
┌──────────────────────────────────────┐
│  Flask REST API                      │
│  Gunicorn WSGI · CORS                │
└─────────────────┬────────────────────┘
                  │
                  ▼
┌──────────────────────────────────────┐
│  Prediction Engine                   │
│  EfficientNetB0 (ImageNet weights)   │
│  → GlobalAveragePooling              │
│  → Dense 256 (ReLU + L2)            │
│  → Dense 38 (Softmax)               │
└──────────────────────────────────────┘
```

**Request lifecycle:**

1. User uploads leaf image via drag-and-drop or camera capture
2. Backend resizes to 224×224 and applies EfficientNet `preprocess_input`
3. Forward pass through frozen backbone + custom classification head
4. Softmax outputs → top-5 predictions with confidence scores
5. Disease info looked up from `disease_data.py` → treatment and prevention steps returned

---

## Performance

| Metric | Value |
|---|---|
| Validation Accuracy | **98.2%** |
| Top-5 Accuracy | **99.7%** |
| Inference Time | ~200ms |
| API Response Time | <500ms |
| Model Size | ~21MB |
| Frontend Load | <2s |

Healthy classes achieve >95% precision due to distinct visual features. Fungal diseases discriminate well from characteristic lesion patterns. Viral diseases can occasionally be confused with nutrient deficiencies — a known limitation of image-only classification.

---

## Tech Stack

### Backend

| Library | Version | Purpose |
|---|---|---|
| Python | 3.10+ | Runtime |
| Flask | 3.0.0 | REST API |
| Flask-CORS | 4.0.0 | Cross-origin requests |
| TensorFlow / Keras | 2.15 / 3.x | Model inference |
| NumPy | 1.24.3 | Array operations |
| Pillow | 10.1.0 | Image loading and resizing |
| OpenCV | 4.8.1 | Image manipulation |
| Gunicorn | 21.2.0 | Production WSGI server |

### Frontend

| Library | Version | Purpose |
|---|---|---|
| React | 18.2.0 | UI |
| TypeScript | 5.3.3 | Type safety |
| Vite | 5.0.8 | Build tool |
| TailwindCSS | 3.3.6 | Styling |
| Recharts | 2.10.3 | Confidence bar charts |
| React Dropzone | 14.2.3 | File upload |
| Lucide React | 0.294.0 | Icons |

### Hosting

| Service | Purpose |
|---|---|
| Render | Backend API (Flask + Gunicorn) |
| Vercel | Frontend (Vite static build) |
| GitHub | Source control + CI/CD |

---

## Quick Start

### Prerequisites

- Python 3.10+ and pip
- Node.js 18+ and npm
- A trained model at `backend/model/saved_models/best_model.keras` *(see [Training](#-training-pipeline))*

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env            # set FLASK_ENV, PORT as needed

python app.py
```

API at **http://localhost:5001** · Docs at **http://localhost:5001/api/health**

### Frontend

```bash
cd frontend
npm install

# Point at your local backend
echo "VITE_API_URL=http://localhost:5001/api" > .env.local

npm run dev
```

App at **http://localhost:5173**

---

## Model Architecture

### EfficientNetB0 Transfer Learning

Training happens in two phases to maximize accuracy while minimizing overfitting.

**Phase 1 — Feature Extraction (frozen backbone)**

The EfficientNetB0 base (pretrained on ImageNet) is frozen. Only the classification head trains.

```
Input (224, 224, 3)
  │
  ▼
EfficientNetB0 base          ← frozen, ImageNet weights, output: (7, 7, 1280)
  │
  ▼
GlobalAveragePooling2D       → 1280-dim feature vector
  │
  ▼
BatchNormalization
Dropout (0.3)
Dense (256, ReLU) + L2(0.001)
BatchNormalization
Dropout (0.3)
  │
  ▼
Dense (38, Softmax)          → 38 disease classes
```

**Phase 2 — Fine-tuning (top 20 backbone layers unfrozen)**

The top 20 layers of EfficientNetB0 are unfrozen and trained jointly with the head at a lower learning rate.

| Component | Phase 1 Trainable | Phase 2 Trainable |
|---|---|---|
| EfficientNetB0 base | ~4.0M (frozen) | ~0.8M (top 20 layers) |
| Classification head | ~0.5M | ~0.5M |
| **Total** | **~0.5M** | **~1.3M** |

### Training Configuration

```python
# Phase 1
optimizer = Adam(learning_rate=0.001)

# Phase 2 (fine-tuning)
optimizer = Adam(learning_rate=1e-5)

loss = CategoricalCrossentropy(label_smoothing=0.1)

callbacks = [
    EarlyStopping(monitor='val_accuracy', patience=10, restore_best_weights=True),
    ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, min_lr=1e-7),
    ModelCheckpoint(monitor='val_accuracy', save_best_only=True),
]

augmentation = {
    'rotation_range': 30,
    'width_shift_range': 0.2,
    'height_shift_range': 0.2,
    'shear_range': 0.2,
    'zoom_range': 0.2,
    'horizontal_flip': True,
    'vertical_flip': True,
}
```

### ⚠️ Preprocessing Note

EfficientNet requires its own preprocessing function — **do not use `rescale=1./255`**. Using standard normalization will produce garbage predictions.

```python
from tensorflow.keras.applications.efficientnet import preprocess_input

datagen = ImageDataGenerator(
    preprocessing_function=preprocess_input,  # ✅ correct
    # rescale=1./255                          # ❌ wrong — never use this with EfficientNet
)
```

This must be applied identically during training **and** inference.

---

## Training Pipeline

### Dataset

The model trains on the [PlantVillage Dataset](https://github.com/spMohanty/PlantVillage-Dataset):

| Split | Images |
|---|---|
| Training | 34,748 |
| Validation | 8,707 |
| **Total** | **43,455** |

38 disease categories · 14 plant species

### Running Training

```bash
cd backend
python model/train_fixed.py
```

Outputs written to `backend/model/saved_models/`:

| File | Description |
|---|---|
| `best_model.keras` | Best checkpoint by `val_accuracy` |
| `class_names.json` | Class index → label mapping |
| `training_log.csv` | Per-epoch loss and accuracy |

---

## API Reference

**Base URLs**

- Production: `https://plant-disease-api.onrender.com/api`
- Development: `http://localhost:5001/api`

### Endpoints

#### `GET /api/health`
Service health check.
```json
{
  "status": "healthy",
  "service": "Plant Disease Classification API",
  "version": "1.0.0",
  "timestamp": "2026-04-01T12:00:00.000000"
}
```

#### `GET /api/classes`
Returns all 38 disease class labels.
```json
{
  "success": true,
  "count": 38,
  "classes": ["Apple___Apple_scab", "Apple___Black_rot", "..."]
}
```

#### `POST /api/predict`
Upload a leaf image for classification.

```
Content-Type: multipart/form-data
Body: image=<file>
```

```json
{
  "success": true,
  "primary_prediction": {
    "disease": "Tomato___Late_blight",
    "confidence": 0.9542,
    "confidence_percentage": "95.42%"
  },
  "all_predictions": [
    { "disease": "Tomato___Late_blight",       "confidence": 0.9542 },
    { "disease": "Tomato___Early_blight",      "confidence": 0.0321 },
    { "disease": "Tomato___Septoria_leaf_spot","confidence": 0.0089 },
    { "disease": "Potato___Late_blight",       "confidence": 0.0032 },
    { "disease": "Tomato___healthy",           "confidence": 0.0016 }
  ],
  "treatment": {
    "description": "Late blight is caused by the oomycete Phytophthora infestans...",
    "treatment": [
      "Apply copper-based fungicides every 7–10 days",
      "Remove and destroy infected plant material",
      "Ensure proper air circulation between plants"
    ],
    "prevention": [
      "Use disease-resistant tomato varieties",
      "Avoid overhead irrigation",
      "Rotate crops every 2–3 years"
    ]
  }
}
```

#### `POST /api/predict/base64`
Same as `/api/predict` but accepts a base64-encoded image.

```json
{ "image": "data:image/jpeg;base64,/9j/4AAQ..." }
```

#### `GET /api/disease/{disease_name}`
Fetch treatment info for a specific disease by its class label (e.g. `Tomato___Late_blight`).

#### `GET /api/model/info`
Returns model metadata: input shape, number of classes, parameter count, load status.

---

## Project Structure

```
plant-disease-classification/
├── backend/
│   ├── app.py                         # Flask entry point
│   ├── config.py                      # Configuration
│   ├── gunicorn_config.py             # Production WSGI config
│   ├── render.yaml                    # Render deployment blueprint
│   ├── requirements.txt
│   ├── uploads/                       # Uploaded images (temp)
│   └── model/
│       ├── predict.py                 # Inference module
│       ├── disease_data.py            # Treatment & prevention database
│       ├── train_fixed.py             # Training script
│       └── saved_models/
│           ├── best_model.keras       # Trained model
│           └── class_names.json       # Class index mapping
│
└── frontend/
    ├── vite.config.ts
    ├── tailwind.config.js
    ├── tsconfig.json
    ├── vercel.json
    └── src/
        ├── App.tsx
        ├── api/api.ts                 # API service layer
        └── components/
            ├── ImageUpload.tsx        # Drag-and-drop upload
            ├── PredictionResults.tsx  # Results + treatment display
            ├── ConfidenceChart.tsx    # Top-5 bar chart
            ├── PredictionHistory.tsx  # Session history sidebar
            ├── Navbar.tsx
            └── Footer.tsx
```

---

## Supported Diseases (38 classes)

| Plant | Diseases |
|---|---|
| **Apple** | Apple Scab, Black Rot, Cedar Apple Rust, Healthy |
| **Blueberry** | Healthy |
| **Cherry** | Powdery Mildew, Healthy |
| **Corn** | Cercospora Leaf Spot, Common Rust, Northern Leaf Blight, Healthy |
| **Grape** | Black Rot, Esca (Black Measles), Leaf Blight, Healthy |
| **Orange** | Huanglongbing (Citrus Greening) |
| **Peach** | Bacterial Spot, Healthy |
| **Pepper** | Bacterial Spot, Healthy |
| **Potato** | Early Blight, Late Blight, Healthy |
| **Raspberry** | Healthy |
| **Soybean** | Healthy |
| **Squash** | Powdery Mildew |
| **Strawberry** | Leaf Scorch, Healthy |
| **Tomato** | Bacterial Spot, Early Blight, Late Blight, Leaf Mold, Septoria Leaf Spot, Spider Mites, Target Spot, Mosaic Virus, Yellow Leaf Curl Virus, Healthy |

---

## Deployment

### Backend → Render

1. Connect your GitHub repo to Render and create a **Web Service**
2. Set **Root Directory** to `backend`
3. **Build command**: `pip install -r requirements.txt`
4. **Start command**: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 120`
5. Add environment variables: `FLASK_ENV=production`, `TF_CPP_MIN_LOG_LEVEL=2`
6. Upload `model/saved_models/best_model.keras` before deploying

### Frontend → Vercel

1. Connect your GitHub repo to Vercel
2. Set **Root Directory** to `frontend`, **Framework** to Vite
3. Add environment variable: `VITE_API_URL=https://your-api-url.onrender.com/api`
4. Deploy

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions and environment-specific gotchas.

---

## Troubleshooting

**Low or nonsensical prediction confidence**
Almost always a preprocessing mismatch. Confirm that `preprocess_input` from `tensorflow.keras.applications.efficientnet` is used in both `train_fixed.py` and `predict.py` — not `rescale=1./255`.

**404 errors on Render**
Render assigns a dynamic port via `$PORT`. Make sure `app.py` uses `os.environ.get('PORT', 5001)` rather than a hardcoded port.

**CORS errors in the browser**
Your Vercel deployment domain needs to be in `CORS_ORIGINS` in `backend/config.py`. Add it and redeploy.

**TypeScript build fails on Vercel**
Usually caused by unused imports in strict mode. Either remove the imports or set `"noUnusedLocals": false` in `tsconfig.json`.

---

## Roadmap

**Near-term**
- [ ] Batch prediction (multiple images in one request)
- [ ] Confidence threshold filtering (suppress low-confidence results)
- [ ] Multilingual treatment recommendations

**Medium-term**
- [ ] TFLite export for offline / mobile inference
- [ ] Real-time camera prediction
- [ ] React Native mobile app
- [ ] User accounts and scan history persistence

**Long-term**
- [ ] Object detection for multi-leaf images
- [ ] Disease severity assessment
- [ ] More plant species and disease classes
- [ ] Agricultural IoT integration
- [ ] SIEM / reporting integrations

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit: `git commit -m 'feat: describe your change'`
4. Push: `git push origin feature/your-feature`
5. Open a Pull Request

---

## Acknowledgements

- **PlantVillage Dataset** — Hughes et al., *"An open access repository of images on plant health to enable the development of mobile disease diagnostics"*
- **EfficientNet** — Tan & Le, *"EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks"* (ICML 2019)
- TensorFlow / Keras team for the deep learning framework

---

## License

MIT — see [LICENSE](LICENSE) for details.

---

<p align="center">
  Built with Flask · TensorFlow · EfficientNetB0 · React
</p>
