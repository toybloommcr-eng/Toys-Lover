"""Stronger scrub for leftover Chinese / factory-spec text on marketing sheets."""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

ROOT = Path(r"e:\Toys Lover")
PRODUCT_DIR = ROOT / "public" / "images" / "products"
CATEGORY_DIR = ROOT / "public" / "images" / "categories"
CANVAS = 1600

# Known marketing sheets that still carry Chinese / factory specs
PRIORITY = [
    "candy-house-bath-bombs",
    "ocean-series-bath-bombs",
    "mermaid-bath-bomb-gift",
    "animal-bath-bomb-gift",
    "sea-bath-bomb-gift",
    "light-up-shutter-glasses",
    "dumpling-face-squishy-24",
    "fruit-combo-squishy",
    "soft-cotton-fruit-squishy",
    "big-into-energy-surprise",
    "needoh-tis-the-squeeze",
    "squishy-surprise-bag",
]


def scrub(bgr: np.ndarray) -> np.ndarray:
    h, w = bgr.shape[:2]
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)

    mask = np.zeros((h, w), np.uint8)

    # Hot pink / magenta factory backgrounds — wipe dark glyphs + red Chinese pills
    pink = cv2.inRange(hsv, (135, 50, 80), (175, 255, 255))
    pink |= cv2.inRange(hsv, (0, 70, 120), (15, 255, 255))
    if pink.mean() > 8:
        dark = (gray < 100).astype(np.uint8) * 255
        # Dilate pink so text sitting on pink is included
        pink_d = cv2.dilate(pink, np.ones((11, 11), np.uint8), 1)
        mask |= cv2.bitwise_and(dark, pink_d)
        # Red label pills ("内藏玩具")
        red = cv2.inRange(hsv, (0, 120, 120), (12, 255, 255))
        red |= cv2.inRange(hsv, (165, 120, 120), (180, 255, 255))
        mask |= cv2.dilate(red, np.ones((9, 9), np.uint8), 1)
        # Dimension callouts (cm numbers) — small dark blobs on pink
        num, labels, stats, _ = cv2.connectedComponentsWithStats(cv2.bitwise_and(dark, pink_d), 8)
        for i in range(1, num):
            area = stats[i, cv2.CC_STAT_AREA]
            bw, bh = stats[i, cv2.CC_STAT_WIDTH], stats[i, cv2.CC_STAT_HEIGHT]
            if 8 < area < h * w * 0.015 and bw < w * 0.35 and bh < h * 0.1:
                mask[labels == i] = 255

    # White text on black (catalogue grids)
    v = hsv[:, :, 2]
    if (v < 50).mean() > 0.3:
        bright = cv2.inRange(hsv, (0, 0, 190), (180, 90, 255))
        band = np.zeros((h, w), np.uint8)
        band[: int(h * 0.24)] = 255
        band[int(h * 0.76) :] = 255
        band[:, : int(w * 0.1)] = 255
        mask |= cv2.dilate(cv2.bitwise_and(bright, band), np.ones((5, 3), np.uint8), 2)

    # White sticker / info cards
    white = cv2.inRange(hsv, (0, 0, 220), (180, 45, 255))
    white = cv2.morphologyEx(white, cv2.MORPH_CLOSE, np.ones((13, 13), np.uint8), 2)
    num, labels, stats, _ = cv2.connectedComponentsWithStats(white, 8)
    for i in range(1, num):
        x, y, bw, bh, area = stats[i]
        if h * w * 0.015 < area < h * w * 0.35 and y > h * 0.35:
            roi = gray[y : y + bh, x : x + bw]
            if roi.size and cv2.Canny(roi, 40, 120).mean() > 5:
                mask[y : y + bh, x : x + bw] = 255

    if mask.mean() < 0.0005:
        return bgr
    mask = cv2.dilate(mask, np.ones((5, 5), np.uint8), 1)
    return cv2.inpaint(bgr, mask, 6, cv2.INPAINT_TELEA)


