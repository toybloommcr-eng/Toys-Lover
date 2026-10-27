"""Remove Chinese / wholesale text overlays and beautify every catalog photo."""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

ROOT = Path(r"e:\Toys Lover")
DIRS = [
    ROOT / "public" / "images" / "products",
    ROOT / "public" / "images" / "categories",
]
CANVAS = 1600
FILL = 0.99


def to_cv(im: Image.Image) -> np.ndarray:
    return cv2.cvtColor(np.asarray(im.convert("RGB")), cv2.COLOR_RGB2BGR)


def to_pil(bgr: np.ndarray) -> Image.Image:
    return Image.fromarray(cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB))


def remove_white_text_on_dark(bgr: np.ndarray) -> np.ndarray:
    """Knock out bright Chinese labels on black / near-black backgrounds."""
    h, w = bgr.shape[:2]
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    v = hsv[:, :, 2]
    dark_ratio = float((v < 45).mean())
    if dark_ratio < 0.35:
        return bgr

    # Bright text / numbers
    bright = cv2.inRange(hsv, (0, 0, 185), (180, 80, 255))
    # Prefer top/bottom/side bands where catalogues put Chinese copy
    band = np.zeros((h, w), dtype=np.uint8)
    band[: int(h * 0.22), :] = 255
    band[int(h * 0.78) :, :] = 255
    band[:, : int(w * 0.08)] = 255
    band[:, int(w * 0.92) :] = 255
    mask = cv2.bitwise_and(bright, band)
    # Also catch floating white Chinese anywhere on black
    mask2 = cv2.bitwise_and(bright, cv2.inRange(v, 0, 70))  # wrong - need neighborhood
    # Dilate bright blobs that sit on dark pixels
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 3))
    mask = cv2.dilate(mask, kernel, iterations=2)
    # Extra: small bright components over dark bg in full frame
    full_bright = cv2.dilate(bright, kernel, iterations=1)
    dark = (v < 55).astype(np.uint8) * 255
    dark = cv2.dilate(dark, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)), 1)
    float_text = cv2.bitwise_and(full_bright, dark)
    # Keep only relatively small text-ish blobs (not the glowing glasses)
    num, labels, stats, _ = cv2.connectedComponentsWithStats(float_text, 8)
    float_clean = np.zeros_like(float_text)
    area_img = h * w
    for i in range(1, num):
        area = stats[i, cv2.CC_STAT_AREA]
        bw = stats[i, cv2.CC_STAT_WIDTH]
        bh = stats[i, cv2.CC_STAT_HEIGHT]
        if area < area_img * 0.02 and area > 20 and max(bw, bh) < max(h, w) * 0.35:
            # Prefer wide short text lines or small digits
            if bw > bh * 1.2 or (bw < w * 0.12 and bh < h * 0.12):
                float_clean[labels == i] = 255
    mask = cv2.bitwise_or(mask, float_clean)
    if mask.mean() < 0.001:
        return bgr
    return cv2.inpaint(bgr, mask, 4, cv2.INPAINT_TELEA)


