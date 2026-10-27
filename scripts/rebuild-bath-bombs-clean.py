"""Rebuild bath-bomb product shots from New Products originals — product only, no Chinese."""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

ROOT = Path(r"e:\Toys Lover")
SRC = ROOT / "New Products"
OUT = ROOT / "public" / "images" / "products"
CAT = ROOT / "public" / "images" / "categories"
CANVAS = 1600

# Map slug -> source filename patterns
MAP = [
    ("candy-house-bath-bombs", ["8.44.42 PM (1)"]),
    ("ocean-series-bath-bombs", ["8.44.42 PM (2)"]),
    ("sea-bath-bomb-gift", ["8.44.42 PM.jpeg", "8.44.42 PM.jpg"]),
    ("mermaid-bath-bomb-gift", ["8.44.41 PM.jpeg", "8.44.41 PM.jpg"]),
    ("animal-bath-bomb-gift", ["8.44.41 PM (1)"]),
]


def find_src(needles: list[str]) -> Path | None:
    files = list(SRC.iterdir()) if SRC.exists() else []
    for needle in needles:
        for p in files:
            if needle.lower() in p.name.lower() and p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}:
                return p
    return None


def polish(im: Image.Image) -> Image.Image:
    im = ImageOps.exif_transpose(im).convert("RGB")
    im = ImageEnhance.Color(im).enhance(1.12)
    im = ImageEnhance.Contrast(im).enhance(1.1)
    im = ImageEnhance.Sharpness(im).enhance(1.35)
    im = ImageEnhance.Brightness(im).enhance(1.03)
    return im.filter(ImageFilter.UnsharpMask(radius=1.3, percent=130, threshold=2))


def crop_main_product(bgr: np.ndarray) -> np.ndarray:
    """Prefer the retail box / photo area; drop Chinese spec panels on the side/bottom."""
    h, w = bgr.shape[:2]
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)

    # Detect hot pink factory sheet background
    pink = cv2.inRange(hsv, (140, 60, 90), (175, 255, 255))
    pink |= cv2.inRange(hsv, (0, 80, 140), (12, 255, 255))
    pink_ratio = pink.mean() / 255.0

    if pink_ratio > 0.2:
        # Keep left ~62% (usually box + single bomb) and top charm strip if present,
        # but exclude bottom-right Chinese block by taking left+center product cluster.
        content = cv2.bitwise_not(pink)
        content = cv2.morphologyEx(content, cv2.MORPH_CLOSE, np.ones((25, 25), np.uint8), 2)
        # Force-ignore bottom-right quadrant text zone
        content[int(h * 0.62) :, int(w * 0.55) :] = 0
        # Ignore red Chinese pill labels
        red = cv2.inRange(hsv, (0, 120, 120), (12, 255, 255))
        red |= cv2.inRange(hsv, (165, 120, 120), (180, 255, 255))
        content[red > 0] = 0
        ys, xs = np.where(content > 0)
        if len(xs) > 100:
            pad = 16
            x0, x1 = max(0, xs.min() - pad), min(w, xs.max() + pad)
            y0, y1 = max(0, ys.min() - pad), min(h, ys.max() + pad)
            # Prefer wider product crop on the left half if Chinese sits right
            if x1 - x0 < w * 0.45:
                x0, x1 = 0, int(w * 0.68)
                y0, y1 = 0, int(h * 0.78)
            crop = bgr[y0:y1, x0:x1].copy()
            # Paint remaining pink text to soft blush
            chsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
            cpink = cv2.inRange(chsv, (140, 40, 80), (175, 255, 255))
            cpink |= cv2.inRange(chsv, (0, 60, 120), (12, 255, 255))
            # Only fill sparse pink leftover corners, not product
            gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
            fill = cv2.bitwise_and(cpink, (gray > 160).astype(np.uint8) * 255)
            fill = cv2.dilate(fill, np.ones((7, 7), np.uint8), 1)
            blush = np.full_like(crop, (245, 210, 230))  # soft studio blush BGR
            crop = np.where(fill[..., None] > 0, blush, crop)
            # Remove dark Chinese leftovers on blush
            dark = (cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY) < 90).astype(np.uint8) * 255
            near = cv2.dilate(fill, np.ones((21, 21), np.uint8), 1)
            text = cv2.bitwise_and(dark, near)
            if text.mean() > 0.1:
                crop = cv2.inpaint(crop, text, 4, cv2.INPAINT_TELEA)
            return crop

    # Non-pink photos (mermaid lifestyle) — content crop
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 40, 120)
    edges = cv2.dilate(edges, np.ones((5, 5), np.uint8), 1)
    ys, xs = np.where(edges > 0)
    if len(xs) < 50:
        return bgr
    pad = int(0.04 * max(h, w))
    return bgr[
        max(0, ys.min() - pad) : min(h, ys.max() + pad),
        max(0, xs.min() - pad) : min(w, xs.max() + pad),
    ].copy()


def to_square(im: Image.Image) -> Image.Image:
    im = polish(im)
    w, h = im.size
    side = min(w, h)
    scale = CANVAS / side
    nw, nh = max(CANVAS, int(w * scale)), max(CANVAS, int(h * scale))
    im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    left, top = (nw - CANVAS) // 2, (nh - CANVAS) // 2
    return im.crop((left, top, left + CANVAS, top + CANVAS))


def main() -> None:
    for slug, needles in MAP:
        src = find_src(needles)
        if not src:
            print("MISSING source", slug, needles)
            continue
        bgr = cv2.cvtColor(np.asarray(Image.open(src).convert("RGB")), cv2.COLOR_RGB2BGR)
        crop = crop_main_product(bgr)
        im = Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB))
        out = to_square(im)
        dest = OUT / f"{slug}.jpg"
        out.save(dest, format="JPEG", quality=95, optimize=True, subsampling=0)
        print("rebuilt", slug, "from", src.name, f"{dest.stat().st_size//1024}kb")

    # Category hero from mermaid gift (cleanest lifestyle shot)
    hero = OUT / "mermaid-bath-bomb-gift.jpg"
    if hero.exists():
        Image.open(hero).convert("RGB").save(CAT / "bath-bomb-gifts.jpg", quality=95, optimize=True)
        print("category bath-bomb-gifts refreshed")


if __name__ == "__main__":
    main()
