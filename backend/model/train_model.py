"""
Training script for Plant Disease Classification Model
Uses EfficientNetB0 with transfer learning on PlantVillage dataset
"""

import os
import json
import numpy as np
from datetime import datetime

# Set TensorFlow logging
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
from tensorflow.keras import layers, models, optimizers, regularizers
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import (
    EarlyStopping, 
    ReduceLROnPlateau, 
    ModelCheckpoint,
    TensorBoard,
    CSVLogger
)
from tensorflow.keras.metrics import top_k_categorical_accuracy

# Configuration
IMAGE_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 30
NUM_CLASSES = 38
INPUT_SHAPE = (IMAGE_SIZE, IMAGE_SIZE, 3)

# Data paths - update these to your dataset location
TRAIN_DIR = 'data/train'
VAL_DIR = 'data/val'

# Model save paths
MODEL_DIR = 'model/saved_models'
os.makedirs(MODEL_DIR, exist_ok=True)

BEST_MODEL_PATH = os.path.join(MODEL_DIR, 'best_model.keras')
CLASS_NAMES_PATH = os.path.join(MODEL_DIR, 'class_names.json')
TRAINING_HISTORY_PATH = os.path.join(MODEL_DIR, 'training_history.json')


def create_data_generators():
    """
    Create data generators with augmentation for training and validation.
    
    Returns:
        train_generator, validation_generator, class_indices
    """
    # Training data augmentation
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=30,
        width_shift_range=0.25,
        height_shift_range=0.25,
        shear_range=0.2,
        zoom_range=0.25,
        horizontal_flip=True,
        vertical_flip=True,
        brightness_range=[0.8, 1.2],
        fill_mode='nearest'
    )
    
    # Validation data - only rescaling
    val_datagen = ImageDataGenerator(rescale=1./255)
    
    # Create generators
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


def create_model(num_classes: int = NUM_CLASSES):
    """
    Create EfficientNetB0 model with custom classification head.
    
    Args:
        num_classes: Number of output classes
        
    Returns:
        Compiled Keras model
    """
    # Load EfficientNetB0 base model (pretrained on ImageNet)
    base_model = EfficientNetB0(
        weights='imagenet',
        include_top=False,
        input_shape=INPUT_SHAPE
    )
    
    # Freeze base model layers
    base_model.trainable = False
    
    # Build custom head
    inputs = layers.Input(shape=INPUT_SHAPE)
    
    # Pass through base model
    x = base_model(inputs, training=False)
    
    # Global average pooling
    x = layers.GlobalAveragePooling2D()(x)
    
    # Batch normalization
    x = layers.BatchNormalization()(x)
    
    # First dense layer with L2 regularization
    x = layers.Dense(
        512, 
        activation='relu',
        kernel_regularizer=regularizers.l2(0.001)
    )(x)
    
    # Dropout for regularization
    x = layers.Dropout(0.4)(x)
    
    # Second dense layer
    x = layers.Dense(
        256, 
        activation='relu',
        kernel_regularizer=regularizers.l2(0.001)
    )(x)
    
    # Dropout
    x = layers.Dropout(0.3)(x)
    
    # Output layer
    outputs = layers.Dense(num_classes, activation='softmax')(x)
    
    # Create model
    model = models.Model(inputs, outputs, name='plant_disease_classifier')
    
    # Compile model
    model.compile(
        optimizer=optimizers.Adam(learning_rate=0.001),
        loss=tf.keras.losses.CategoricalCrossentropy(label_smoothing=0.1),
        metrics=['accuracy', top_3_accuracy, top_5_accuracy]
    )
    
    return model, base_model


def top_3_accuracy(y_true, y_pred):
    """Top-3 accuracy metric"""
    return top_k_categorical_accuracy(y_true, y_pred, k=3)


def top_5_accuracy(y_true, y_pred):
    """Top-5 accuracy metric"""
    return top_k_categorical_accuracy(y_true, y_pred, k=5)


def get_callbacks():
    """
    Create training callbacks.
    
    Returns:
        List of Keras callbacks
    """
    callbacks = [
        # Early stopping
        EarlyStopping(
            monitor='val_loss',
            patience=8,
            restore_best_weights=True,
            verbose=1,
            mode='min'
        ),
        
        # Reduce learning rate on plateau
        ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=4,
            min_lr=1e-7,
            verbose=1,
            mode='min'
        ),
        
        # Model checkpoint
        ModelCheckpoint(
            BEST_MODEL_PATH,
            monitor='val_accuracy',
            save_best_only=True,
            mode='max',
            verbose=1
        ),
        
        # CSV logger
        CSVLogger(
            os.path.join(MODEL_DIR, 'training_log.csv'),
            separator=',',
            append=False
        )
    ]
    
    return callbacks


