"""Upscale soft/low-bitrate catalog photos and rebuild core category heroes to HD."""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

ROOT = Path(r"e:\Toys Lover")
PRODUCT_DIR = ROOT / "public" / "images" / "products"
CATEGORY_DIR = ROOT / "public" / "images" / "categories"
CANVAS = 1400
INNER = 0.92
WHITE = (255, 255, 255)

LOW_BITRATE = [
    "cloud-ghost-squishy",
    "basketball-play-set",
    "fairy-light-bubble-wand",
    "pretend-vacuum-cleaner",
    "lucky-cat-squishy",
    "cat-face-musical-guitar",
    "butter-block-squishy",
    "speed-phantom-rc",
    "banana-trio-squishy",
    "jumbo-pencil-squishy",
    "unzip-penguin-squishy",
    "super-arrow-set",
    "crunch-carrot-squishy",
    "unicorn-snuggle-plush",
    "cheddar-block-squishy",
    "giant-duck-squishy",
    "mango-cloud-squishy",
    "electric-water-blaster",
]

CATEGORY_HEROES = {
    "action-figures": "hero-league-figure",
    "educational-stem": "space-explorer-kit",
    "baby-toddler": "piano-fitness-gym",
    "board-games": "soccer-star-table-game",
    "building-sets": "dino-expedition-build",
    "dolls-plush": "snuggle-puppy-plush",
    "games-gadgets": "quick-push-console",
    "outdoor-sports": "ride-on-4x4-jeep",
    "role-play": "dream-castle-playset",
}


def polish(im: Image.Image) -> Image.Image:
    im = ImageOps.exif_transpose(im).convert("RGB")
    im = ImageEnhance.Contrast(im).enhance(1.1)
    im = ImageEnhance.Color(im).enhance(1.08)
    im = ImageEnhance.Sharpness(im).enhance(1.35)
    return im


def content_box(im: Image.Image) -> tuple[int, int, int, int]:
    rgb = np.asarray(im)
    h, w = rgb.shape[:2]
    border = np.concatenate(
        [
            rgb[:8, :, :].reshape(-1, 3),
            rgb[-8:, :, :].reshape(-1, 3),
            rgb[:, :8, :].reshape(-1, 3),
            rgb[:, -8:, :].reshape(-1, 3),
        ]
    )
    bg = border.astype(np.float32).mean(axis=0)
    dist = np.linalg.norm(rgb.astype(np.float32) - bg, axis=2)
    mask = dist > max(14.0, float(np.percentile(dist, 45)) * 0.35)
    if mask.mean() < 0.02:
        return 0, 0, w - 1, h - 1
    ys, xs = np.where(mask)
    pad = int(0.04 * max(w, h))
    return max(0, int(xs.min()) - pad), max(0, int(ys.min()) - pad), min(w - 1, int(xs.max()) + pad), min(h - 1, int(ys.max()) + pad)


def frame_hd(src: Path, dest: Path) -> None:
    im = polish(Image.open(src))
    left, top, right, bot = content_box(im)
    crop = im.crop((left, top, right + 1, bot + 1))
    # Upscale soft sources with Lanczos before fit
    if max(crop.size) < CANVAS * INNER:
        scale = (CANVAS * INNER) / max(crop.size)
        crop = crop.resize((max(1, int(crop.width * scale)), max(1, int(crop.height * scale))), Image.Resampling.LANCZOS)
        crop = crop.filter(ImageFilter.UnsharpMask(radius=1.2, percent=120, threshold=2))
    max_side = int(CANVAS * INNER)
    crop.thumbnail((max_side, max_side), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (CANVAS, CANVAS), WHITE)
    canvas.paste(crop, ((CANVAS - crop.width) // 2, (CANVAS - crop.height) // 2))
    dest.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(dest, format="JPEG", quality=94, optimize=True, subsampling=0)


def main() -> None:
    for slug in LOW_BITRATE:
        src = PRODUCT_DIR / f"{slug}.jpg"
        if not src.exists():
            print("missing", slug)
            continue
        before = src.stat().st_size
        frame_hd(src, src)
        after = src.stat().st_size
        im = Image.open(src)
        print(f"product {slug}: {before // 1024}kb -> {after // 1024}kb {im.size}")

    for cat, slug in CATEGORY_HEROES.items():
        src = PRODUCT_DIR / f"{slug}.jpg"
        dest = CATEGORY_DIR / f"{cat}.jpg"
        if not src.exists():
            print("missing hero", slug)
            continue
        frame_hd(src, dest)
        im = Image.open(dest)
        print(f"category {cat}: {dest.stat().st_size // 1024}kb {im.size}")


if __name__ == "__main__":
    main()
