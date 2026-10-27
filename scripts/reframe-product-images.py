#!/usr/bin/env python3
"""Crop excess white margins and frame product photos to ~85% fill on a white square."""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parents[1]
PRODUCTS = ROOT / "public" / "images" / "products"
TARGET = 1200
MIN_FILL = 0.58  # subject ratio before reframing
TARGET_FILL = 0.86


def subject_bbox(im: Image.Image, threshold: int = 248) -> tuple[int, int, int, int] | None:
    rgb = im.convert("RGB")
    w, h = rgb.size
    px = rgb.load()
    min_x, min_y, max_x, max_y = w, h, 0, 0
    found = False
    step = max(1, min(w, h) // 400)
    for y in range(0, h, step):
        for x in range(0, w, step):
            r, g, b = px[x, y]
            if r < threshold or g < threshold or b < threshold:
                found = True
                if x < min_x:
                    min_x = x
                if y < min_y:
                    min_y = y
                if x > max_x:
                    max_x = x
                if y > max_y:
                    max_y = y
    if not found:
        return None
    pad = int(max(w, h) * 0.02)
    return (
        max(0, min_x - pad),
        max(0, min_y - pad),
        min(w, max_x + pad + step),
        min(h, max_y + pad + step),
    )


def fill_ratio(im: Image.Image) -> float:
    small = im.convert("RGB").resize((160, 160))
    pix = list(small.getdata())
    nw = sum(1 for r, g, b in pix if r < 248 or g < 248 or b < 248)
    return nw / len(pix)


def reframe(im: Image.Image) -> Image.Image:
    rgb = ImageOps.exif_transpose(im).convert("RGB")
    bbox = subject_bbox(rgb)
    if bbox:
        rgb = rgb.crop(bbox)

    # Fit subject into TARGET square with margin so fill ~= TARGET_FILL
    w, h = rgb.size
    side = max(w, h)
    # enlarge subject relative to canvas
    subject_side = int(TARGET * TARGET_FILL)
    scale = subject_side / side
    new_w = max(1, int(w * scale))
    new_h = max(1, int(h * scale))
    resized = rgb.resize((new_w, new_h), Image.Resampling.LANCZOS)
    # light sharpen for clarity
    resized = resized.filter(ImageFilter.UnsharpMask(radius=1.2, percent=110, threshold=2))

    canvas = Image.new("RGB", (TARGET, TARGET), (255, 255, 255))
    canvas.paste(resized, ((TARGET - new_w) // 2, (TARGET - new_h) // 2))
    return canvas


def process_file(path: Path, force: bool = False) -> str:
    try:
        im = Image.open(path)
    except Exception as exc:  # noqa: BLE001
        return f"skip open {path.name}: {exc}"
    before = fill_ratio(im)
    if not force and before >= MIN_FILL and max(im.size) >= 900:
        return f"ok  fill={before:.2f} {path.name}"

    framed = reframe(im)
    after = fill_ratio(framed)
    # Prefer JPEG for storefront consistency; keep webp extension content as jpeg bytes only if jpg
    out = path
    if path.suffix.lower() == ".webp":
        # save as high-quality webp if pillow supports, else jpg sibling and leave path
        try:
            framed.save(out, "WEBP", quality=88, method=6)
        except Exception:
            out = path.with_suffix(".jpg")
            framed.save(out, "JPEG", quality=88, optimize=True, progressive=True)
    else:
        framed.save(out, "JPEG", quality=88, optimize=True, progressive=True)
    return f"fix fill {before:.2f}->{after:.2f} {path.name}"


def collect_targets(only_subdir: str | None) -> list[Path]:
    roots = [PRODUCTS]
    if only_subdir:
        roots = [PRODUCTS / only_subdir]
    files: list[Path] = []
    for root in roots:
        if not root.exists():
            continue
        files.extend(root.rglob("*.jpg"))
        files.extend(root.rglob("*.jpeg"))
        files.extend(root.rglob("*.webp"))
        files.extend(root.rglob("*.png"))
    return sorted(files)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--subdir", default=None, help="e.g. telegram")
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()

    files = collect_targets(args.subdir)
    if args.limit:
        files = files[: args.limit]

    fixed = 0
    for i, path in enumerate(files, 1):
        msg = process_file(path, force=args.force)
        if msg.startswith("fix"):
            fixed += 1
        if i % 50 == 0 or msg.startswith("fix") or msg.startswith("skip"):
            print(f"[{i}/{len(files)}] {msg}")
    print(f"done files={len(files)} fixed={fixed}")


if __name__ == "__main__":
    main()
