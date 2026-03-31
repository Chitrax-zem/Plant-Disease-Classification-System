"""
FIXED Training Script for Plant Disease Classification
Addresses the low accuracy issue with proper configuration
"""

import os
import json
import numpy as np
from datetime import datetime

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
from tensorflow.keras import layers, models, optimizers, regularizers
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.applications.efficientnet import preprocess_input
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import (
    EarlyStopping, 
    ReduceLROnPlateau, 
    ModelCheckpoint,
    CSVLogger
)

print("TensorFlow version:", tf.__version__)
print("GPU Available:", tf.config.list_physical_devices('GPU'))

# ==================== CONFIGURATION ====================
IMAGE_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 25  # Start with fewer epochs, then fine-tune
FINE_TUNE_EPOCHS = 15
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
    """
    Create data generators with CORRECT preprocessing for EfficientNet.
    
    IMPORTANT: EfficientNet expects specific preprocessing (preprocess_input).
    Using rescale=1./255 is WRONG for EfficientNet!
    """
    
    # Training data augmentation
    # NOTE: We use preprocess_input for EfficientNet, NOT rescale=1./255
    train_datagen = ImageDataGenerator(
        preprocessing_function=preprocess_input,  # CRITICAL FIX!
        rotation_range=30,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        vertical_flip=True,
        fill_mode='nearest'
    )
    
    # Validation data - same preprocessing, no augmentation
    val_datagen = ImageDataGenerator(
        preprocessing_function=preprocess_input  # CRITICAL FIX!
    )
    
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
    """
    Create EfficientNetB0 model with proper architecture.
    """
    
    # Load base model with ImageNet weights
    base_model = EfficientNetB0(
        weights='imagenet',
        include_top=False,
        input_shape=INPUT_SHAPE
    )
    
    # Freeze base model for initial training
    base_model.trainable = False
    
    # Build model
    inputs = layers.Input(shape=INPUT_SHAPE)
    
    # Base model - inputs are already preprocessed
    x = base_model(inputs, training=False)
    
    # Classification head
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.3)(x)  # Reduced from 0.5
    
    x = layers.Dense(
        256,  # Reduced from 512
        activation='relu',
        kernel_regularizer=regularizers.l2(0.001)
    )(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.3)(x)
    
    # Output layer - NO label smoothing here, it's in the loss
    outputs = layers.Dense(num_classes, activation='softmax')(x)
    
    model = models.Model(inputs, outputs, name='plant_disease_classifier')
    
    # Compile with appropriate learning rate
    model.compile(
        optimizer=optimizers.Adam(learning_rate=0.001),
        loss=tf.keras.losses.CategoricalCrossentropy(label_smoothing=0.1),
        metrics=['accuracy']
    )
    
    return model, base_model


def get_callbacks():
    """Create training callbacks."""
    
    callbacks = [
        EarlyStopping(
            monitor='val_accuracy',
            patience=10,
            restore_best_weights=True,
            verbose=1,
            mode='max'
        ),
        
        ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=3,
            min_lr=1e-7,
            verbose=1
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


def unfreeze_layers(model, base_model, num_layers=20):
    """
    Unfreeze top layers of base model for fine-tuning.
    """
    base_model.trainable = True
    
    # Freeze all but the top N layers
    for layer in base_model.layers[:-num_layers]:
        layer.trainable = False
    
    # Recompile with lower learning rate
    model.compile(
        optimizer=optimizers.Adam(learning_rate=1e-5),  # Much lower LR
        loss=tf.keras.losses.CategoricalCrossentropy(label_smoothing=0.1),
        metrics=['accuracy']
    )
    
    return model


def main():
    print("\n" + "="*60)
    print("Plant Disease Classification - FIXED Training Script")
    print("="*60)
    
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
    print(f"Class names saved to: {CLASS_NAMES_PATH}")
    
    # Create model
    print("\nBuilding model...")
    model, base_model = create_model(len(class_names))
    
    # Print model summary
    print("\nModel Architecture:")
    print(f"  Base: EfficientNetB0 (ImageNet weights, frozen)")
    print(f"  Head: GlobalAvgPool -> BN -> Dropout -> Dense(256) -> Dropout -> Dense(38)")
    print(f"  Trainable params: {sum([tf.keras.backend.count_params(w) for w in model.trainable_weights]):,}")
    
    # Get callbacks
    callbacks = get_callbacks()
    
    # ==================== PHASE 1: Train classifier head ====================
    print("\n" + "="*50)
    print("PHASE 1: Training classifier head (base model frozen)")
    print("="*50)
    
    history = model.fit(
        train_gen,
        epochs=EPOCHS,
        validation_data=val_gen,
        callbacks=callbacks,
        verbose=1
    )
    
    # ==================== PHASE 2: Fine-tuning ====================
    print("\n" + "="*50)
    print("PHASE 2: Fine-tuning (unfreezing top 20 layers)")
    print("="*50)
    
    model = unfreeze_layers(model, base_model, num_layers=20)
    
    # Count trainable params after unfreezing
    trainable_params = sum([tf.keras.backend.count_params(w) for w in model.trainable_weights])
    print(f"Trainable params after unfreezing: {trainable_params:,}")
    
    history_fine = model.fit(
        train_gen,
        epochs=EPOCHS + FINE_TUNE_EPOCHS,
        initial_epoch=EPOCHS,
        validation_data=val_gen,
        callbacks=callbacks,
        verbose=1
    )
    
    # ==================== Evaluation ====================
    print("\n" + "="*50)
    print("Final Evaluation")
    print("="*50)
    
    results = model.evaluate(val_gen, verbose=1)
    print(f"\nValidation Loss: {results[0]:.4f}")
    print(f"Validation Accuracy: {results[1]*100:.2f}%")
    
    # Save final model
    final_path = os.path.join(MODEL_DIR, 'final_model.keras')
    model.save(final_path)
    print(f"\nFinal model saved to: {final_path}")
    
    # Training summary
    best_val_acc = max(history.history['val_accuracy'] + history_fine.history['val_accuracy'])
    print("\n" + "="*60)
    print("TRAINING COMPLETE!")
    print("="*60)
    print(f"Best Validation Accuracy: {best_val_acc*100:.2f}%")
    print(f"Model saved to: {BEST_MODEL_PATH}")
    
    return model, history, history_fine


if __name__ == '__main__':
    main()