def remove_spec_panels(bgr: np.ndarray) -> np.ndarray:
    """Remove solid-colour wholesale / Chinese spec panels (pink/white blocks of text)."""
    h, w = bgr.shape[:2]
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    # Near-white panels
    white = cv2.inRange(hsv, (0, 0, 210), (180, 40, 255))
    # Hot pink / magenta marketing panels common on China sheets
    pink = cv2.inRange(hsv, (140, 40, 120), (175, 255, 255))
    pink2 = cv2.inRange(hsv, (0, 60, 140), (12, 255, 255))
    panels = cv2.bitwise_or(white, cv2.bitwise_or(pink, pink2))
    panels = cv2.morphologyEx(panels, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8), iterations=2)

    num, labels, stats, _ = cv2.connectedComponentsWithStats(panels, 8)
    mask = np.zeros((h, w), dtype=np.uint8)
    area_img = h * w
    for i in range(1, num):
        x, y, bw, bh, area = stats[i]
        if area < area_img * 0.03:
            continue
        # Spec blocks tend to sit on edges / corners and be rectangular
        on_edge = x < w * 0.08 or y < h * 0.08 or x + bw > w * 0.92 or y + bh > h * 0.72
        rectangular = 0.2 < (bw / max(bh, 1)) < 5.5
        if on_edge and rectangular and area < area_img * 0.45:
            # Confirm looks like text: high local contrast inside
            roi = cv2.cvtColor(bgr[y : y + bh, x : x + bw], cv2.COLOR_BGR2GRAY)
            if roi.size == 0:
                continue
            edges = cv2.Canny(roi, 60, 140)
            if edges.mean() > 8:  # busy with glyphs
                mask[y : y + bh, x : x + bw] = 255

    # Also white warehouse sticker boxes (bottom-right info cards)
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    _, th = cv2.threshold(gray, 235, 255, cv2.THRESH_BINARY)
    th = cv2.morphologyEx(th, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8), 2)
    num, labels, stats, _ = cv2.connectedComponentsWithStats(th, 8)
    for i in range(1, num):
        x, y, bw, bh, area = stats[i]
        if area_img * 0.01 < area < area_img * 0.2 and y > h * 0.45 and bw > w * 0.12:
            roi = gray[y : y + bh, x : x + bw]
            if roi.size and cv2.Canny(roi, 50, 120).mean() > 6:
                mask[y : y + bh, x : x + bw] = 255

    if mask.mean() < 0.002:
        return bgr
    mask = cv2.dilate(mask, np.ones((7, 7), np.uint8), 1)
    return cv2.inpaint(bgr, mask, 5, cv2.INPAINT_TELEA)


def remove_dimension_callouts(bgr: np.ndarray) -> np.ndarray:
    """Remove thin black measurement lines / cm labels on bright marketing sheets."""
    h, w = bgr.shape[:2]
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    # Dark thin strokes on bright bg
    bright_bg = gray > 180
    if bright_bg.mean() < 0.25:
        return bgr
    edges = cv2.Canny(gray, 80, 160)
    # Keep long thin horizontal/vertical lines typical of dimension rulers
    horiz = cv2.morphologyEx(edges, cv2.MORPH_OPEN, np.ones((1, 25), np.uint8))
    vert = cv2.morphologyEx(edges, cv2.MORPH_OPEN, np.ones((25, 1), np.uint8))
    lines = cv2.bitwise_or(horiz, vert)
    # Small dark text near those lines
    dark = (gray < 90).astype(np.uint8) * 255
    dark = cv2.bitwise_and(dark, (bright_bg.astype(np.uint8) * 255))
    num, labels, stats, _ = cv2.connectedComponentsWithStats(dark, 8)
    text = np.zeros_like(dark)
    for i in range(1, num):
        area = stats[i, cv2.CC_STAT_AREA]
        bw = stats[i, cv2.CC_STAT_WIDTH]
        bh = stats[i, cv2.CC_STAT_HEIGHT]
        if 15 < area < h * w * 0.01 and bw < w * 0.25 and bh < h * 0.08:
            text[labels == i] = 255
    mask = cv2.bitwise_or(lines, text)
    mask = cv2.dilate(mask, np.ones((3, 3), np.uint8), 1)
    if mask.mean() < 0.001:
        return bgr
    return cv2.inpaint(bgr, mask, 3, cv2.INPAINT_TELEA)


def content_box(rgb: np.ndarray) -> tuple[int, int, int, int]:
    h, w = rgb.shape[:2]
    white = np.array([255.0, 255.0, 255.0])
    cream = np.array([255.0, 244.0, 232.0])
    black = np.array([0.0, 0.0, 0.0])
    dist_w = np.linalg.norm(rgb.astype(np.float32) - white, axis=2)
    dist_c = np.linalg.norm(rgb.astype(np.float32) - cream, axis=2)
    dist_b = np.linalg.norm(rgb.astype(np.float32) - black, axis=2)
    if (dist_b < 28).mean() > 0.5:
        # Black-bg product collage — use non-black content, ignore faint text leftovers
        mask = dist_b > 40
        if mask.mean() < 0.02:
            return 0, 0, w - 1, h - 1
        ys, xs = np.where(mask)
        pad = int(0.02 * max(w, h))
        return max(0, xs.min() - pad), max(0, ys.min() - pad), min(w - 1, xs.max() + pad), min(h - 1, ys.max() + pad)
    dist = np.minimum(dist_w, dist_c)
    mask = dist > 16
    if mask.mean() < 0.01:
        mask = dist > 9
    if mask.mean() < 0.005:
        return 0, 0, w - 1, h - 1
    ys, xs = np.where(mask)
    pad = int(0.02 * max(w, h))
    return max(0, xs.min() - pad), max(0, ys.min() - pad), min(w - 1, xs.max() + pad), min(h - 1, ys.max() + pad)