def rebuild_bath_sheet(bgr: np.ndarray) -> np.ndarray:
    """Keep the product box + charm strip; drop Chinese / cm clutter onto clean pink."""
    h, w = bgr.shape[:2]
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    # Non-pink content (product photography)
    pink = cv2.inRange(hsv, (135, 40, 70), (175, 255, 255))
    pink |= cv2.inRange(hsv, (0, 50, 110), (18, 255, 255))
    content = cv2.bitwise_not(pink)
    content = cv2.morphologyEx(content, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8), 1)
    content = cv2.morphologyEx(content, cv2.MORPH_CLOSE, np.ones((21, 21), np.uint8), 2)
    num, labels, stats, _ = cv2.connectedComponentsWithStats(content, 8)
    keep = np.zeros((h, w), np.uint8)
    area_img = h * w
    boxes = []
    for i in range(1, num):
        x, y, bw, bh, area = stats[i]
        if area < area_img * 0.04:
            continue
        # Drop thin text-only strips that are mostly white with Chinese
        roi = bgr[y : y + bh, x : x + bw]
        if roi.size == 0:
            continue
        white_ratio = float((cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY) > 230).mean())
        # Prefer chunky product photos / boxes, skip pure white Chinese lists
        if white_ratio > 0.75 and bh < h * 0.35 and bw < w * 0.4:
            continue
        boxes.append((area, x, y, bw, bh))
        keep[y : y + bh, x : x + bw] = 255
    if not boxes:
        return scrub(bgr)
    # Soft pink studio canvas
    canvas = np.full_like(bgr, (235, 105, 185))  # BGR soft magenta
    # Paste kept regions
    ys, xs = np.where(keep > 0)
    if len(xs) == 0:
        return scrub(bgr)
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    pad = 24
    x0, y0 = max(0, x0 - pad), max(0, y0 - pad)
    x1, y1 = min(w - 1, x1 + pad), min(h - 1, y1 + pad)
    crop = bgr[y0 : y1 + 1, x0 : x1 + 1].copy()
    crop = scrub(crop)
    # Center crop on canvas square later via beautify pipeline
    return crop


def finish(im: Image.Image, dark_ok: bool = False) -> Image.Image:
    im = ImageOps.exif_transpose(im).convert("RGB")
    im = ImageEnhance.Color(im).enhance(1.2)
    im = ImageEnhance.Contrast(im).enhance(1.14)
    im = ImageEnhance.Brightness(im).enhance(1.03)
    im = ImageEnhance.Sharpness(im).enhance(1.4)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.5, percent=150, threshold=2))
    arr = np.asarray(im)
    h, w = arr.shape[:2]
    side = min(h, w)
    # cover square
    scale = CANVAS / side
    nh, nw = int(h * scale), int(w * scale)
    im2 = im.resize((nw, nh), Image.Resampling.LANCZOS)
    left, top = (nw - CANVAS) // 2, (nh - CANVAS) // 2
    im2 = im2.crop((left, top, left + CANVAS, top + CANVAS))
    bg = (12, 12, 16) if dark_ok else (255, 255, 255)
    # If image already square canvas size, return
    if im2.size == (CANVAS, CANVAS):
        return im2
    out = Image.new("RGB", (CANVAS, CANVAS), bg)
    out.paste(im2, (0, 0))
    return out


def process(path: Path) -> None:
    bgr = cv2.cvtColor(np.asarray(Image.open(path).convert("RGB")), cv2.COLOR_RGB2BGR)
    name = path.stem
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    pinkish = float(
        (
            cv2.inRange(hsv, (135, 40, 70), (175, 255, 255)).mean()
            + cv2.inRange(hsv, (0, 50, 110), (18, 255, 255)).mean()
        )
        / 255
        * 100
    )
    if "bath" in name or pinkish > 18:
        bgr = rebuild_bath_sheet(bgr)
    else:
        bgr = scrub(bgr)
    dark = float((cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY) < 40).mean()) > 0.4
    im = Image.fromarray(cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB))
    out = finish(im, dark_ok=dark)
    out.save(path, format="JPEG", quality=95, optimize=True, subsampling=0)


def main() -> None:
    targets: list[Path] = []
    for slug in PRIORITY:
        for folder in (PRODUCT_DIR, CATEGORY_DIR):
            p = folder / f"{slug}.jpg"
            if p.exists():
                targets.append(p)
    # Also sweep any highly pink marketing leftovers
    for p in PRODUCT_DIR.glob("*.jpg"):
        if p in targets:
            continue
        bgr = cv2.imread(str(p))
        if bgr is None:
            continue
        hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
        pink = cv2.inRange(hsv, (135, 50, 80), (175, 255, 255)).mean()
        if pink > 25:
            targets.append(p)

    # Refresh category glow glasses from cleaned product
    print("scrubbing", len(targets), "priority images")
    for p in targets:
        try:
            process(p)
            print(" OK", p.name)
        except Exception as exc:  # noqa: BLE001
            print("FAIL", p.name, exc)

    src = PRODUCT_DIR / "light-up-shutter-glasses.jpg"
    dst = CATEGORY_DIR / "light-up-glasses.jpg"
    if src.exists():
        Image.open(src).convert("RGB").save(dst, quality=95, optimize=True)
        print("synced category light-up-glasses")

    for slug, cat in [
        ("candy-house-bath-bombs", "bath-bomb-gifts"),
        ("mermaid-bath-bomb-gift", "bath-bomb-gifts"),
    ]:
        s = PRODUCT_DIR / f"{slug}.jpg"
        d = CATEGORY_DIR / f"{cat}.jpg"
        if s.exists() and slug.startswith("mermaid"):
            Image.open(s).convert("RGB").save(d, quality=95, optimize=True)
            print("synced", cat)


if __name__ == "__main__":
    main()
