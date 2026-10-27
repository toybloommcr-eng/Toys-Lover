"""Restore glow glasses and rebuild bath bombs without Chinese panels."""

from __future__ import annotations

import subprocess
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

ROOT = Path(r"e:\Toys Lover")
OUT = ROOT / "public" / "images" / "products"
CAT = ROOT / "public" / "images" / "categories"
SRC = ROOT / "New Products"
CANVAS = 1600


def polish(im: Image.Image) -> Image.Image:
    im = ImageOps.exif_transpose(im).convert("RGB")
    im = ImageEnhance.Color(im).enhance(1.15)
    im = ImageEnhance.Contrast(im).enhance(1.1)
    im = ImageEnhance.Sharpness(im).enhance(1.4)
    im = ImageEnhance.Brightness(im).enhance(1.02)
    return im.filter(ImageFilter.UnsharpMask(radius=1.2, percent=135, threshold=2))


def cover(im: Image.Image) -> Image.Image:
    im = polish(im)
    w, h = im.size
    side = min(w, h)
    scale = CANVAS / side
    nw, nh = max(CANVAS, int(w * scale)), max(CANVAS, int(h * scale))
    im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    return im.crop(((nw - CANVAS) // 2, (nh - CANVAS) // 2, (nw - CANVAS) // 2 + CANVAS, (nh - CANVAS) // 2 + CANVAS))


def restore_glasses() -> None:
    raw = subprocess.check_output(
        ["git", "show", "0a447ff:public/images/products/light-up-shutter-glasses.jpg"],
        cwd=str(ROOT),
    )
    tmp = ROOT / "scripts" / "_tmp_glasses.jpg"
    tmp.write_bytes(raw)
    im = Image.open(tmp).convert("RGB")
    bgr = cv2.cvtColor(np.asarray(im), cv2.COLOR_RGB2BGR)
    h, w = bgr.shape[:2]
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    bright = cv2.inRange(hsv, (0, 0, 190), (180, 90, 255))
    band = np.zeros((h, w), np.uint8)
    band[: int(h * 0.2)] = 255
    band[int(h * 0.8) :] = 255
    band[:, : int(w * 0.08)] = 255
    mask = cv2.dilate(cv2.bitwise_and(bright, band), np.ones((5, 3), np.uint8), 2)
    bgr = cv2.inpaint(bgr, mask, 4, cv2.INPAINT_TELEA)
    out = cover(Image.fromarray(cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)))
    out.save(OUT / "light-up-shutter-glasses.jpg", quality=95, optimize=True, subsampling=0)
    out.save(CAT / "light-up-glasses.jpg", quality=95, optimize=True)
    tmp.unlink(missing_ok=True)
    print("glasses restored", (OUT / "light-up-shutter-glasses.jpg").stat().st_size // 1024, "kb")


def rebuild_bath() -> None:
    jobs = [
        # Keep box + charm strip; cut bottom Chinese / cm blocks
        ("candy-house-bath-bombs", "8.44.42 PM (1)", (0.0, 0.0, 1.0, 0.58)),
        ("ocean-series-bath-bombs", "8.44.42 PM (2)", (0.0, 0.0, 1.0, 0.58)),
        ("sea-bath-bomb-gift", "8.44.42 PM.jpeg", (0.04, 0.04, 0.96, 0.96)),
        ("animal-bath-bomb-gift", "8.44.41 PM (1)", (0.02, 0.02, 0.98, 0.98)),
        ("mermaid-bath-bomb-gift", "8.44.41 PM.jpeg", (0.02, 0.02, 0.98, 0.98)),
    ]
    for slug, needle, box in jobs:
        src = next((p for p in SRC.iterdir() if needle.lower() in p.name.lower()), None)
        if not src:
            print("miss", slug)
            continue
        im = Image.open(src).convert("RGB")
        w, h = im.size
        crop = im.crop((int(box[0] * w), int(box[1] * h), int(box[2] * w), int(box[3] * h)))
        bgr = cv2.cvtColor(np.asarray(crop), cv2.COLOR_RGB2BGR)
        hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
        pink = cv2.inRange(hsv, (140, 40, 80), (175, 255, 255)) | cv2.inRange(hsv, (0, 50, 120), (12, 255, 255))
        dark = (cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY) < 95).astype(np.uint8) * 255
        text = cv2.bitwise_and(dark, cv2.dilate(pink, np.ones((15, 15), np.uint8), 1))
        red = cv2.inRange(hsv, (0, 120, 120), (12, 255, 255)) | cv2.inRange(hsv, (165, 120, 120), (180, 255, 255))
        text = cv2.bitwise_or(cv2.dilate(text, np.ones((3, 3), np.uint8), 1), cv2.dilate(red, np.ones((7, 7), np.uint8), 1))
        edges = cv2.Canny(cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY), 80, 160)
        lines = cv2.morphologyEx(edges, cv2.MORPH_OPEN, np.ones((1, 22), np.uint8))
        lines |= cv2.morphologyEx(edges, cv2.MORPH_OPEN, np.ones((22, 1), np.uint8))
        text = cv2.bitwise_or(text, cv2.dilate(lines, np.ones((2, 2), np.uint8), 1))
        if text.mean() > 0.15:
            bgr = cv2.inpaint(bgr, text, 5, cv2.INPAINT_TELEA)
        out = cover(Image.fromarray(cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)))
        out.save(OUT / f"{slug}.jpg", quality=95, optimize=True, subsampling=0)
        print("bath", slug, (OUT / f"{slug}.jpg").stat().st_size // 1024, "kb")

    Image.open(OUT / "mermaid-bath-bomb-gift.jpg").save(CAT / "bath-bomb-gifts.jpg", quality=95, optimize=True)
    print("category bath-bomb-gifts synced")


if __name__ == "__main__":
    restore_glasses()
    rebuild_bath()
    print("done")
