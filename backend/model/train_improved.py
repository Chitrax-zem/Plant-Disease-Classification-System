"""
Improved Training Script for Plant Disease Classification
With better hyperparameters and longer training
"""

import os
import json
import numpy as np
from datetime import datetime

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
from tensorflow.keras import layers, models, optimizers, regularizers
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import (
    EarlyStopping, 
    ReduceLROnPlateau, 
    ModelCheckpoint,
    CSVLogger
)

# ==================== CONFIGURATION ====================
# Increase epochs and adjust hyperparameters
IMAGE_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 50  # Increased from 30
FINE_TUNE_EPOCHS = 20  # Increased from 10
NUM_CLASSES = 38
INPUT_SHAPE = (IMAGE_SIZE, IMAGE_SIZE, 3)

# Data paths
TRAIN_DIR = 'data/train'
VAL_DIR = 'data/val'

# Model save paths
MODEL_DIR = 'model/saved_models'
os.makedirs(MODEL_DIR, exist_ok=True)

BEST_MODEL_PATH = os.path.join(MODEL_DIR, 'best_model.keras')
CLASS_NAMES_PATH = os.path.join(MODEL_DIR, 'class_names.json')


def create_data_generators():
    """Create data generators with strong augmentation"""
    
    # Strong training augmentation
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=40,  # Increased
        width_shift_range=0.3,  # Increased
        height_shift_range=0.3,  # Increased
        shear_range=0.3,  # Increased
        zoom_range=0.3,  # Increased
        horizontal_flip=True,
        vertical_flip=True,
        brightness_range=[0.7, 1.3],  # Wider range
        fill_mode='nearest',
        channel_shift_range=20,  # Added
    )
    
    val_datagen = ImageDataGenerator(rescale=1./255)
    
    train_generator = train_datagen.flow_from_directory(
        TRAIN_DIR,
        target_size=(IMAGE_SIZE, IMAGE_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        shuffle=True,
        seed=42
    )
    
    validation_generator = val_datagen.flow_from_directory(
        VAL_DIR,
        target_size=(IMAGE_SIZE, IMAGE_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        shuffle=False
    )
    
    return train_generator, validation_generator, train_generator.class_indices


def create_model(num_classes):
    """Create EfficientNetB0 model with improved architecture"""
    
    # Load base model
    base_model = EfficientNetB0(
        weights='imagenet',
        include_top=False,
        input_shape=INPUT_SHAPE
    )
    
    # Freeze base model initially
    base_model.trainable = False
    
    # Build improved head
    inputs = layers.Input(shape=INPUT_SHAPE)
    
    # Data augmentation layer (applied during training only)
    x = layers.RandomRotation(0.2)(inputs)
    x = layers.RandomZoom(0.2)(x)
    x = layers.RandomFlip("horizontal_and_vertical")(x)
    
    # Base model
    x = base_model(x, training=False)
    
    # Global pooling
    x = layers.GlobalAveragePooling2D()(x)
    
    # Improved classification head
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.5)(x)  # Increased dropout
    
    x = layers.Dense(
        512, 
        activation='relu',
        kernel_regularizer=regularizers.l2(0.01)  # Increased L2
    )(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.5)(x)
    
    x = layers.Dense(
        256, 
        activation='relu',
        kernel_regularizer=regularizers.l2(0.01)
    )(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.4)(x)
    
    # Output
    outputs = layers.Dense(num_classes, activation='softmax')(x)
    
    model = models.Model(inputs, outputs, name='plant_disease_classifier_v2')
    
    # Compile with lower initial learning rate
    model.compile(
        optimizer=optimizers.Adam(learning_rate=0.001),
        loss=tf.keras.losses.CategoricalCrossentropy(label_smoothing=0.1),
        metrics=[
            'accuracy',
            tf.keras.metrics.TopKCategoricalAccuracy(k=3, name='top_3_accuracy'),
            tf.keras.metrics.TopKCategoricalAccuracy(k=5, name='top_5_accuracy')
        ]
    )
    
    return model, base_model


def get_callbacks():
    """Create improved callbacks"""
    
    callbacks = [
        EarlyStopping(
            monitor='val_accuracy',
            patience=12,  # Increased patience
            restore_best_weights=True,
            verbose=1,
            mode='max',
            min_delta=0.001  # Minimum improvement
        ),
        
        ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.3,  # More aggressive reduction
            patience=5,
            min_lr=1e-8,
            verbose=1,
            mode='min'
        ),
        
        ModelCheckpoint(
            BEST_MODEL_PATH,
            monitor='val_accuracy',
            save_best_only=True,
            mode='max',
            verbose=1
        ),
        
        CSVLogger(
            os.path.join(MODEL_DIR, 'training_log.csv'),
            separator=',',
            append=False
        )
    ]
    
    return callbacks


