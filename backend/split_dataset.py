import os, random, shutil

train_dir = "data/train"
val_dir = "data/val"

split = 0.2

for cls in os.listdir(train_dir):
    cls_path = os.path.join(train_dir, cls)

    if not os.path.isdir(cls_path):
        continue

    images = os.listdir(cls_path)
    random.shuffle(images)

    val_size = int(len(images) * split)

    os.makedirs(os.path.join(val_dir, cls), exist_ok=True)

    for img in images[:val_size]:
        shutil.move(
            os.path.join(cls_path, img),
            os.path.join(val_dir, cls, img)
        )

print("✅ Dataset split complete")