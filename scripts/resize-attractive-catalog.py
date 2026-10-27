"""Resize catalog to clean 1000px HD squares (contain, no distortion).

Chinese scrub runs ONLY on known marketing-sheet products so clean pack
shots are never inpainted / damaged.
"""

from __future__ import annotations

import io
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

ROOT = Path(r"e:\Toys Lover")
DIRS = [
    ROOT / "public" / "images" / "products",
    ROOT / "public" / "images" / "categories",
]

CANVAS = 1000
INNER = 0.90
QUALITY = 90

# Only these (and matching category heroes) get Chinese overlay cleanup
SCRUB_SLUGS = {
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
    "glow-pearl-squishy-packet",
    "funny-face-cheese-diy-packet",
    "funny-face-fruit-squishy-packet",
    "crystal-strawberry-squishy-packet",
    "chiboki-decompression-tube-packet",
    "coconut-squishy-packet",
    "squeeze-cheese-packet",
    "simulation-soap-squeeze-packet",
}


def to_cv(im: Image.Image) -> np.ndarray:
    return cv2.cvtColor(np.asarray(im.convert("RGB")), cv2.COLOR_RGB2BGR)


def to_pil(bgr: np.ndarray) -> Image.Image:
    return Image.fromarray(cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB))


def scrub_chinese(bgr: np.ndarray) -> tuple[np.ndarray, bool]:
    before = bgr.copy()
    h, w = bgr.shape[:2]
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    mask = np.zeros((h, w), np.uint8)

    v = hsv[:, :, 2]
    if (v < 50).mean() > 0.35:
        bright = cv2.inRange(hsv, (0, 0, 190), (180, 80, 255))
        band = np.zeros((h, w), np.uint8)
        band[: int(h * 0.22)] = 255
        band[int(h * 0.78) :] = 255
        band[:, : int(w * 0.08)] = 255
        band[:, int(w * 0.92) :] = 255
        mask |= cv2.dilate(cv2.bitwise_and(bright, band), np.ones((5, 3), np.uint8), 2)

    pink = cv2.inRange(hsv, (135, 55, 90), (175, 255, 255))
    pink |= cv2.inRange(hsv, (0, 80, 130), (12, 255, 255))
    if pink.mean() > 12:
        pink_d = cv2.dilate(pink, np.ones((9, 9), np.uint8), 1)
        dark = (gray < 95).astype(np.uint8) * 255
        mask |= cv2.bitwise_and(dark, pink_d)
        red = cv2.inRange(hsv, (0, 130, 130), (10, 255, 255))
        red |= cv2.inRange(hsv, (168, 130, 130), (180, 255, 255))
        mask |= cv2.dilate(red, np.ones((7, 7), np.uint8), 1)

    white = cv2.inRange(hsv, (0, 0, 225), (180, 40, 255))
    white = cv2.morphologyEx(white, cv2.MORPH_CLOSE, np.ones((11, 11), np.uint8), 2)
    num, labels, stats, _ = cv2.connectedComponentsWithStats(white, 8)
    area_img = h * w
    for i in range(1, num):
        x, y, bw, bh, area = stats[i]
        if area_img * 0.02 < area < area_img * 0.28 and y > h * 0.4:
            roi = gray[y : y + bh, x : x + bw]
            if roi.size and cv2.Canny(roi, 50, 130).mean() > 7:
                if x + bw > w * 0.55 or y + bh > h * 0.75:
                    mask[y : y + bh, x : x + bw] = 255

    if mask.mean() < 0.001:
        return bgr, False
    mask = cv2.dilate(mask, np.ones((5, 5), np.uint8), 1)
    cleaned = cv2.inpaint(bgr, mask, 5, cv2.INPAINT_TELEA)
    changed = float(np.mean(cv2.absdiff(before, cleaned) > 10)) > 0.003
    return cleaned, changed


