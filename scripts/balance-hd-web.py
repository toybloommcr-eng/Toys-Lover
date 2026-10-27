"""Keep polished HD detail while trimming overweight JPEGs for web."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(r"e:\Toys Lover")
DIRS = [
    ROOT / "public" / "images" / "products",
    ROOT / "public" / "images" / "categories",
]

MAX_SIDE = 1400
# Prefer clarity: only shrink files that are still heavy
HEAVY_KB = 420
QUALITY = 88


def balance(path: Path) -> tuple[int, int]:
    before = path.stat().st_size
    if before <= HEAVY_KB * 1024:
        return before, before
    im = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    if max(im.size) > MAX_SIDE:
        im.thumbnail((MAX_SIDE, MAX_SIDE), Image.Resampling.LANCZOS)
    tmp = path.with_suffix(".tmp.jpg")
    im.save(
        tmp,
        format="JPEG",
        quality=QUALITY,
        optimize=True,
        progressive=True,
        subsampling=1,
    )
    tmp.replace(path)
    return before, path.stat().st_size


def main() -> None:
    files: list[Path] = []
    for folder in DIRS:
        files.extend(sorted(folder.glob("*.jpg")))
    trimmed = 0
    saved = 0
    for i, path in enumerate(files, 1):
        before, after = balance(path)
        if after < before:
            trimmed += 1
            saved += before - after
        if i % 80 == 0 or i == len(files):
            print(f"  {i}/{len(files)} trimmed {trimmed}", flush=True)
    print(
        f"done — trimmed {trimmed} heavy files, saved {saved // (1024 * 1024)} MB",
        flush=True,
    )


if __name__ == "__main__":
    main()
