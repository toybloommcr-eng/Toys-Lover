"""Import Toys Extra Category: HD white frames + aisle records."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageEnhance, ImageOps

ROOT = Path(r"e:\Toys Lover")
SRC = ROOT / "Toys Extra Category"
PRODUCT_DIR = ROOT / "public" / "images" / "products"
CATEGORY_DIR = ROOT / "public" / "images" / "categories"
OUT_TS = ROOT / "lib" / "data" / "extra-stock.ts"

CANVAS = 1400
INNER = 0.93
WHITE = (255, 255, 255)

# first-match: needle, cat, price, prefix, title, age, brand, theme, short, materials
RULES = [
    ("crunchy", "crunchy-squishies", 2.50, "crunchy-squishy", "Crunchy Squishy", "6-8 years", "Squish Lane", "Sensory", "Slow-rise crunchy squishy from the extra tray — a pocket fidget with a crackly fill.", "PU foam, crunchy beads."),
    ("funky", "funky-frights", 7.50, "funky-fright", "Funky Fright Set", "6-8 years", "Squish Lane", "Halloween", "Neon Halloween squeeze set from the extra tray — ghosts, pumpkins, and party glow.", "Slow-rise foam, mixed Halloween shapes."),
    # 2.75 folder must beat "mini" (inside "minimum")
    ("2.75", "glow-swords", 2.75, "pixel-glow-sword", "Pixel Glow Sword", "6-8 years", "Party Glow", "Lights", "Pixel glow sword with batteries — a light-up play sword from the extra tray.", "LED plastic, batteries included as labelled."),
    ("batteries", "glow-swords", 2.75, "pixel-glow-sword", "Pixel Glow Sword", "6-8 years", "Party Glow", "Lights", "Pixel glow sword with batteries — a light-up play sword from the extra tray.", "LED plastic, batteries included as labelled."),
    ("mini grinch", "festive-dumplings", 1.75, "mini-festive-dumpling", "Mini Festive Dumpling", "6-8 years", "Squish Lane", "Sensory", "Mini festive dumpling squeeze — a pocket-money fidget from the extra tray.", "Slow-rise foam, printed wrapper."),
    ("dumpling", "festive-dumplings", 2.25, "festive-dumpling", "Festive Dumpling Squeeze", "6-8 years", "Squish Lane", "Sensory", "Festive dumpling squeeze from the extra tray — a slow-rise fidget in holiday wrap.", "Slow-rise foam, printed wrapper."),
    ("grinch", "festive-dumplings", 2.25, "festive-dumpling", "Festive Dumpling Squeeze", "6-8 years", "Squish Lane", "Sensory", "Festive dumpling squeeze from the extra tray — a slow-rise fidget in holiday wrap.", "Slow-rise foam, printed wrapper."),
    ("light up hat", "light-up-hats", 3.50, "glow-party-hat", "Glow Party Hat", "6-8 years", "Party Glow", "Lights", "Light-up party hat at £3.50 from the extra tray — brim glow for photos.", "Hat with LED brim, batteries as labelled."),
    ("halloween hat", "halloween-hats", 2.50, "halloween-party-hat", "Halloween Party Hat", "6-8 years", "Party Glow", "Halloween", "Halloween party hat from the extra pack — dress-up for photos and trick-or-treat.", "Felt or knit hat, party print."),
    ("halloween squish", "halloween-squishies", 2.25, "halloween-tray-squishy", "Halloween Tray Squishy", "6-8 years", "Squish Lane", "Halloween", "Halloween tray squishy from the extra box — pumpkins, bats, and trick-or-treat wraps.", "Slow-rise PU foam."),
    ("glasses", "light-up-glasses", 2.50, "light-up-shutter-glasses", "Light-Up Shutter Glasses", "9-12 years", "Party Glow", "Lights", "LED shutter glasses from the extra tray — party colours that light the brim.", "LED plastic, batteries as labelled."),
    ("gloves", "light-up-gloves", 2.50, "light-up-party-gloves", "Light-Up Party Gloves", "6-8 years", "Party Glow", "Lights", "LED party gloves from the extra pack — fingers light up for night play.", "Knit glove, LED tips, batteries as labelled."),
    ("7cm", "cheese-squishies", 4.75, "jumbo-cheese-squishy", "Jumbo Cheese Squishy", "6-8 years", "Squish Lane", "Sensory", "7 cm jumbo cheese squishy — a slow-rise butter-brick fidget from the extra pack.", "PU foam cheese brick."),
    ("4.75", "cheese-squishies", 4.75, "jumbo-cheese-squishy", "Jumbo Cheese Squishy", "6-8 years", "Squish Lane", "Sensory", "7 cm jumbo cheese squishy — a slow-rise butter-brick fidget from the extra pack.", "PU foam cheese brick."),
    ("cheese", "cheese-squishies", 2.50, "mini-cheese-squishy", "Mini Cheese Squishy", "6-8 years", "Squish Lane", "Sensory", "5 cm mini cheese squishy — a pocket butter-brick fidget from the extra pack.", "PU foam cheese brick."),
    ("vaseline", "cheese-squishies", 2.50, "mini-cheese-squishy", "Mini Cheese Squishy", "6-8 years", "Squish Lane", "Sensory", "5 cm mini cheese squishy — a pocket butter-brick fidget from the extra pack.", "PU foam cheese brick."),
]

SAFETY = {
    "3-5 years": "Ages 3+. Use under adult supervision. Keep small parts away from under-threes.",
    "6-8 years": "Ages 6+. Not a food item. Supervise first use of lights and batteries.",
    "9-12 years": "Ages 9+. Remove tags and packaging before gifting. Batteries as labelled.",
    "13+ years": "Ages 13+ / teen desk toy. Small parts — not for young children.",
}

FEATURES = {
    "crunchy-squishies": ["Crunchy fill", "Slow rise", "Pocket size", "Ages 6+"],
    "funky-frights": ["Halloween mix", "Neon squeezes", "Party tray", "Ages 6+"],
    "festive-dumplings": ["Dumpling shape", "Slow rise", "Festive wrap", "Ages 6+"],
    "halloween-hats": ["Party hat", "Halloween print", "Dress-up", "Ages 6+"],
    "halloween-squishies": ["Slow rise", "Halloween wrap", "Tray pick", "Ages 6+"],
    "light-up-glasses": ["LED shutters", "Party colours", "Batteries as labelled", "Ages 9+"],
    "light-up-gloves": ["LED fingertips", "Night play", "Pair", "Ages 6+"],
    "light-up-hats": ["LED brim", "Party photos", "One size kids", "Ages 6+"],
    "cheese-squishies": ["Cheese brick", "Slow rise", "Desk fidget", "Ages 6+"],
    "glow-swords": ["Pixel glow", "Batteries included", "Play sword", "Ages 6+"],
}


def folder_norm(name: str) -> str:
    return name.lower().replace("£", " ").replace("haloween", "halloween")


def match_rule(folder_name: str):
    n = folder_norm(folder_name)
    for rule in RULES:
        if rule[0] in n:
            return rule
    return None


def images_in(folder: Path) -> list[Path]:
    files = sorted(
        [p for p in folder.iterdir() if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}],
        key=lambda p: p.name.lower(),
    )
    return [p for p in files if p.stat().st_size >= 20000]


def polish(im: Image.Image) -> Image.Image:
    im = ImageOps.exif_transpose(im).convert("RGB")
    im = ImageEnhance.Contrast(im).enhance(1.08)
    im = ImageEnhance.Color(im).enhance(1.07)
    im = ImageEnhance.Sharpness(im).enhance(1.16)
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
    pad = int(0.035 * max(w, h))
    return max(0, int(xs.min()) - pad), max(0, int(ys.min()) - pad), min(w - 1, int(xs.max()) + pad), min(h - 1, int(ys.max()) + pad)


def frame_hd(src: Path, dest: Path) -> None:
    im = polish(Image.open(src))
    left, top, right, bot = content_box(im)
    crop = im.crop((left, top, right + 1, bot + 1))
    max_side = int(CANVAS * INNER)
    crop.thumbnail((max_side, max_side), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (CANVAS, CANVAS), WHITE)
    canvas.paste(crop, ((CANVAS - crop.width) // 2, (CANVAS - crop.height) // 2))
    dest.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(dest, format="JPEG", quality=93, optimize=True, subsampling=0)


def ts_escape(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def emit_product(item: dict, index: int) -> str:
    stock = 14 + (index * 6) % 38
    features = ", ".join(ts_escape(f) for f in item["features"])
    extra = "\n    isNew: true,"
    if index % 6 == 0:
        extra += "\n    isBestSeller: true,"
    return f"""  {{
    slug: {ts_escape(item["slug"])},
    name: {ts_escape(item["name"])},
    price: {item["price"]},
    ageRange: {ts_escape(item["age"])},
    brand: {ts_escape(item["brand"])},
    theme: {ts_escape(item["theme"])},
    categorySlug: {ts_escape(item["cat"])},
    images: [],
    shortDescription: {ts_escape(item["short"])},
    description: {ts_escape(item["short"] + " Photographed on a clean white frame so the toy stays sharp on every screen.")},
    features: [{features}],
    safety: {ts_escape(SAFETY[item["age"]])},
    materials: {ts_escape(item["materials"])},{extra}
    stock: {stock},
  }}"""


def main() -> None:
    PRODUCT_DIR.mkdir(parents=True, exist_ok=True)
    CATEGORY_DIR.mkdir(parents=True, exist_ok=True)
    records = []
    heroes: dict[str, str] = {}
    used: set[str] = set()

    folders = sorted([p for p in SRC.iterdir() if p.is_dir()], key=lambda p: p.name.lower())
    for folder in folders:
        rule = match_rule(folder.name)
        files = images_in(folder)
        label = folder.name.encode("unicode_escape").decode()
        if not files:
            print("skip empty/tiny", label)
            continue
        if not rule:
            print("UNMATCHED", label)
            continue
        _n, cat, price, prefix, title, age, brand, theme, short, materials = rule
        print("aisle", cat, "x", len(files), "GBP", price)
        for i, src in enumerate(files, start=1):
            slug = f"{prefix}-{i:02d}" if len(files) > 1 else prefix
            while slug in used:
                slug = f"{slug}-b"
            used.add(slug)
            name = title if len(files) == 1 else f"{title} {i:02d}"
            dest = PRODUCT_DIR / f"{slug}.jpg"
            frame_hd(src, dest)
            print(f"  {slug}: {dest.stat().st_size // 1024}kb")
            records.append(
                {
                    "slug": slug,
                    "name": name,
                    "price": price,
                    "age": age,
                    "brand": brand,
                    "theme": theme,
                    "short": short,
                    "cat": cat,
                    "features": FEATURES[cat],
                    "materials": materials,
                }
            )
            heroes.setdefault(cat, slug)

    for cat, slug in heroes.items():
        src = PRODUCT_DIR / f"{slug}.jpg"
        if src.exists():
            Image.open(src).convert("RGB").save(CATEGORY_DIR / f"{cat}.jpg", format="JPEG", quality=92, optimize=True)
            print("category", cat)

    body = ",\n".join(emit_product(item, i) for i, item in enumerate(records))
    OUT_TS.write_text(
        'import type { Product } from "@/lib/types";\n\n'
        "export const extraStock: Product[] = [\n"
        f"{body}\n"
        "];\n",
        encoding="utf-8",
    )
    print("wrote", OUT_TS.name, "products", len(records), "aisles", len(heroes))


if __name__ == "__main__":
    main()
