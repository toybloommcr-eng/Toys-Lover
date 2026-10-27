"""Expand lifestyle photos that still sit inside a white letterbox."""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageOps

ROOT = Path(r"e:\Toys Lover\public\images")
FOLDERS = [ROOT / "products", ROOT / "categories"]


def white_mat(rgb: np.ndarray) -> np.ndarray:
    pix = rgb.astype(np.float32)
    dist = np.linalg.norm(pix - 255.0, axis=2)
    r, g, b = pix[:, :, 0], pix[:, :, 1], pix[:, :, 2]
    lum = 0.299 * r + 0.587 * g + 0.114 * b
    sat = np.maximum(np.maximum(r, g), b) - np.minimum(np.minimum(r, g), b)
    return (dist < 14) | ((lum > 246) & (sat < 12))


def expand(path: Path) -> str:
    im = Image.open(path).convert("RGB")
    rgb = np.asarray(im)
    h, w = rgb.shape[:2]
    mat = white_mat(rgb)
    band = max(16, min(h, w) // 10)
    border = np.zeros((h, w), dtype=bool)
    border[:band] = True
    border[-band:] = True
    border[:, :band] = True
    border[:, -band:] = True
    inner = np.zeros((h, w), dtype=bool)
    inner[h // 5 : -h // 5, w // 5 : -w // 5] = True
    if mat[border].mean() < 0.72 or mat[inner].mean() > 0.38:
        return "skip"

    content = ~mat
    col = content.mean(axis=0)
    row = content.mean(axis=1)
    xs = np.where(col > 0.05)[0]
    ys = np.where(row > 0.05)[0]
    if xs.size == 0 or ys.size == 0:
        return "skip"
    left, right = int(xs[0]), int(xs[-1])
    top, bot = int(ys[0]), int(ys[-1])
    if (right - left) < w * 0.4 or (bot - top) < h * 0.4:
        return "skip"
    crop = im.crop((left, top, right + 1, bot + 1))
    filled = ImageOps.fit(crop, (w, h), method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
    filled.save(path, format="JPEG", quality=90, optimize=True, progressive=True)
    return "fill"


def main() -> None:
    files: list[Path] = []
    for folder in FOLDERS:
        files.extend(sorted(folder.glob("*.jpg")))
    filled = skipped = 0
    for path in files:
        note = expand(path)
        if note == "fill":
            filled += 1
        else:
            skipped += 1
        if note == "fill":
            print(f"{path.parent.name}/{path.name}: fill")
    print(f"done fill={filled} skip={skipped}")


if __name__ == "__main__":
    main()
