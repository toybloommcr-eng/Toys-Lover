"""Rematch New Products + Innovative packets from local folders.

- Gentle white HD squares (no aggressive oversharpen / painterly look)
- Squeeze Bear: crop the three loose bears only (drop Chinese + dimension lines)
- Other packet sheets: keep largest product cluster; skip if crop fails quality
"""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageOps

ROOT = Path(r"e:\Toys Lover")
PRODUCTS = ROOT / "public" / "images" / "products"
NEW = ROOT / "New Products"
INNOV = ROOT / "Innovative category Squeeshies"
CANVAS = 1000
INNER = 0.90
JPEG_Q = 88

# New Products filename -> slug (must match october import)
NEW_MAP = {
    "1 GBP Each.jpeg": "christmas-super-squishy-box",
    "3D Printed Model.jpeg": "3d-printed-gear-ball",
    "Big Into Energy 6GBP Each.jpeg": "big-into-energy-surprise",
    "fidget spinning ball.jpeg": "fidget-spinning-ball",
    "Fruit Combo Squish 1.5 GBP.jpeg": "fruit-combo-squishy",
    "WhatsApp Image 2026-10-10 at 8.42.55 PM (5).jpeg": "soft-cotton-fruit-squishy",
    "New one.jpeg": "aircraft-tanks-2in1",
    "Super Driver 3.50 GBP.jpeg": "super-driver-red",
    "£2 each 24 in box.jpeg": "dumpling-face-squishy-24",
    "£6 each.jpeg": "rainbow-leopard-plush",
    "£9.50 each item.jpeg": "pink-idol-plush",
    "£9.50 each.jpeg": "needoh-tis-the-squeeze",
    "WhatsApp Image 2026-10-10 at 8.42.55 PM.jpeg": "gear-train-transparent",
    "WhatsApp Image 2026-10-10 at 8.42.55 PM (1).jpeg": "marine-swat-justice-ship",
    "WhatsApp Image 2026-10-10 at 8.42.55 PM (3).jpeg": "colorful-gear-sport-car",
    "WhatsApp Image 2026-10-10 at 8.44.41 PM.jpeg": "mermaid-bath-bomb-gift",
    "WhatsApp Image 2026-10-10 at 8.44.41 PM (1).jpeg": "animal-bath-bomb-gift",
    "WhatsApp Image 2026-10-10 at 8.44.42 PM.jpeg": "sea-bath-bomb-gift",
    "WhatsApp Image 2026-10-10 at 8.44.42 PM (1).jpeg": "candy-house-bath-bombs",
    "WhatsApp Image 2026-10-10 at 8.44.42 PM (2).jpeg": "ocean-series-bath-bombs",
}

# Innovative packet sources (factory sheets / lifestyle). Prefer photo over sheet text.
PACKET_MAP = {
    "squeeze-bear-fruit-hat-packet": INNOV / "WhatsApp Image 2026-10-07 at 4.24.26 PM.jpeg",
    "squeeze-cheese-packet": INNOV / "WhatsApp Image 2026-10-07 at 4.24.12 PM.jpeg",
    "moldable-cheese-squishy-packet": INNOV / "WhatsApp Image 2026-10-07 at 4.24.20 PM.jpeg",
    "funny-face-cheese-diy-packet": INNOV / "WhatsApp Image 2026-10-07 at 4.24.25 PM.jpeg",
    "crystal-strawberry-squishy-packet": INNOV / "WhatsApp Image 2026-10-07 at 4.24.23 PM.jpeg",
    "funny-face-fruit-squishy-packet": INNOV / "WhatsApp Image 2026-10-07 at 4.24.23 PM.jpeg",  # better fruit shot than mislabeled clicker
    "stress-buster-fruit-bottle-packet": INNOV / "WhatsApp Image 2026-10-07 at 4.24.21 PM.jpeg",
    "coconut-squishy-packet": INNOV / "WhatsApp Image 2026-10-07 at 4.24.18 PM.jpeg",
    "stress-buster-fruit-bear-packet": INNOV / "WhatsApp Image 2026-10-07 at 4.24.22 PM.jpeg",
    "simulation-soap-squeeze-packet": INNOV / "WhatsApp Image 2026-10-07 at 4.24.17 PM.jpeg",
    "chiboki-decompression-tube-packet": INNOV / "WhatsApp Image 2026-10-07 at 4.25.17 PM.jpeg",
    "glow-pearl-squishy-packet": INNOV / "WhatsApp Image 2026-10-07 at 4.24.19 PM.jpeg",
}

# Super Driver also has blue variant from same New Products folder
EXTRA_NEW = {
    "Super Driver 3.50 GBP.jpeg": "super-driver-blue",  # same tray photo for sibling SKU if needed
}


