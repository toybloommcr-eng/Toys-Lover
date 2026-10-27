"""Polish catalog photos into sharp, attractive HD storefront JPEGs.

Uses the restored masters (already checked out). Soft sources get a careful
Lanczos upscale + unsharp pass; everything saves at high JPEG quality.
"""

from __future__ import annotations

import io
from pathlib import Path

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

ROOT = Path(r"e:\Toys Lover")
DIRS = [
    ROOT / "public" / "images" / "products",
    ROOT / "public" / "images" / "categories",
]

HD = 1400
INNER = 0.90
SOFT_THRESHOLD = 14.0


def laplacian_var(im: Image.Image) -> float:
    gray = np.asarray(im.convert("L"), dtype=np.float32)
    lap = np.abs(
        gray[1:-1, 1:-1] * 4
        - gray[:-2, 1:-1]
        - gray[2:, 1:-1]
        - gray[1:-1, :-2]
        - gray[1:-1, 2:]
    )
    return float(lap.mean())


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


def enhance(im: Image.Image, soft: bool) -> Image.Image:
    im = ImageOps.exif_transpose(im).convert("RGB")
    if soft:
        im = ImageEnhance.Color(im).enhance(1.14)
        im = ImageEnhance.Contrast(im).enhance(1.12)
        im = ImageEnhance.Brightness(im).enhance(1.03)
        im = ImageEnhance.Sharpness(im).enhance(1.55)
        im = im.filter(ImageFilter.UnsharpMask(radius=1.4, percent=145, threshold=2))
    else:
        im = ImageEnhance.Color(im).enhance(1.08)
        im = ImageEnhance.Contrast(im).enhance(1.06)
        im = ImageEnhance.Sharpness(im).enhance(1.22)
        im = im.filter(ImageFilter.UnsharpMask(radius=1.0, percent=110, threshold=2))
    return im


def polish_one(path: Path) -> tuple[str, int, int, float, float]:
    before = path.stat().st_size
    raw = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    soft_score = laplacian_var(raw)
    soft = soft_score < SOFT_THRESHOLD

    im = enhance(raw, soft=soft)
    rgb = np.asarray(im)
    left, top, right, bot = content_box(rgb)
    crop = im.crop((left, top, right + 1, bot + 1))

    target = int(HD * INNER)
    # Soft photos: upscale first so detail recovers before framing
    if soft and max(crop.size) < target:
        scale = target / max(crop.size)
        # Cap upscale so we do not invent too much noise
        scale = min(scale, 2.0)
        crop = crop.resize(
            (max(1, int(crop.width * scale)), max(1, int(crop.height * scale))),
            Image.Resampling.LANCZOS,
        )
        crop = crop.filter(ImageFilter.UnsharpMask(radius=1.2, percent=130, threshold=2))

    crop.thumbnail((target, target), Image.Resampling.LANCZOS)
    bg = studio_bg(np.asarray(crop))
    canvas = Image.new("RGB", (HD, HD), bg)
    canvas.paste(crop, ((HD - crop.width) // 2, (HD - crop.height) // 2))

    quality = 93 if soft else 90
    buf = io.BytesIO()
    canvas.save(
        buf,
        format="JPEG",
        quality=quality,
        optimize=True,
        progressive=True,
        subsampling=0 if soft else 1,
    )
    path.write_bytes(buf.getvalue())
    after = path.stat().st_size
    return path.name, before, after, soft_score, laplacian_var(canvas)


def main() -> None:
    files: list[Path] = []
    for folder in DIRS:
        files.extend(sorted(folder.glob("*.jpg")))
    print(f"polishing {len(files)} images to {HD}px HD")
    soft_n = 0
    for i, path in enumerate(files, 1):
        name, before, after, before_s, after_s = polish_one(path)
        if before_s < SOFT_THRESHOLD:
            soft_n += 1
        if i % 50 == 0 or i == len(files) or before_s < SOFT_THRESHOLD and i <= 20:
            tag = "SOFT" if before_s < SOFT_THRESHOLD else "ok"
            print(
                f"  {i}/{len(files)} [{tag}] {name} "
                f"{before // 1024}->{after // 1024}kb "
                f"sharp {before_s:.1f}->{after_s:.1f}",
                flush=True,
            )
    print(f"done — enhanced {soft_n} soft photos", flush=True)


if __name__ == "__main__":
    main()
