"""Crop product photography out of Chinese wholesale sheets onto white HD squares.

Falls back to generated clean assets when a sheet has no usable product crop.
"""

from __future__ import annotations

import io
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

ROOT = Path(r"e:\Toys Lover")
PRODUCTS = ROOT / "public" / "images" / "products"
ASSETS = Path(r"C:\Users\Nouman Faiz\.cursor\projects\e-Toys-Lover\assets")
CANVAS = 1000
INNER = 0.88

# Packet / known Chinese marketing sheets that must not stay as factory art
FORCE_CLEAN = [
    "squeeze-bear-fruit-hat-packet",
    "squeeze-cheese-packet",
    "moldable-cheese-squishy-packet",
    "funny-face-cheese-diy-packet",
    "crystal-strawberry-squishy-packet",
    "funny-face-fruit-squishy-packet",
    "stress-buster-fruit-bottle-packet",
    "coconut-squishy-packet",
    "stress-buster-fruit-bear-packet",
    "simulation-soap-squeeze-packet",
    "chiboki-decompression-tube-packet",
    "glow-pearl-squishy-packet",
]

GENERATED = {
    "squeeze-bear-fruit-hat-packet": "squeeze-bear-fruit-hat-clean.jpg",
}


def looks_like_sheet(bgr: np.ndarray) -> bool:
    h, w = bgr.shape[:2]
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    # dense dark text on bright bg
    bright = (gray > 200).mean()
    dark = (gray < 80).mean()
    edges = cv2.Canny(gray, 60, 140).mean()
    # many thin lines / callouts
    return (bright > 0.35 and dark > 0.04 and edges > 12) or edges > 18


def largest_product_crop(im: Image.Image) -> Image.Image | None:
    """Keep the chunkiest non-paper content block (toys / boxes), drop text columns."""
    rgb = np.asarray(im.convert("RGB"))
    h, w = rgb.shape[:2]
    pix = rgb.astype(np.float32)
    white = np.array([255.0, 255.0, 255.0])
    dist = np.linalg.norm(pix - white, axis=2)
    mask = (dist > 18).astype(np.uint8) * 255
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8), 2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8), 1)
    num, labels, stats, _ = cv2.connectedComponentsWithStats(mask, 8)
    best = None
    best_score = 0.0
    area_img = h * w
    for i in range(1, num):
        x, y, bw, bh, area = stats[i]
        if area < area_img * 0.04:
            continue
        # Prefer square-ish / chunky product clusters over tall thin text columns
        ratio = bw / max(bh, 1)
        if ratio < 0.35 or ratio > 3.8:
            continue
        # Penalize far-left text columns on sheets
        left_penalty = 0.55 if x < w * 0.12 and bw < w * 0.35 else 1.0
        score = area * left_penalty * min(ratio, 1 / max(ratio, 0.01))
        if score > best_score:
            best_score = score
            pad = int(0.03 * max(h, w))
            best = (
                max(0, x - pad),
                max(0, y - pad),
                min(w, x + bw + pad),
                min(h, y + bh + pad),
            )
    if not best:
        return None
    return im.crop(best)


def to_white_square(crop: Image.Image) -> Image.Image:
    crop = ImageOps.exif_transpose(crop).convert("RGB")
    crop = ImageEnhance.Color(crop).enhance(1.08)
    crop = ImageEnhance.Contrast(crop).enhance(1.06)
    crop = ImageEnhance.Sharpness(crop).enhance(1.18)
    crop = crop.filter(ImageFilter.UnsharpMask(radius=1.0, percent=110, threshold=2))
    fitted = crop.copy()
    fitted.thumbnail((int(CANVAS * INNER), int(CANVAS * INNER)), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (CANVAS, CANVAS), (255, 255, 255))
    canvas.paste(fitted, ((CANVAS - fitted.width) // 2, (CANVAS - fitted.height) // 2))
    return canvas


def save(im: Image.Image, path: Path) -> None:
    buf = io.BytesIO()
    im.save(buf, format="JPEG", quality=90, optimize=True, progressive=True, subsampling=1)
    path.write_bytes(buf.getvalue())


def process_slug(slug: str) -> str:
    dest = PRODUCTS / f"{slug}.jpg"
    gen = GENERATED.get(slug)
    if gen and (ASSETS / gen).exists():
        canvas = to_white_square(Image.open(ASSETS / gen))
        save(canvas, dest)
        return "generated"

    if not dest.exists():
        return "missing"

    im = ImageOps.exif_transpose(Image.open(dest)).convert("RGB")
    bgr = cv2.cvtColor(np.asarray(im), cv2.COLOR_RGB2BGR)
    if not looks_like_sheet(bgr) and slug not in FORCE_CLEAN:
        canvas = to_white_square(im)
        save(canvas, dest)
        return "refresh"

    crop = largest_product_crop(im)
    if crop is None or min(crop.size) < 180:
        # Unusable sheet — blank out with a soft placeholder product area removed:
        # mark for catalog removal by writing a sentinel tiny white file? better return remove
        return "remove"

    canvas = to_white_square(crop)
    save(canvas, dest)
    return "cropped"


def main() -> None:
    # Process all force-clean + any sheet-like products in public
    targets = set(FORCE_CLEAN)
    for path in sorted(PRODUCTS.glob("*.jpg")):
        try:
            bgr = cv2.cvtColor(np.asarray(Image.open(path).convert("RGB")), cv2.COLOR_RGB2BGR)
            if looks_like_sheet(bgr):
                targets.add(path.stem)
        except Exception:
            continue

    print(f"cleaning {len(targets)} sheet-like images")
    remove: list[str] = []
    counts: dict[str, int] = {}
    for slug in sorted(targets):
        note = process_slug(slug)
        counts[note] = counts.get(note, 0) + 1
        if note == "remove":
            remove.append(slug)
            print("REMOVE", slug)
        elif note != "refresh":
            print(note, slug)
    print("done", counts)
    out = ROOT / "scripts" / "remove-chinese-slugs.txt"
    out.write_text("\n".join(remove), encoding="utf-8")
    print("wrote", out, "count", len(remove))


if __name__ == "__main__":
    main()