def fine_tune_model(model, base_model, train_gen, val_gen, callbacks, initial_epochs):
    """Fine-tune with gradual unfreezing"""
    
    # First, unfreeze last 30 layers
    base_model.trainable = True
    
    # Freeze all but last 30 layers
    for layer in base_model.layers[:-30]:
        layer.trainable = False
    
    # Recompile with lower learning rate
    model.compile(
        optimizer=optimizers.Adam(learning_rate=1e-5),  # Much lower LR
        loss=tf.keras.losses.CategoricalCrossentropy(label_smoothing=0.1),
        metrics=[
            'accuracy',
            tf.keras.metrics.TopKCategoricalAccuracy(k=3, name='top_3_accuracy'),
            tf.keras.metrics.TopKCategoricalAccuracy(k=5, name='top_5_accuracy')
        ]
    )
    
    print("\n" + "="*50)
    print("Phase 2: Fine-tuning (last 30 layers)")
    print("="*50)
    
    history_fine = model.fit(
        train_gen,
        epochs=initial_epochs + FINE_TUNE_EPOCHS,
        initial_epoch=initial_epochs,
        validation_data=val_gen,
        callbacks=callbacks,
        verbose=1
    )
    
    return model, history_fine


def main():
    print("\n" + "="*60)
    print("Plant Disease Classification - Improved Training")
    print("="*60)
    
    # Check GPU
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        print(f"GPU Available: {gpus}")
    else:
        print("Running on CPU - training will be slower")
    
    # Create data generators
    print("\nLoading dataset...")
    train_gen, val_gen, class_indices = create_data_generators()
    
    # Save class names
    idx_to_class = {v: k for k, v in class_indices.items()}
    class_names = [idx_to_class[i] for i in range(len(idx_to_class))]
    with open(CLASS_NAMES_PATH, 'w') as f:
        json.dump(class_names, f, indent=2)
    
    print(f"Training samples: {train_gen.samples}")
    print(f"Validation samples: {val_gen.samples}")
    print(f"Number of classes: {len(class_names)}")
    
    # Create model
    print("\nBuilding model...")
    model, base_model = create_model(len(class_names))
    model.summary()
    
    # Callbacks
    callbacks = get_callbacks()
    
    # Phase 1: Train with frozen base
    print("\n" + "="*50)
    print("Phase 1: Training classifier head")
    print("="*50)
    
    history = model.fit(
        train_gen,
        epochs=EPOCHS,
        validation_data=val_gen,
        callbacks=callbacks,
        verbose=1
    )
    
    # Phase 2: Fine-tune
    model, history_fine = fine_tune_model(
        model, base_model, train_gen, val_gen, callbacks, EPOCHS
    )
    
    # Save final model
    final_path = os.path.join(MODEL_DIR, 'final_model.keras')
    model.save(final_path)
    print(f"\nSaved final model to {final_path}")
    
    # Evaluate
    print("\n" + "="*50)
    print("Final Evaluation")
    print("="*50)
    
    results = model.evaluate(val_gen, verbose=1)
    print(f"\nValidation Loss: {results[0]:.4f}")
    print(f"Validation Accuracy: {results[1]:.4f}")
    print(f"Top-3 Accuracy: {results[2]:.4f}")
    print(f"Top-5 Accuracy: {results[3]:.4f}")
    
    print("\n" + "="*60)
    print("Training Complete!")
    print("="*60)
    
    return model, history


if __name__ == '__main__':
    main()