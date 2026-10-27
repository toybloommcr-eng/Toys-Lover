"""Re-export every product photo as full HD with a complete, uncropped view."""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageEnhance, ImageOps

ROOT = Path(r"e:\Toys Lover\public\images\products")
CANVAS = 1400
# Keep more of the photo so packaging stays complete (less aggressive crop).
INNER = 0.94
WHITE = (255, 255, 255)
KEEP_AROUND = 0.08


def polish(im: Image.Image) -> Image.Image:
    im = ImageOps.exif_transpose(im).convert("RGB")
    im = ImageEnhance.Contrast(im).enhance(1.06)
    im = ImageEnhance.Color(im).enhance(1.05)
    im = ImageEnhance.Sharpness(im).enhance(1.15)
    im = ImageEnhance.Brightness(im).enhance(1.02)
    return im


def studio_bg(rgb: np.ndarray) -> tuple[int, int, int]:
    border = np.concatenate(
        [
            rgb[:12, :, :].reshape(-1, 3),
            rgb[-12:, :, :].reshape(-1, 3),
            rgb[:, :12, :].reshape(-1, 3),
            rgb[:, -12:, :].reshape(-1, 3),
        ]
    )
    return tuple(int(v) for v in np.median(border, axis=0))


def content_box(rgb: np.ndarray) -> tuple[int, int, int, int]:
    h, w = rgb.shape[:2]
    bg = np.array(studio_bg(rgb), dtype=np.float32)
    dist = np.linalg.norm(rgb.astype(np.float32) - bg, axis=2)
    # Soft threshold — prefer keeping edges of packaging over tight crop.
    mask = dist > max(12.0, float(np.percentile(dist, 45)) * 0.35)
    if mask.mean() > 0.92:
        mask = dist > float(np.percentile(dist, 30))
    if mask.mean() < 0.015:
        return 0, 0, w - 1, h - 1
    ys, xs = np.where(mask)
    pad = int(KEEP_AROUND * max(w, h))
    return (
        max(0, int(xs.min()) - pad),
        max(0, int(ys.min()) - pad),
        min(w - 1, int(xs.max()) + pad),
        min(h - 1, int(ys.max()) + pad),
    )


def upgrade(path: Path) -> None:
    im = polish(Image.open(path))
    rgb = np.asarray(im)
    left, top, right, bot = content_box(rgb)
    crop = im.crop((left, top, right + 1, bot + 1))
    max_side = int(CANVAS * INNER)
    crop.thumbnail((max_side, max_side), Image.Resampling.LANCZOS)
    # If the source is already smaller, upscale gently so tiles stay sharp.
    if max(crop.size) < 900:
        scale = 900 / max(crop.size)
        crop = crop.resize(
            (max(1, int(crop.width * scale)), max(1, int(crop.height * scale))),
            Image.Resampling.LANCZOS,
        )
        crop.thumbnail((max_side, max_side), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (CANVAS, CANVAS), WHITE)
    canvas.paste(crop, ((CANVAS - crop.width) // 2, (CANVAS - crop.height) // 2))
    canvas.save(path, format="JPEG", quality=95, optimize=True, subsampling=0)


def main() -> None:
    files = sorted(ROOT.glob("*.jpg"))
    print("upgrading", len(files), "product photos to", CANVAS, "px HD full view")
    for i, path in enumerate(files, 1):
        try:
            upgrade(path)
        except Exception as exc:  # noqa: BLE001
            print("FAIL", path.name, exc)
            continue
        if i % 40 == 0 or i == len(files):
            print(f"  {i}/{len(files)} {path.name} {path.stat().st_size // 1024}kb")
    print("done")


if __name__ == "__main__":
    main()