def fine_tune_model(model, base_model, train_generator, validation_generator, callbacks):
    """
    Fine-tune the model by unfreezing some base model layers.
    
    Args:
        model: The trained model
        base_model: The EfficientNetB0 base model
        train_generator: Training data generator
        validation_generator: Validation data generator
        callbacks: List of callbacks
        
    Returns:
        Fine-tuned model and training history
    """
    # Unfreeze the last 20 layers of the base model
    base_model.trainable = True
    
    # Freeze all layers except the last 20
    for layer in base_model.layers[:-20]:
        layer.trainable = False
    
    # Recompile with lower learning rate
    model.compile(
        optimizer=optimizers.Adam(learning_rate=1e-5),
        loss=tf.keras.losses.CategoricalCrossentropy(label_smoothing=0.1),
        metrics=['accuracy', top_3_accuracy, top_5_accuracy]
    )
    
    print("\n" + "="*50)
    print("Starting Fine-tuning Phase")
    print("="*50 + "\n")
    
    # Fine-tune for additional epochs
    fine_tune_epochs = 10
    
    history_fine = model.fit(
        train_generator,
        epochs=fine_tune_epochs,
        validation_data=validation_generator,
        callbacks=callbacks,
        verbose=1
    )
    
    return model, history_fine


def save_class_names(class_indices: dict):
    """
    Save class names to JSON file.
    
    Args:
        class_indices: Dictionary mapping class names to indices
    """
    # Reverse the dictionary to get index -> class name
    idx_to_class = {v: k for k, v in class_indices.items()}
    
    # Create list in order
    class_names = [idx_to_class[i] for i in range(len(idx_to_class))]
    
    # Save to JSON
    with open(CLASS_NAMES_PATH, 'w') as f:
        json.dump(class_names, f, indent=2)
    
    print(f"Saved {len(class_names)} class names to {CLASS_NAMES_PATH}")


def save_training_history(history):
    """
    Save training history to JSON file.
    
    Args:
        history: Keras training history object
    """
    history_dict = {
        'accuracy': [float(x) for x in history.history['accuracy']],
        'val_accuracy': [float(x) for x in history.history['val_accuracy']],
        'loss': [float(x) for x in history.history['loss']],
        'val_loss': [float(x) for x in history.history['val_loss']],
        'top_3_accuracy': [float(x) for x in history.history.get('top_3_accuracy', [])],
        'val_top_3_accuracy': [float(x) for x in history.history.get('val_top_3_accuracy', [])],
        'top_5_accuracy': [float(x) for x in history.history.get('top_5_accuracy', [])],
        'val_top_5_accuracy': [float(x) for x in history.history.get('val_top_5_accuracy', [])],
        'lr': [float(x) for x in history.history.get('lr', [])]
    }
    
    with open(TRAINING_HISTORY_PATH, 'w') as f:
        json.dump(history_dict, f, indent=2)
    
    print(f"Saved training history to {TRAINING_HISTORY_PATH}")


def main():
    """Main training function"""
    print("\n" + "="*60)
    print("Plant Disease Classification Model Training")
    print("Using EfficientNetB0 Transfer Learning")
    print("="*60 + "\n")
    
    # Check for GPU
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        print(f"Found {len(gpus)} GPU(s)")
        for gpu in gpus:
            print(f"  - {gpu}")
    else:
        print("No GPU found, training on CPU")
    
    print("\n" + "-"*50)
    print("Creating data generators...")
    print("-"*50)
    
    # Create data generators
    train_generator, validation_generator, class_indices = create_data_generators()
    
    # Save class names
    save_class_names(class_indices)
    
    print(f"\nTraining samples: {train_generator.samples}")
    print(f"Validation samples: {validation_generator.samples}")
    print(f"Number of classes: {len(class_indices)}")
    
    print("\n" + "-"*50)
    print("Building model...")
    print("-"*50)
    
    # Create model
    model, base_model = create_model(num_classes=len(class_indices))
    
    # Print model summary
    model.summary()
    
    # Get callbacks
    callbacks = get_callbacks()
    
    print("\n" + "-"*50)
    print("Starting training...")
    print("-"*50)
    
    # Train model
    history = model.fit(
        train_generator,
        epochs=EPOCHS,
        validation_data=validation_generator,
        callbacks=callbacks,
        verbose=1
    )
    
    # Save training history
    save_training_history(history)
    
    print("\n" + "-"*50)
    print("Fine-tuning model...")
    print("-"*50)
    
    # Fine-tune model
    model, history_fine = fine_tune_model(
        model, base_model, train_generator, validation_generator, callbacks
    )
    
    # Save final model
    final_model_path = os.path.join(MODEL_DIR, 'final_model.keras')
    model.save(final_model_path)
    print(f"\nSaved final model to {final_model_path}")
    
    # Evaluate model
    print("\n" + "-"*50)
    print("Evaluating model...")
    print("-"*50)
    
    evaluation = model.evaluate(validation_generator, verbose=1)
    print(f"\nValidation Loss: {evaluation[0]:.4f}")
    print(f"Validation Accuracy: {evaluation[1]:.4f}")
    print(f"Validation Top-3 Accuracy: {evaluation[2]:.4f}")
    print(f"Validation Top-5 Accuracy: {evaluation[3]:.4f}")
    
    print("\n" + "="*60)
    print("Training Complete!")
    print("="*60)
    
    return model, history


if __name__ == '__main__':
    main()