"""Give every product photo a matching studio background and a safe inner margin."""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(r"e:\Toys Lover\public\images\products")
CANVAS = 1024
INNER = 0.78
WHITE = (255, 255, 255)
CREAM = np.array([255, 244, 232], dtype=np.float32)
KEEP_AROUND = 0.04


def strip_cream_mat(im: Image.Image) -> Image.Image:
    rgb = np.asarray(im).astype(np.float32)
    dist = np.linalg.norm(rgb - CREAM, axis=2)
    mask = dist > 10
    if mask.mean() < 0.05:
        return im
    ys, xs = np.where(mask)
    box = (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)
    # Only strip if the mat is a clear outer border.
    w, h = im.size
    if box[0] > w * 0.04 and box[1] > h * 0.04:
        return im.crop(box)
    return im


def studio_bg(rgb: np.ndarray) -> tuple[int, int, int]:
    border = np.concatenate(
        [
            rgb[:10, :, :].reshape(-1, 3),
            rgb[-10:, :, :].reshape(-1, 3),
            rgb[:, :10, :].reshape(-1, 3),
            rgb[:, -10:, :].reshape(-1, 3),
        ]
    )
    bg = np.median(border, axis=0)
    return tuple(int(v) for v in bg)


def content_box(rgb: np.ndarray) -> tuple[int, int, int, int]:
    h, w = rgb.shape[:2]
    bg = np.array(studio_bg(rgb), dtype=np.float32)
    dist = np.linalg.norm(rgb.astype(np.float32) - bg, axis=2)
    mask = dist > max(14.0, float(np.percentile(dist, 50)) * 0.4)
    if mask.mean() > 0.9:
        mask = dist > float(np.percentile(dist, 38))
    if mask.mean() < 0.02:
        return 0, 0, w - 1, h - 1
    ys, xs = np.where(mask)
    left, right = int(xs.min()), int(xs.max())
    top, bot = int(ys.min()), int(ys.max())
    pad = int(KEEP_AROUND * max(w, h))
    return (
        max(0, left - pad),
        max(0, top - pad),
        min(w - 1, right + pad),
        min(h - 1, bot + pad),
    )


def reframe(path: Path) -> None:
    im = strip_cream_mat(Image.open(path).convert("RGB"))
    rgb = np.asarray(im)
    left, top, right, bot = content_box(rgb)
    crop = im.crop((left, top, right + 1, bot + 1))
    bg = studio_bg(np.asarray(crop))
    max_side = int(CANVAS * INNER)
    crop.thumbnail((max_side, max_side), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (CANVAS, CANVAS), WHITE)
    x = (CANVAS - crop.width) // 2
    y = (CANVAS - crop.height) // 2
    canvas.paste(crop, (x, y))
    canvas.save(path, format="JPEG", quality=90, optimize=True, subsampling=1)


def main() -> None:
    for path in sorted(ROOT.glob("*.jpg")):
        reframe(path)
        print("reframed", path.name)


if __name__ == "__main__":
    main()