def content_box(rgb: np.ndarray) -> tuple[int, int, int, int]:
    h, w = rgb.shape[:2]
    white = np.array([255.0, 255.0, 255.0])
    cream = np.array([255.0, 244.0, 232.0])
    black = np.array([0.0, 0.0, 0.0])
    dist_w = np.linalg.norm(rgb.astype(np.float32) - white, axis=2)
    dist_c = np.linalg.norm(rgb.astype(np.float32) - cream, axis=2)
    dist_b = np.linalg.norm(rgb.astype(np.float32) - black, axis=2)

    if (dist_b < 28).mean() > 0.45:
        mask = dist_b > 35
        if mask.mean() < 0.02:
            return 0, 0, w - 1, h - 1
        ys, xs = np.where(mask)
        pad = int(0.03 * max(w, h))
        return (
            max(0, int(xs.min()) - pad),
            max(0, int(ys.min()) - pad),
            min(w - 1, int(xs.max()) + pad),
            min(h - 1, int(ys.max()) + pad),
        )

    dist = np.minimum(dist_w, dist_c)
    mask = dist > 14.0
    if mask.mean() > 0.92 or mask.mean() < 0.01:
        return 0, 0, w - 1, h - 1
    ys, xs = np.where(mask)
    pad = int(0.04 * max(w, h))
    return (
        max(0, int(xs.min()) - pad),
        max(0, int(ys.min()) - pad),
        min(w - 1, int(xs.max()) + pad),
        min(h - 1, int(ys.max()) + pad),
    )


def studio_bg(rgb: np.ndarray) -> tuple[int, int, int]:
    if (rgb.mean(axis=2) < 40).mean() > 0.4:
        return (10, 10, 14)
    return (255, 255, 255)


def beautify(im: Image.Image) -> Image.Image:
    im = ImageOps.exif_transpose(im).convert("RGB")
    im = ImageEnhance.Color(im).enhance(1.1)
    im = ImageEnhance.Contrast(im).enhance(1.07)
    im = ImageEnhance.Brightness(im).enhance(1.02)
    im = ImageEnhance.Sharpness(im).enhance(1.22)
    return im.filter(ImageFilter.UnsharpMask(radius=1.05, percent=115, threshold=2))


def process(path: Path) -> dict:
    slug = path.stem
    original = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    bgr = to_cv(original)
    did_scrub = False
    if slug in SCRUB_SLUGS:
        bgr, did_scrub = scrub_chinese(bgr)

    im = beautify(to_pil(bgr))
    rgb = np.asarray(im)
    left, top, right, bot = content_box(rgb)
    crop = im.crop((left, top, right + 1, bot + 1))
    fitted = crop.copy()
    fitted.thumbnail((int(CANVAS * INNER), int(CANVAS * INNER)), Image.Resampling.LANCZOS)
    bg = studio_bg(np.asarray(crop))
    canvas = Image.new("RGB", (CANVAS, CANVAS), bg)
    canvas.paste(fitted, ((CANVAS - fitted.width) // 2, (CANVAS - fitted.height) // 2))

    buf = io.BytesIO()
    canvas.save(
        buf,
        format="JPEG",
        quality=QUALITY,
        optimize=True,
        progressive=True,
        subsampling=1,
    )
    path.write_bytes(buf.getvalue())
    return {"kb": path.stat().st_size // 1024, "scrubbed": did_scrub}


def main() -> None:
    files: list[Path] = []
    for folder in DIRS:
        files.extend(sorted(folder.glob("*.jpg")))
    print(f"resizing {len(files)} images to {CANVAS}px HD contain ({int(INNER * 100)}%)")
    scrubbed = 0
    for i, path in enumerate(files, 1):
        try:
            info = process(path)
            if info["scrubbed"]:
                scrubbed += 1
                print(f"  scrubbed {path.name}", flush=True)
        except Exception as exc:  # noqa: BLE001
            print("FAIL", path.name, exc, flush=True)
            continue
        if i % 60 == 0 or i == len(files):
            print(f"  {i}/{len(files)} {path.name} {info['kb']}kb", flush=True)
    print(f"done - scrubbed {scrubbed} known Chinese sheets", flush=True)


if __name__ == "__main__":
    main()
