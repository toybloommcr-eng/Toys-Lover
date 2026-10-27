from pathlib import Path
from PIL import Image

ASSETS = Path(r"C:\Users\Nouman Faiz\.cursor\projects\e-Toys-Lover\assets")
PRODUCTS = Path(r"e:\Toys Lover\public\images\products")
WHITE = (255, 255, 255)
SIZE = 800

NEW = [
    "dumpling-pop-spinner.png",
    "sunshine-squeeze-blob.png",
    "unicorn-snuggle-plush.png",
    "mermaid-dress-up-set.png",
    "twin-track-rc-set.png",
    "beach-bucket-set.png",
    "swirl-ice-cream-squishy.png",
    "cheddar-block-squishy.png",
]


def fit_square(im: Image.Image) -> Image.Image:
    im = im.convert("RGB")
    im.thumbnail((SIZE, SIZE), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (SIZE, SIZE), WHITE)
    x = (SIZE - im.width) // 2
    y = (SIZE - im.height) // 2
    canvas.paste(im, (x, y))
    return canvas


def main() -> None:
    for name in NEW:
        src = ASSETS / name
        if not src.exists():
            print("missing", src)
            continue
        dst = PRODUCTS / (Path(name).stem + ".jpg")
        fit_square(Image.open(src)).save(dst, format="JPEG", quality=78, optimize=True, subsampling=1)
        print("wrote", dst.name, dst.stat().st_size)

    for path in PRODUCTS.glob("*.jpg"):
        im = Image.open(path).convert("RGB")
        if max(im.size) > SIZE:
            im.thumbnail((SIZE, SIZE), Image.Resampling.LANCZOS)
        canvas = Image.new("RGB", (SIZE, SIZE), WHITE)
        x = (SIZE - im.width) // 2
        y = (SIZE - im.height) // 2
        canvas.paste(im, (x, y))
        canvas.save(path, format="JPEG", quality=78, optimize=True, subsampling=1)
        print("compressed", path.name, path.stat().st_size)


if __name__ == "__main__":
    main()
