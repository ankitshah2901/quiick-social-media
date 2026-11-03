"""Crop near-white margins off product photos so the product fills the frame (keeps a small border)."""
import os, sys
from PIL import Image, ImageChops

def trim(path):
    im = Image.open(path).convert("RGB")
    diff = ImageChops.difference(im, Image.new("RGB", im.size, (255, 255, 255))).convert("L")
    box = diff.point(lambda v: 255 if v > 18 else 0).getbbox()
    if not box:
        return False
    w, h = box[2] - box[0], box[3] - box[1]
    if w * h > 0.85 * im.width * im.height:
        return False
    pad = int(max(w, h) * 0.06)
    box = (max(0, box[0] - pad), max(0, box[1] - pad), min(im.width, box[2] + pad), min(im.height, box[3] + pad))
    im.crop(box).save(path, quality=88)
    return True

if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "media", "products")
    n = sum(trim(os.path.join(d, f)) for f in os.listdir(d) if f.endswith(".jpg"))
    print("trimmed", n)
