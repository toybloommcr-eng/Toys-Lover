from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageEnhance

ROOT = Path(r"e:\Toys Lover")
OUT = ROOT / "public" / "images" / "products"
CAT = ROOT / "public" / "images" / "categories"

# Glasses: hard-clear Chinese bands
p = OUT / "light-up-shutter-glasses.jpg"
im = np.asarray(Image.open(p).convert("RGB")).copy()
h, w = im.shape[:2]
im[: int(h * 0.17)] = 0
im[int(h * 0.85) :] = 0
im[:, : int(w * 0.045)] = 0
pil = Image.fromarray(im)
pil = ImageEnhance.Color(pil).enhance(1.22)
pil = ImageEnhance.Contrast(pil).enhance(1.14)
pil = ImageEnhance.Sharpness(pil).enhance(1.55)
pil.save(p, quality=95, optimize=True, subsampling=0)
pil.save(CAT / "light-up-glasses.jpg", quality=95, optimize=True)
print("glasses cleared")

for slug in ["candy-house-bath-bombs", "ocean-series-bath-bombs"]:
    path = OUT / f"{slug}.jpg"
    bgr = cv2.cvtColor(np.asarray(Image.open(path).convert("RGB")), cv2.COLOR_RGB2BGR).copy()
    h, w = bgr.shape[:2]
    # clone a clean pink-ish strip over bottom measurement band
    sample = bgr[int(h * 0.88) : int(h * 0.90)].mean(axis=0, keepdims=True).astype(np.uint8)
    bgr[int(h * 0.91) :] = sample
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    pink = cv2.inRange(hsv, (140, 30, 70), (175, 255, 255)) | cv2.inRange(hsv, (0, 40, 100), (15, 255, 255))
    dark = (cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY) < 85).astype(np.uint8) * 255
    edge = np.zeros((h, w), np.uint8)
    edge[: int(h * 0.12)] = 255
    edge[int(h * 0.85) :] = 255
    edge[:, int(w * 0.78) :] = 255
    mask = cv2.dilate(
        cv2.bitwise_and(dark, cv2.bitwise_and(cv2.dilate(pink, np.ones((9, 9), np.uint8), 1), edge)),
        np.ones((5, 5), np.uint8),
        1,
    )
    if mask.mean() > 0.05:
        bgr = cv2.inpaint(bgr, mask, 5, cv2.INPAINT_TELEA)
    out = Image.fromarray(cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB))
    out = ImageEnhance.Color(out).enhance(1.18)
    out = ImageEnhance.Contrast(out).enhance(1.12)
    out = ImageEnhance.Sharpness(out).enhance(1.45)
    out.save(path, quality=95, optimize=True, subsampling=0)
    print("cleaned", slug)

print("done")
