from pathlib import Path

import imageio.v2 as imageio
import numpy as np
from PIL import Image

ROOT = Path(r"e:\Toys Lover")
IMG = ROOT / "public" / "images"
OUT = ROOT / "public" / "videos" / "hero-play.mp4"
OUT.parent.mkdir(parents=True, exist_ok=True)

FILES = [
    "hero-play.jpg",
    "hero-kids-2.jpg",
    "hero-kids-3.jpg",
    "banner-garden-play.jpg",
]

WIDTH, HEIGHT = 1280, 720
FPS = 20
SECONDS = 2.8


def cover(path: Path, width: int, height: int) -> Image.Image:
    image = Image.open(path).convert("RGB")
    scale = max(width / image.width, height / image.height)
    size = (int(image.width * scale) + 1, int(image.height * scale) + 1)
    image = image.resize(size, Image.LANCZOS)
    left = max(0, (image.width - width) // 2)
    top = max(0, (image.height - height) // 2)
    return image.crop((left, top, left + width, top + height))


def main() -> None:
    writer = imageio.get_writer(
        str(OUT),
        fps=FPS,
        codec="libx264",
        ffmpeg_params=[
            "-pix_fmt",
            "yuv420p",
            "-crf",
            "23",
            "-preset",
            "veryfast",
            "-movflags",
            "+faststart",
        ],
    )
    frames = int(FPS * SECONDS)
    try:
        for index, name in enumerate(FILES):
            base = cover(IMG / name, int(WIDTH * 1.16), int(HEIGHT * 1.16))
            for step in range(frames):
                progress = step / max(frames - 1, 1)
                pan = progress if index % 2 == 0 else 1 - progress
                max_x = base.width - WIDTH
                max_y = base.height - HEIGHT
                x = int(max_x * pan)
                y = int(max_y * (0.25 + 0.5 * progress))
                frame = base.crop((x, y, x + WIDTH, y + HEIGHT))
                writer.append_data(np.asarray(frame))
    finally:
        writer.close()
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
