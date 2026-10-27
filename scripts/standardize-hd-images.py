"""Export every catalog photo to a standard HD square with clear, attractive framing."""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

ROOT = Path(r"e:\Toys Lover")
DIRS = [
    ROOT / "public" / "images" / "products",
    ROOT / "public" / "images" / "categories",
]

# Standard storefront size — sharp HD without oversized crop
CANVAS = 1200
INNER = 0.88  # product fills ~88% — full pack visible with clean margin


def polish(im: Image.Image) -> Image.Image:
    im = ImageOps.exif_transpose(im).convert("RGB")
    im = ImageEnhance.Color(im).enhance(1.12)
    im = ImageEnhance.Contrast(im).enhance(1.08)
    im = ImageEnhance.Brightness(im).enhance(1.02)
    im = ImageEnhance.Sharpness(im).enhance(1.28)
    return im.filter(ImageFilter.UnsharpMask(radius=1.1, percent=120, threshold=2))


def content_box(rgb: np.ndarray) -> tuple[int, int, int, int]:
    h, w = rgb.shape[:2]
    white = np.array([255.0, 255.0, 255.0])
    cream = np.array([255.0, 244.0, 232.0])
    black = np.array([0.0, 0.0, 0.0])
    dist_w = np.linalg.norm(rgb.astype(np.float32) - white, axis=2)
    dist_c = np.linalg.norm(rgb.astype(np.float32) - cream, axis=2)
    dist_b = np.linalg.norm(rgb.astype(np.float32) - black, axis=2)

    # Dark studio (neon glasses etc.)
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
    if mask.mean() > 0.92:
        return 0, 0, w - 1, h - 1
    if mask.mean() < 0.015:
        mask = dist > 9.0
    if mask.mean() < 0.005:
        return 0, 0, w - 1, h - 1
    ys, xs = np.where(mask)
    pad = int(0.04 * max(w, h))
    return (
        max(0, int(xs.min()) - pad),
        max(0, int(ys.min()) - pad),
        min(w - 1, int(xs.max()) + pad),
        min(h - 1, int(ys.max()) + pad),
    )


def fit_contain(crop: Image.Image, max_side: int) -> Image.Image:
    """Scale product to fit inside max_side (full product visible)."""
    crop = crop.copy()
    crop.thumbnail((max_side, max_side), Image.Resampling.LANCZOS)
    # Upscale soft/small sources gently for HD clarity
    if max(crop.size) < 720:
        scale = 720 / max(crop.size)
        crop = crop.resize(
            (max(1, int(crop.width * scale)), max(1, int(crop.height * scale))),
            Image.Resampling.LANCZOS,
        )
        crop.thumbnail((max_side, max_side), Image.Resampling.LANCZOS)
    return crop


def studio_bg(rgb: np.ndarray) -> tuple[int, int, int]:
    """Pick white or near-black studio based on source."""
    if (rgb.mean(axis=2) < 40).mean() > 0.4:
        return (10, 10, 14)
    return (255, 255, 255)


def standardize(path: Path) -> None:
    im = polish(Image.open(path))
    rgb = np.asarray(im)
    left, top, right, bot = content_box(rgb)
    crop = im.crop((left, top, right + 1, bot + 1))
    fitted = fit_contain(crop, int(CANVAS * INNER))
    bg = studio_bg(np.asarray(crop))
    canvas = Image.new("RGB", (CANVAS, CANVAS), bg)
    canvas.paste(fitted, ((CANVAS - fitted.width) // 2, (CANVAS - fitted.height) // 2))
    canvas.save(path, format="JPEG", quality=92, optimize=True, subsampling=0)


def main() -> None:
    files: list[Path] = []
    for d in DIRS:
        files.extend(sorted(d.glob("*.jpg")))
    print(f"standardizing {len(files)} images to {CANVAS}px HD (contain {int(INNER*100)}%)")
    for i, path in enumerate(files, 1):
        try:
            standardize(path)
        except Exception as exc:  # noqa: BLE001
            print("FAIL", path.name, exc)
            continue
        if i % 60 == 0 or i == len(files):
            print(f"  {i}/{len(files)} {path.name} {path.stat().st_size // 1024}kb")
    print("done")


if __name__ == "__main__":
    main()
