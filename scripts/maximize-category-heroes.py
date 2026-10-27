"""Rebuild every category hero from its best product photo, cover-filled HD."""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
from PIL import Image, ImageEnhance, ImageOps

ROOT = Path(r"e:\Toys Lover")
PRODUCT_DIR = ROOT / "public" / "images" / "products"
CATEGORY_DIR = ROOT / "public" / "images" / "categories"
PRODUCTS_TS = ROOT / "lib" / "data" / "products.ts"
STOCK_FILES = [
    ROOT / "lib" / "data" / "new-stock.ts",
    ROOT / "lib" / "data" / "advance-stock.ts",
    ROOT / "lib" / "data" / "extra-stock.ts",
    ROOT / "lib" / "data" / "china-stock.ts",
    ROOT / "lib" / "data" / "innovative-stock.ts",
    ROOT / "lib" / "data" / "october-new-stock.ts",
    PRODUCTS_TS,
]

CANVAS = 1600
FILL = 0.99


def polish(im: Image.Image) -> Image.Image:
    im = ImageOps.exif_transpose(im).convert("RGB")
    im = ImageEnhance.Contrast(im).enhance(1.1)
    im = ImageEnhance.Color(im).enhance(1.08)
    im = ImageEnhance.Sharpness(im).enhance(1.3)
    return im


def content_box(rgb: np.ndarray) -> tuple[int, int, int, int]:
    h, w = rgb.shape[:2]
    white = np.array([255.0, 255.0, 255.0])
    cream = np.array([255.0, 244.0, 232.0])
    black = np.array([0.0, 0.0, 0.0])
    dist_w = np.linalg.norm(rgb.astype(np.float32) - white, axis=2)
    dist_c = np.linalg.norm(rgb.astype(np.float32) - cream, axis=2)
    dist_b = np.linalg.norm(rgb.astype(np.float32) - black, axis=2)
    # Prefer non-white content; for black-bg collages keep full frame.
    black_bg = (dist_b < 28).mean() > 0.55
    if black_bg:
        return 0, 0, w - 1, h - 1
    dist = np.minimum(dist_w, dist_c)
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


def maximize_file(src: Path, dest: Path) -> None:
    im = polish(Image.open(src))
    rgb = np.asarray(im)
    left, top, right, bot = content_box(rgb)
    crop = im.crop((left, top, right + 1, bot + 1))
    side = max(400, int(CANVAS * FILL))
    filled = cover_square(crop, side)
    canvas = Image.new("RGB", (CANVAS, CANVAS), (255, 255, 255))
    canvas.paste(filled, ((CANVAS - side) // 2, (CANVAS - side) // 2))
    dest.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(dest, format="JPEG", quality=96, optimize=True, subsampling=0)


def parse_category_products() -> dict[str, list[str]]:
    """Map categorySlug -> product slugs from stock TS files."""
    mapping: dict[str, list[str]] = {}
    slug_re = re.compile(r'slug:\s*"([^"]+)"')
    cat_re = re.compile(r'categorySlug:\s*"([^"]+)"')
    for path in STOCK_FILES:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        # Split roughly on product objects
        chunks = re.split(r"\n\s*\{\s*\n", text)
        for chunk in chunks:
            slugs = slug_re.findall(chunk)
            cats = cat_re.findall(chunk)
            if not slugs or not cats:
                continue
            slug, cat = slugs[0], cats[0]
            mapping.setdefault(cat, []).append(slug)
    return mapping


def pick_source(cat: str, slugs: list[str]) -> Path | None:
    for slug in slugs:
        candidate = PRODUCT_DIR / f"{slug}.jpg"
        if candidate.exists():
            return candidate
    # fallback existing category file
    existing = CATEGORY_DIR / f"{cat}.jpg"
    return existing if existing.exists() else None


def main() -> None:
    mapping = parse_category_products()
    # Also process any category jpg even if no products parsed
    cats = {p.stem for p in CATEGORY_DIR.glob("*.jpg")} | set(mapping)
    print("categories", len(cats), "mapped", len(mapping))
    done = 0
    for cat in sorted(cats):
        src = pick_source(cat, mapping.get(cat, []))
        if not src:
            print("skip", cat)
            continue
        dest = CATEGORY_DIR / f"{cat}.jpg"
        maximize_file(src, dest)
        done += 1
        print(f"  {cat} <- {src.name} ({dest.stat().st_size // 1024}kb)")
    # Also re-maximize every product once more for consistency
    products = sorted(PRODUCT_DIR.glob("*.jpg"))
    print("re-maximizing products", len(products))
    for i, path in enumerate(products, 1):
        maximize_file(path, path)
        if i % 80 == 0 or i == len(products):
            print(f"  products {i}/{len(products)}")
    print("done categories", done, "products", len(products))


if __name__ == "__main__":
    main()
