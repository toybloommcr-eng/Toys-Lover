from pathlib import Path

from PIL import Image

ROOT = Path(r"e:\Toys Lover\public\images")
MAX_WIDTH = 1600
SKIP = {"logo-mark.png"}


def main() -> None:
    paths = sorted(p for p in ROOT.rglob("*") if p.is_file())
    for path in paths:
        if path.name in SKIP:
            continue
        if path.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
            continue
        image = Image.open(path)
        fmt = "JPEG" if path.suffix.lower() in {".jpg", ".jpeg"} else "PNG"
        if fmt == "JPEG":
            image = image.convert("RGB")
        width, height = image.size
        if width > MAX_WIDTH:
            height = int(height * MAX_WIDTH / width)
            image = image.resize((MAX_WIDTH, height), Image.Resampling.LANCZOS)
        before = path.stat().st_size
        if fmt == "JPEG":
            image.save(path, format="JPEG", quality=76, optimize=True, progressive=True)
        else:
            image.save(path, format="PNG", optimize=True)
        after = path.stat().st_size
        print(f"{path.relative_to(ROOT)}: {before // 1024}kb -> {after // 1024}kb ({image.size[0]}x{image.size[1]})")


if __name__ == "__main__":
    main()
