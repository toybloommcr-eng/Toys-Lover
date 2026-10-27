"""Force every catalog photo onto a clean pure-white square studio background."""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

ROOT = Path(r"e:\Toys Lover")
DIRS = [
    ROOT / "public" / "images" / "products",
    ROOT / "public" / "images" / "categories",
]
CANVAS = 1000
INNER = 0.88


def content_mask(rgb: np.ndarray) -> np.ndarray:
    pix = rgb.astype(np.float32)
    white = np.array([255.0, 255.0, 255.0])
    cream = np.array([255.0, 244.0, 232.0])
    black = np.array([0.0, 0.0, 0.0])
    dist_w = np.linalg.norm(pix - white, axis=2)
    dist_c = np.linalg.norm(pix - cream, axis=2)
    dist_b = np.linalg.norm(pix - black, axis=2)
    lum = pix.mean(axis=2)

    # Dark studio: keep non-black pixels
    if (dist_b < 28).mean() > 0.4:
        return dist_b > 32

    # Light / cream paper: keep non-paper pixels
    paper = np.minimum(dist_w, dist_c) < 18
    # also wash near-white low-sat pixels
    mx = pix.max(axis=2)
    mn = pix.min(axis=2)
    sat = mx - mn
    paper |= (lum > 235) & (sat < 18)
    return ~paper


def process(path: Path) -> None:
    im = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    rgb = np.asarray(im)
    mask = content_mask(rgb)
    if mask.mean() < 0.008:
        # Almost empty — just save white-padded original
        fitted = im.copy()
        fitted.thumbnail((int(CANVAS * INNER), int(CANVAS * INNER)), Image.Resampling.LANCZOS)
    else:
        ys, xs = np.where(mask)
        pad = int(0.03 * max(im.size))
        box = (
            max(0, int(xs.min()) - pad),
            max(0, int(ys.min()) - pad),
            min(im.width, int(xs.max()) + pad + 1),
            min(im.height, int(ys.max()) + pad + 1),
        )
        crop = im.crop(box)
        # Soft edge wash: any near-white/black fringe in crop toward white canvas later
        arr = np.asarray(crop).astype(np.float32)
        fringe = content_mask(arr.astype(np.uint8)) == False  # noqa: E712
        # don't wipe product interiors aggressively — only very light fringe
        lum = arr.mean(axis=2)
        soft = fringe & (lum > 220)
        arr[soft] = 255
        crop = Image.fromarray(arr.astype(np.uint8))
        crop = ImageEnhance.Color(crop).enhance(1.06)
        crop = ImageEnhance.Contrast(crop).enhance(1.04)
        crop = ImageEnhance.Sharpness(crop).enhance(1.12)
        crop = crop.filter(ImageFilter.UnsharpMask(radius=0.9, percent=100, threshold=2))
        fitted = crop.copy()
        fitted.thumbnail((int(CANVAS * INNER), int(CANVAS * INNER)), Image.Resampling.LANCZOS)

    canvas = Image.new("RGB", (CANVAS, CANVAS), (255, 255, 255))
    canvas.paste(fitted, ((CANVAS - fitted.width) // 2, (CANVAS - fitted.height) // 2))
    canvas.save(path, format="JPEG", quality=90, optimize=True, progressive=True, subsampling=1)


def main() -> None:
    files: list[Path] = []
    for d in DIRS:
        files.extend(sorted(d.glob("*.jpg")))
    print(f"whitening {len(files)} images to pure white {CANVAS}px")
    for i, path in enumerate(files, 1):
        try:
            process(path)
        except Exception as exc:  # noqa: BLE001
            print("FAIL", path.name, exc)
        if i % 60 == 0 or i == len(files):
            print(f"  {i}/{len(files)} {path.name}", flush=True)
    print("done", flush=True)


if __name__ == "__main__":
    main()
