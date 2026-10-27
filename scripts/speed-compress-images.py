"""Shrink photos that appear on first paint so Next Image has less work."""
from pathlib import Path

from PIL import Image

ROOT = Path(r"e:\Toys Lover\public\images")
WHITE = (255, 255, 255)


def jpeg_save(image: Image.Image, path: Path, quality: int) -> None:
    image.convert("RGB").save(path, format="JPEG", quality=quality, optimize=True, progressive=True)


def shrink(path: Path, max_side: int, quality: int) -> None:
    if not path.exists():
        print("missing", path)
        return
    image = Image.open(path)
    image = image.convert("RGB")
    image.thumbnail((max_side, max_side), Image.Resampling.LANCZOS)
    before = path.stat().st_size
    jpeg_save(image, path, quality)
    after = path.stat().st_size
    print(f"{path.relative_to(ROOT)}: {before // 1024}kb -> {after // 1024}kb {image.size}")


def main() -> None:
    logo = ROOT / "logo-mark.png"
    if logo.exists():
        mark = Image.open(logo).convert("RGBA")
        mark.thumbnail((96, 96), Image.Resampling.LANCZOS)
        before = logo.stat().st_size
        mark.save(logo, format="PNG", optimize=True)
        print(f"logo-mark.png: {before // 1024}kb -> {logo.stat().st_size // 1024}kb {mark.size}")

    for name in [
        "hero-play.jpg",
        "hero-kids-2.jpg",
        "hero-kids-3.jpg",
        "hero-toys.jpg",
        "page-shop.jpg",
        "page-sale.jpg",
        "page-discover.jpg",
        "page-contact.jpg",
        "page-blog.jpg",
        "page-about.jpg",
        "banner-garden-play.jpg",
        "banner-squishy-lane.jpg",
        "age-13-plus.jpg",
        "cat-stem.jpg",
        "cat-figures.jpg",
        "cat-plush.jpg",
        "cat-blocks.jpg",
        "cat-games.jpg",
        "cat-arts.jpg",
        "cat-outdoor.jpg",
        "cat-baby.jpg",
        "cat-roleplay.jpg",
        "cat-gadgets.jpg",
        "team-amina.jpg",
        "team-hassan.jpg",
        "team-sana.jpg",
    ]:
        shrink(ROOT / name, 1080, 62)

    for path in (ROOT / "categories").glob("*.jpg"):
        shrink(path, 480, 68)

    products = ROOT / "products"
    for path in products.glob("*.jpg"):
        image = Image.open(path).convert("RGB")
        image.thumbnail((640, 640), Image.Resampling.LANCZOS)
        before = path.stat().st_size
        jpeg_save(image, path, 70)
        print(f"products/{path.name}: {before // 1024}kb -> {path.stat().st_size // 1024}kb {image.size}")


if __name__ == "__main__":
    main()
