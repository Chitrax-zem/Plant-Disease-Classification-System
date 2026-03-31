"""
Setup script to organize dataset into train/val splits
"""

import os
import shutil
import random
from pathlib import Path
from tqdm import tqdm

def split_dataset(
    source_dir='data/color',
    train_dir='data/train',
    val_dir='data/val',
    split_ratio=0.8
):
    """
    Split dataset into train and validation sets.
    
    Args:
        source_dir: Path to raw dataset with class folders
        train_dir: Output path for training data
        val_dir: Output path for validation data
        split_ratio: Ratio for training set (0.8 = 80% train)
    """
    source = Path(source_dir)
    train = Path(train_dir)
    val = Path(val_dir)
    
    if not source.exists():
        print(f"Source directory not found: {source_dir}")
        print("\nPlease first download the dataset:")
        print("  python download_dataset.py")
        return False
    
    # Create output directories
    train.mkdir(parents=True, exist_ok=True)
    val.mkdir(parents=True, exist_ok=True)
    
    # Get all class folders
    class_dirs = [d for d in source.iterdir() if d.is_dir()]
    print(f"Found {len(class_dirs)} classes")
    
    # Process each class
    for class_dir in tqdm(class_dirs, desc="Processing classes"):
        class_name = class_dir.name
        
        # Get all images
        valid_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif'}
        images = [f for f in class_dir.iterdir() 
                 if f.suffix.lower() in valid_extensions]
        
        if len(images) == 0:
            print(f"Warning: No images found in {class_name}")
            continue
        
        # Shuffle images
        random.seed(42)
        random.shuffle(images)
        
        # Split
        split_idx = int(len(images) * split_ratio)
        train_images = images[:split_idx]
        val_images = images[split_idx:]
        
        # Create class folders
        (train / class_name).mkdir(exist_ok=True)
        (val / class_name).mkdir(exist_ok=True)
        
        # Copy images
        for img in train_images:
            shutil.copy2(img, train / class_name / img.name)
        
        for img in val_images:
            shutil.copy2(img, val / class_name / img.name)
        
        print(f"  {class_name}: {len(train_images)} train, {len(val_images)} val")
    
    # Summary
    train_count = sum(1 for _ in train.rglob('*') if _.is_file())
    val_count = sum(1 for _ in val.rglob('*') if _.is_file())
    
    print("\n" + "="*50)
    print("Dataset Split Complete!")
    print("="*50)
    print(f"Training images:   {train_count}")
    print(f"Validation images: {val_count}")
    print(f"Total images:      {train_count + val_count}")
    print(f"Classes:           {len(class_dirs)}")
    
    return True


def verify_dataset():
    """Verify the dataset is properly organized"""
    train_path = Path('data/train')
    val_path = Path('data/val')
    
    if not train_path.exists() or not val_path.exists():
        print("Dataset not found. Run split_dataset() first.")
        return False
    
    train_classes = set(d.name for d in train_path.iterdir() if d.is_dir())
    val_classes = set(d.name for d in val_path.iterdir() if d.is_dir())
    
    if train_classes != val_classes:
        print("Warning: Train and val have different classes!")
        print(f"Train only: {train_classes - val_classes}")
        print(f"Val only: {val_classes - train_classes}")
    
    # Count per class
    print("\nImages per class:")
    for cls in sorted(train_classes)[:10]:
        train_count = len(list((train_path / cls).glob('*')))
        val_count = len(list((val_path / cls).glob('*')))
        print(f"  {cls}: {train_count} train, {val_count} val")
    
    if len(train_classes) > 10:
        print(f"  ... and {len(train_classes) - 10} more classes")
    
    return True


if __name__ == '__main__':
    print("="*60)
    print("PlantVillage Dataset Setup")
    print("="*60)
    
    # Step 1: Split dataset
    success = split_dataset()
    
    if success:
        # Step 2: Verify
        print("\nVerifying dataset...")
        verify_dataset()
        
        print("\n" + "="*60)
        print("Ready for training!")
        print("Run: python model/train_model.py")
        print("="*60)