"""Compress catalog JPGs for fast web delivery while keeping HD clarity."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(r"e:\Toys Lover")
DIRS = [
    ROOT / "public" / "images" / "products",
    ROOT / "public" / "images" / "categories",
]

# Keep square HD frames; aggressive but clean JPEG for storefront thumbs
MAX_SIDE = 1200
QUALITY = 78
TARGET_KB = 180  # soft target — drop quality further if still huge


def compress(path: Path) -> tuple[int, int]:
    before = path.stat().st_size
    im = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    w, h = im.size
    if max(w, h) > MAX_SIDE:
        im.thumbnail((MAX_SIDE, MAX_SIDE), Image.Resampling.LANCZOS)

    quality = QUALITY
    tmp = path.with_suffix(".tmp.jpg")
    for q in range(quality, 58, -4):
        im.save(
            tmp,
            format="JPEG",
            quality=q,
            optimize=True,
            progressive=True,
            subsampling=2,
        )
        if tmp.stat().st_size <= TARGET_KB * 1024 or q <= 62:
            quality = q
            break

    tmp.replace(path)
    after = path.stat().st_size
    return before, after


def main() -> None:
    files: list[Path] = []
    for folder in DIRS:
        files.extend(sorted(folder.glob("*.jpg")))
    print(f"compressing {len(files)} images (max {MAX_SIDE}px, q~{QUALITY})")
    saved = 0
    total_before = 0
    total_after = 0
    for i, path in enumerate(files, 1):
        before, after = compress(path)
        total_before += before
        total_after += after
        saved += before - after
        if i % 60 == 0 or i == len(files):
            print(
                f"  {i}/{len(files)} {path.name} "
                f"{before // 1024}->{after // 1024}kb",
                flush=True,
            )
    print(
        f"done - saved {saved // (1024 * 1024)} MB "
        f"({total_before // (1024 * 1024)} -> {total_after // (1024 * 1024)} MB)",
        flush=True,
    )


if __name__ == "__main__":
    main()
