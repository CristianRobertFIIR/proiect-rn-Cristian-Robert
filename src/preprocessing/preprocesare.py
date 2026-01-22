import os
import random
from PIL import Image

RAW = r"C:\Users\Cristian Robert\Desktop\proiect-rn-Cristian-Robert\data\raw"
VAL = r"C:\Users\Cristian Robert\Desktop\proiect-rn-Cristian-Robert\data\validation"

SIZE = (224, 224)
VAL_RATIO = 0.2
EX = (".jpg", ".jpeg", ".png", ".webp", ".jfif", ".bmp", ".tiff")

print("preprocessing script running...")

def save_img(in_path, out_path):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    try:
        img = Image.open(in_path).convert("RGB")
        img = img.resize(SIZE)
        img.save(out_path)
    except Exception as e:
        print(f"Error: {e}")

def main():
    if not os.path.exists(RAW):
        print(f"Error: RAW folder not found at {RAW}")
        return

    print("raw =", os.path.abspath(RAW))
    classes = os.listdir(RAW)
    print("found classes:", classes)

    for cls in classes:
        p = os.path.join(RAW, cls)
        if not os.path.isdir(p):
            continue

        imgs = [f for f in os.listdir(p) if f.lower().endswith(EX)]
        print(f"{cls}: {len(imgs)} imgs")

        if len(imgs) == 0:
            continue

        random.shuffle(imgs)
        cut = int(len(imgs) * (1 - VAL_RATIO))
        val = imgs[cut:]

        print(f"  val: {len(val)}")

        for x in val:
            save_img(os.path.join(p, x), os.path.join(VAL, cls, x))

    print("done.")

if __name__ == "__main__":
    main()