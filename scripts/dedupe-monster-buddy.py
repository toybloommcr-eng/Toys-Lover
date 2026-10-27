"""Conservative cleanup: unique Monster Buddy photos + drop identical-hash duplicates only."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageOps

ROOT = Path(r"e:\Toys Lover")
PRODUCTS = ROOT / "public" / "images" / "products"
ADVANCE = ROOT / "Toys Advance Category"
DATA = ROOT / "lib" / "data"
CANVAS = 1000
INNER = 0.90

STOCK_FILES = [
    "advance-stock.ts",
    "extra-stock.ts",
    "china-stock.ts",
    "innovative-stock.ts",
    "october-new-stock.ts",
    "new-stock.ts",
]


def to_white_square(im: Image.Image) -> Image.Image:
    im = ImageOps.exif_transpose(im).convert("RGB")
    im = ImageEnhance.Color(im).enhance(1.05)
    im = ImageEnhance.Contrast(im).enhance(1.04)
    fitted = im.copy()
    fitted.thumbnail((int(CANVAS * INNER), int(CANVAS * INNER)), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (CANVAS, CANVAS), (255, 255, 255))
    canvas.paste(fitted, ((CANVAS - fitted.width) // 2, (CANVAS - fitted.height) // 2))
    return canvas


def save_slug(slug: str, im: Image.Image) -> None:
    im.save(PRODUCTS / f"{slug}.jpg", "JPEG", quality=88, optimize=True, progressive=True)


def images_in(folder: Path) -> list[Path]:
    return sorted(
        [p for p in folder.iterdir() if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}],
        key=lambda p: p.name.lower(),
    )


def find_folder(needle: str) -> Path | None:
    for folder in ADVANCE.iterdir():
        if folder.is_dir() and needle.lower() in folder.name.lower():
            return folder
    return None


def looks_unprofessional(path: Path) -> bool:
    """Only flag clear Chinese sheets or heavy deep-fried dark catalog art."""
    bgr = cv2.imread(str(path))
    if bgr is None:
        return True
    h, w = bgr.shape[:2]
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    left = gray[:, : max(1, w // 3)]
    # Chinese wholesale text column
    if (left > 200).mean() > 0.45 and (left < 70).mean() > 0.06 and cv2.Canny(left, 50, 120).mean() > 14:
        return True
    # Deep-fried: mostly black bg + extreme saturation + harsh edges
    if (gray < 35).mean() > 0.45 and hsv[:, :, 1].mean() > 110 and cv2.Canny(gray, 90, 200).mean() > 30:
        return True
    # Very soft after content crop
    mask = gray < 245
    if mask.mean() > 0.02:
        ys, xs = np.where(mask)
        crop = gray[ys.min() : ys.max() + 1, xs.min() : xs.max() + 1]
        if cv2.Laplacian(crop, cv2.CV_64F).var() < 60:
            return True
    return False


def rematch() -> dict[str, Path]:
    written: dict[str, Path] = {}
    mapping = [
        ("3.1 right up Labubu Big bags", "monster-buddy-big-bag", 12),
        ("Labubu bags (L)", "monster-buddy-large-bag", 7),
        ("Labubu bags (m)", "monster-buddy-medium-bag", 2),
        ("Labubu Bags put this", "monster-buddy-bag", 2),
        ("Labubu small Bags", "monster-buddy-small-bag", 3),
        ("Labubu kirings", "monster-buddy-keyring", 5),
    ]
    for needle, prefix, limit in mapping:
        folder = find_folder(needle)
        if not folder:
            continue
        unique: list[Path] = []
        seen: set[str] = set()
        for p in images_in(folder):
            h = hashlib.md5(p.read_bytes()).hexdigest()
            if h in seen:
                continue
            seen.add(h)
            unique.append(p)
        for i, src in enumerate(unique[:limit], start=1):
            slug = f"{prefix}-{i:02d}"
            save_slug(slug, to_white_square(Image.open(src)))
            written[slug] = src
            print("wrote", slug, flush=True)
    return written


def prefer_slug(slugs: list[str]) -> str:
    def key(s: str):
        m = re.search(r"-(\d+)$", s)
        n = int(m.group(1)) if m else 999
        rank = 0 if "big-bag" in s else 1 if "large-bag" in s else 2 if "medium" in s else 3 if "small" in s else 4
        return (rank, n, s)

    return sorted(slugs, key=key)[0]


def remove_slugs(slugs: set[str]) -> int:
    removed = 0
    for name in STOCK_FILES:
        path = DATA / name
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        original = text
        for slug in sorted(slugs):
            pattern = (
                r"\n  \{\n"
                rf'    slug: "{re.escape(slug)}",\n'
                r".*?"
                r"\n  \},"
            )
            text, n = re.subn(pattern, "", text, count=1, flags=re.S)
            removed += n
            if n:
                continue
            pattern2 = (
                r"\n  \{\n"
                rf'    slug: "{re.escape(slug)}",\n'
                r".*?"
                r"\n  \}\n"
            )
            text, n = re.subn(pattern2, "\n", text, count=1, flags=re.S)
            removed += n
        if text != original:
            text = re.sub(r",\s*\]", "\n]", text)
            path.write_text(text, encoding="utf-8")
            print("updated", name, flush=True)
    return removed


def main() -> None:
    print("rematch monster buddy…", flush=True)
    rematch()

    # Collect all product slugs from stock
    all_text = "\n".join(p.read_text(encoding="utf-8") for p in (DATA / f for f in STOCK_FILES) if p.exists())
    # also core products.ts
    products_ts = (DATA / "products.ts").read_text(encoding="utf-8")
    # only strip from advance/extra/etc — products.ts core uses shop images differently
    stock_slugs = set(re.findall(r'slug:\s*"([^"]+)"', all_text))

    drop: set[str] = set()

    # 1) Identical hash duplicates across stock products
    by_hash: dict[str, list[str]] = {}
    for slug in sorted(stock_slugs):
        path = PRODUCTS / f"{slug}.jpg"
        if not path.exists():
            continue
        by_hash.setdefault(hashlib.md5(path.read_bytes()).hexdigest(), []).append(slug)
    for group in by_hash.values():
        if len(group) < 2:
            continue
        keep = prefer_slug(group)
        for s in group:
            if s != keep:
                drop.add(s)
        print("dup keep", keep, "drop", sorted(set(group) - {keep}), flush=True)

    # 2) Monster buddy / keyring quality gate only
    for slug in sorted(stock_slugs):
        if not slug.startswith("monster-buddy"):
            continue
        if slug in drop:
            continue
        path = PRODUCTS / f"{slug}.jpg"
        if not path.exists() or looks_unprofessional(path):
            drop.add(slug)
            print("quality drop", slug, flush=True)

    print("dropping", len(drop), flush=True)
    print("removed objects", remove_slugs(drop), flush=True)
    for slug in sorted(drop):
        p = PRODUCTS / f"{slug}.jpg"
        if p.exists():
            p.unlink()

    remaining_mb = sorted(
        s
        for s in stock_slugs - drop
        if s.startswith("monster-buddy") and "keyring" not in s and (PRODUCTS / f"{s}.jpg").exists()
    )
    print("monster buddy bags left", len(remaining_mb), remaining_mb, flush=True)


if __name__ == "__main__":
    main()