def cover_square(im: Image.Image, side: int) -> Image.Image:
    w, h = im.size
    scale = side / min(w, h)
    nw, nh = max(side, int(round(w * scale))), max(side, int(round(h * scale)))
    resized = im.resize((nw, nh), Image.Resampling.LANCZOS)
    left, top = (nw - side) // 2, (nh - side) // 2
    return resized.crop((left, top, left + side, top + side))


def beautify(im: Image.Image) -> Image.Image:
    im = ImageOps.exif_transpose(im).convert("RGB")
    # Punchy retail look
    im = ImageEnhance.Color(im).enhance(1.18)
    im = ImageEnhance.Contrast(im).enhance(1.12)
    im = ImageEnhance.Brightness(im).enhance(1.04)
    im = ImageEnhance.Sharpness(im).enhance(1.35)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.4, percent=140, threshold=2))
    # Soft warm lift without washing whites
    arr = np.asarray(im).astype(np.float32)
    arr[..., 0] = np.clip(arr[..., 0] * 1.02 + 2, 0, 255)  # slight warm red
    arr[..., 2] = np.clip(arr[..., 2] * 0.99, 0, 255)
    # Gentle vignette for focus
    h, w = arr.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    cy, cx = h / 2, w / 2
    r = np.sqrt(((yy - cy) / cy) ** 2 + ((xx - cx) / cx) ** 2)
    vignette = np.clip(1.08 - 0.18 * r, 0.82, 1.08)[..., None]
    arr = np.clip(arr * vignette, 0, 255)
    return Image.fromarray(arr.astype(np.uint8))


def process(path: Path) -> dict:
    original = Image.open(path)
    bgr = to_cv(original)
    before = bgr.copy()
    bgr = remove_white_text_on_dark(bgr)
    bgr = remove_spec_panels(bgr)
    bgr = remove_dimension_callouts(bgr)
    im = beautify(to_pil(bgr))
    rgb = np.asarray(im)
    l, t, r, b = content_box(rgb)
    crop = im.crop((l, t, r + 1, b + 1))
    side = int(CANVAS * FILL)
    filled = cover_square(crop, side)
    canvas = Image.new("RGB", (CANVAS, CANVAS), (255, 255, 255))
    # For dark product shots keep a soft charcoal studio instead of harsh white
    sample = np.asarray(filled)
    if (sample.mean(axis=2) < 40).mean() > 0.45:
        canvas = Image.new("RGB", (CANVAS, CANVAS), (12, 12, 16))
    canvas.paste(filled, ((CANVAS - side) // 2, (CANVAS - side) // 2))
    canvas.save(path, format="JPEG", quality=95, optimize=True, subsampling=0)
    changed = float(np.mean(cv2.absdiff(before, bgr) > 8))
    return {"changed": changed, "kb": path.stat().st_size // 1024}


def main() -> None:
    files: list[Path] = []
    for d in DIRS:
        files.extend(sorted(d.glob("*.jpg")))
    print("cleaning + beautifying", len(files), "images")
    touched = 0
    for i, path in enumerate(files, 1):
        try:
            info = process(path)
            if info["changed"] > 0.002:
                touched += 1
        except Exception as exc:  # noqa: BLE001
            print("FAIL", path.name, exc)
            continue
        if i % 60 == 0 or i == len(files):
            print(f"  {i}/{len(files)} text-clean touches ~{touched}")
    print("done. images with visible cleanup:", touched)


if __name__ == "__main__":
    main()
