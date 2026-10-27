"""Fill every product photo so the toy covers nearly the whole HD square (no tiny letterbox)."""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageEnhance, ImageOps

ROOT = Path(r"e:\Toys Lover\public\images\products")
CANVAS = 1600
FILL = 0.99  # product covers 99% of the square


def polish(im: Image.Image) -> Image.Image:
    im = ImageOps.exif_transpose(im).convert("RGB")
    im = ImageEnhance.Contrast(im).enhance(1.1)
    im = ImageEnhance.Color(im).enhance(1.08)
    im = ImageEnhance.Sharpness(im).enhance(1.3)
    im = ImageEnhance.Brightness(im).enhance(1.02)
    return im


def content_box(rgb: np.ndarray) -> tuple[int, int, int, int]:
    h, w = rgb.shape[:2]
    white = np.array([255.0, 255.0, 255.0])
    cream = np.array([255.0, 244.0, 232.0])
    dist = np.minimum(
        np.linalg.norm(rgb.astype(np.float32) - white, axis=2),
        np.linalg.norm(rgb.astype(np.float32) - cream, axis=2),
    )
    mask = dist > 16.0
    if mask.mean() > 0.9:
        return 0, 0, w - 1, h - 1
    if mask.mean() < 0.012:
        mask = dist > 9.0
    if mask.mean() < 0.005:
        return 0, 0, w - 1, h - 1
    ys, xs = np.where(mask)
    pad = max(2, int(0.015 * max(w, h)))
    return (
        max(0, int(xs.min()) - pad),
        max(0, int(ys.min()) - pad),
        min(w - 1, int(xs.max()) + pad),
        min(h - 1, int(ys.max()) + pad),
    )


def cover_square(crop: Image.Image, side: int) -> Image.Image:
    """Scale so the short side fills `side`, then center-crop — product fills the frame."""
    w, h = crop.size
    if w < 1 or h < 1:
        return Image.new("RGB", (side, side), (255, 255, 255))
    scale = side / min(w, h)
    new_w = max(side, int(round(w * scale)))
    new_h = max(side, int(round(h * scale)))
    resized = crop.resize((new_w, new_h), Image.Resampling.LANCZOS)
    left = (new_w - side) // 2
    top = (new_h - side) // 2
    return resized.crop((left, top, left + side, top + side))


def maximize(path: Path) -> float:
    im = polish(Image.open(path))
    rgb = np.asarray(im)
    left, top, right, bot = content_box(rgb)
    crop = im.crop((left, top, right + 1, bot + 1))
    side = max(400, int(CANVAS * FILL))
    filled = cover_square(crop, side)
    canvas = Image.new("RGB", (CANVAS, CANVAS), (255, 255, 255))
    canvas.paste(filled, ((CANVAS - side) // 2, (CANVAS - side) // 2))
    canvas.save(path, format="JPEG", quality=96, optimize=True, subsampling=0)
    out = np.asarray(canvas)
    dist = np.linalg.norm(out.astype(np.float32) - 255.0, axis=2)
    return float((dist > 12).mean() * 100)


def main() -> None:
    files = sorted(ROOT.glob("*.jpg"))
    print("cover-fill maximizing", len(files), "shots @", CANVAS, "px")
    fills: list[float] = []
    for i, path in enumerate(files, 1):
        try:
            fill = maximize(path)
            fills.append(fill)
        except Exception as exc:  # noqa: BLE001
            print("FAIL", path.name, exc)
            continue
        if i % 50 == 0 or i == len(files):
            print(
                f"  {i}/{len(files)} avg {sum(fills)/len(fills):.1f}%  "
                f"min {min(fills):.1f}%  last {path.name} {fill:.1f}%"
            )
    print("done mean", round(sum(fills) / len(fills), 1), "%  min", round(min(fills), 1), "%")


if __name__ == "__main__":
    main()