def to_white_square(crop: Image.Image, pad_ratio: float = INNER) -> Image.Image:
    crop = ImageOps.exif_transpose(crop).convert("RGB")
    # Light polish only — avoid painterly unsharp
    crop = ImageEnhance.Color(crop).enhance(1.04)
    crop = ImageEnhance.Contrast(crop).enhance(1.03)
    fitted = crop.copy()
    max_side = int(CANVAS * pad_ratio)
    fitted.thumbnail((max_side, max_side), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (CANVAS, CANVAS), (255, 255, 255))
    canvas.paste(fitted, ((CANVAS - fitted.width) // 2, (CANVAS - fitted.height) // 2))
    return canvas


def save(slug: str, im: Image.Image) -> None:
    out = PRODUCTS / f"{slug}.jpg"
    im.save(out, "JPEG", quality=JPEG_Q, optimize=True, progressive=True)
    print(f"wrote {slug} {im.size}", flush=True)


def crop_squeeze_bears(src: Path) -> Image.Image:
    """Sheet layout: Chinese top-left, CDU top-right, box bottom-left, 3 bears bottom-right."""
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    w, h = im.size
    # Focus on bottom-right product cluster (three loose bears)
    left = int(w * 0.38)
    top = int(h * 0.48)
    right = int(w * 0.98)
    bottom = int(h * 0.98)
    region = im.crop((left, top, right, bottom))
    # Drop thin black dimension lines via mild inpaint on dark thin strokes
    bgr = cv2.cvtColor(np.asarray(region), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    # mask near-black thin marks (dimension lines / CM labels)
    dark = (gray < 45).astype(np.uint8) * 255
    # keep thick product shadows out: erode then dilate lightly
    dark = cv2.morphologyEx(dark, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
    # only inpaint sparse line pixels
    if dark.mean() < 12:
        bgr = cv2.inpaint(bgr, dark, 3, cv2.INPAINT_TELEA)
    rgb = Image.fromarray(cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB))
    return to_white_square(rgb, 0.92)


def largest_product_crop(im: Image.Image) -> Image.Image | None:
    rgb = np.asarray(im.convert("RGB"))
    h, w = rgb.shape[:2]
    dist = np.linalg.norm(rgb.astype(np.float32) - np.array([255.0, 255.0, 255.0]), axis=2)
    mask = (dist > 22).astype(np.uint8) * 255
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((17, 17), np.uint8), 2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8), 1)
    num, labels, stats, _ = cv2.connectedComponentsWithStats(mask, 8)
    best = None
    best_score = 0.0
    area_img = h * w
    for i in range(1, num):
        x, y, bw, bh, area = stats[i]
        if area < area_img * 0.05:
            continue
        ratio = bw / max(bh, 1)
        if ratio < 0.4 or ratio > 3.5:
            continue
        # Prefer right/center product photos over left Chinese text columns
        side_bonus = 1.25 if x > w * 0.28 else 0.7
        score = area * side_bonus * min(ratio, 1 / max(ratio, 0.01))
        if score > best_score:
            best_score = score
            pad = int(0.025 * max(h, w))
            best = (
                max(0, x - pad),
                max(0, y - pad),
                min(w, x + bw + pad),
                min(h, y + bh + pad),
            )
    if not best:
        return None
    return im.crop(best)


def has_dense_chinese_left(im: Image.Image) -> bool:
    """Heuristic: bright left band with lots of dark glyphs = wholesale sheet."""
    rgb = np.asarray(im.convert("RGB"))
    h, w = rgb.shape[:2]
    left = rgb[:, : max(1, w // 3)]
    gray = cv2.cvtColor(left, cv2.COLOR_RGB2GRAY)
    bright = (gray > 200).mean()
    dark = (gray < 70).mean()
    edges = cv2.Canny(gray, 50, 120).mean()
    return bright > 0.45 and dark > 0.05 and edges > 10


def process_packet(slug: str, src: Path) -> bool:
    if not src.exists():
        print(f"missing source {slug}", flush=True)
        return False
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    if slug == "squeeze-bear-fruit-hat-packet":
        save(slug, crop_squeeze_bears(src))
        return True
    # Lifestyle stress-buster style: full frame, white pad
    if slug == "stress-buster-fruit-bear-packet" and not has_dense_chinese_left(im):
        save(slug, to_white_square(im, 0.94))
        return True
    if has_dense_chinese_left(im):
        crop = largest_product_crop(im)
        if crop is None:
            print(f"skip no-crop {slug}", flush=True)
            return False
        # Reject if crop is mostly white / tiny
        arr = np.asarray(crop)
        if arr.mean() > 245:
            print(f"skip blank-crop {slug}", flush=True)
            return False
        save(slug, to_white_square(crop, 0.90))
        return True
    save(slug, to_white_square(im, 0.92))
    return True


def process_new() -> int:
    n = 0
    for name, slug in NEW_MAP.items():
        src = NEW / name
        if not src.exists():
            # try unicode pound variants
            alt = None
            for p in NEW.iterdir():
                if p.name.replace("£", "").replace("�", "") == name.replace("£", "").replace("�", ""):
                    alt = p
                    break
            if alt is None:
                print(f"missing new {name}", flush=True)
                continue
            src = alt
        im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
        # Bath bomb sheets often have Chinese side panels — crop product cluster
        if "bath" in slug or has_dense_chinese_left(im):
            crop = largest_product_crop(im) or im
            save(slug, to_white_square(crop, 0.90))
        else:
            save(slug, to_white_square(im, 0.92))
        n += 1
    # Blue Super Driver twin from same source if catalog has it
    blue_src = NEW / "Super Driver 3.50 GBP.jpeg"
    if blue_src.exists() and (PRODUCTS / "super-driver-blue.jpg").exists():
        save("super-driver-blue", to_white_square(Image.open(blue_src).convert("RGB"), 0.92))
        n += 1
    return n


def main() -> None:
    print("rematch New Products…", flush=True)
    print("new", process_new(), flush=True)
    print("rematch Innovative packets…", flush=True)
    ok = 0
    for slug, src in PACKET_MAP.items():
        if process_packet(slug, src):
            ok += 1
    print("packets ok", ok, "/", len(PACKET_MAP), flush=True)
    # Coverage check: every catalog slug has a jpg
    import re

    slugs = set()
    for f in (ROOT / "lib" / "data").glob("*.ts"):
        slugs |= set(re.findall(r'slug:\s*"([^"]+)"', f.read_text(encoding="utf-8")))
    missing = sorted(s for s in slugs if not (PRODUCTS / f"{s}.jpg").exists())
    print("catalog slugs", len(slugs), "missing jpg", len(missing), flush=True)
    if missing[:15]:
        print("missing sample", missing[:15], flush=True)


if __name__ == "__main__":
    main()
