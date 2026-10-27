"""Wash leftover peach/cream and give studio cutouts clean white padding. Never crop again."""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(r"e:\Toys Lover\public\images")
FOLDERS = [ROOT / "products", ROOT / "categories"]
WHITE = np.array([255, 255, 255], dtype=np.float32)
CREAM = np.array([255, 244, 232], dtype=np.float32)
PEACH = np.array([255, 226, 200], dtype=np.float32)
WARM = np.array([255, 236, 216], dtype=np.float32)


def paper_mask(rgb: np.ndarray) -> np.ndarray:
    pix = rgb.astype(np.float32)
    r, g, b = pix[:, :, 0], pix[:, :, 1], pix[:, :, 2]
    lum = 0.299 * r + 0.587 * g + 0.114 * b
    mx = np.maximum(np.maximum(r, g), b)
    mn = np.minimum(np.minimum(r, g), b)
    sat = mx - mn
    dist = np.minimum.reduce(
        [
            np.linalg.norm(pix - WHITE, axis=2),
            np.linalg.norm(pix - CREAM, axis=2),
            np.linalg.norm(pix - PEACH, axis=2),
            np.linalg.norm(pix - WARM, axis=2),
        ]
    )
    warm = (r >= g - 6) & (g >= b - 14) & (r > 176)
    return (
        (dist < 32)
        | ((lum > 208) & (sat < 46))
        | ((lum > 192) & warm & (sat < 68))
        | ((lum > 176) & warm & (sat < 40) & (b > 145))
    )


def content_box(mask: np.ndarray, pad_ratio: float = 0.03) -> tuple[int, int, int, int] | None:
    if mask.mean() < 0.008:
        return None
    ys, xs = np.where(mask)
    h, w = mask.shape
    pad = int(pad_ratio * max(h, w))
    return (
        max(0, int(xs.min()) - pad),
        max(0, int(ys.min()) - pad),
        min(w - 1, int(xs.max()) + pad),
        min(h - 1, int(ys.max()) + pad),
    )


def is_lifestyle(rgb: np.ndarray) -> bool:
    h, w = rgb.shape[:2]
    band = max(12, min(h, w) // 16)
    corners = np.concatenate(
        [
            rgb[:band, :band].reshape(-1, 3),
            rgb[:band, -band:].reshape(-1, 3),
            rgb[-band:, :band].reshape(-1, 3),
            rgb[-band:, -band:].reshape(-1, 3),
        ]
    )
    lum = corners.astype(np.float32).mean(axis=1)
    var = float(np.mean(np.var(corners.astype(np.float32), axis=0)))
    return float(np.median(lum)) < 150 or var > 1800


def place_on_white(crop: Image.Image, size: int) -> Image.Image:
    max_side = int(size * 0.84)
    fitted = crop.copy()
    fitted.thumbnail((max_side, max_side), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (size, size), (255, 255, 255))
    canvas.paste(fitted, ((size - fitted.width) // 2, (size - fitted.height) // 2))
    return canvas


def recover(path: Path) -> str:
    im = Image.open(path).convert("RGB")
    rgb = np.asarray(im).copy()
    size = max(im.size)
    paper = paper_mask(rgb)
    rgb[paper] = 255

    if is_lifestyle(np.asarray(im)):
        Image.fromarray(rgb).save(path, format="JPEG", quality=90, optimize=True, progressive=True)
        return "keep"

    product = ~paper_mask(rgb)
    box = content_box(product, 0.02)
    if not box:
        Image.fromarray(rgb).save(path, format="JPEG", quality=90, optimize=True, progressive=True)
        return "wash"

    left, top, right, bot = box
    h, w = product.shape
    flush = left < 10 or top < 10 or right > w - 11 or bot > h - 11
    crop = Image.fromarray(rgb).crop((left, top, right + 1, bot + 1))
    if flush or (right - left) > w * 0.92 or (bot - top) > h * 0.92:
        place_on_white(crop, size).save(path, format="JPEG", quality=90, optimize=True, progressive=True)
        return "pad"
    Image.fromarray(rgb).save(path, format="JPEG", quality=90, optimize=True, progressive=True)
    return "wash"


def main() -> None:
    files: list[Path] = []
    for folder in FOLDERS:
        files.extend(sorted(folder.glob("*.jpg")))
    counts: dict[str, int] = {}
    for path in files:
        note = recover(path)
        counts[note] = counts.get(note, 0) + 1
        print(f"{path.parent.name}/{path.name}: {note}")
    print("done", len(files), counts)


if __name__ == "__main__":
    main()
