"""Import Toys Advance Category: HD white frames + product records."""

from __future__ import annotations

import json
import re
from pathlib import Path

import numpy as np
from PIL import Image, ImageEnhance, ImageOps

ROOT = Path(r"e:\Toys Lover")
SRC = ROOT / "Toys Advance Category"
PRODUCT_DIR = ROOT / "public" / "images" / "products"
CATEGORY_DIR = ROOT / "public" / "images" / "categories"
OUT_TS = ROOT / "lib" / "data" / "advance-stock.ts"

CANVAS = 1400
INNER = 0.86
WHITE = (255, 255, 255)

# first-match folder rules: needle, category, price, slug-prefix, title, age, brand, theme, short, materials
RULES = [
    ("big bag", "monster-buddy-bags", 11.50, "monster-buddy-big-bag", "Monster Buddy Big Bag", "9-12 years", "Street Fun", "Bags", "Roomy monster-buddy bag from the new tray — photographed so the face and zip sit clear.", "Soft plush pile, zip pouch, polyester lining."),
    ("3.1", "monster-buddy-bags", 11.50, "monster-buddy-big-bag", "Monster Buddy Big Bag", "9-12 years", "Street Fun", "Bags", "Roomy monster-buddy bag from the new tray — photographed so the face and zip sit clear.", "Soft plush pile, zip pouch, polyester lining."),
    ("dragon", "hatch-dragons", 2.50, "hatch-dragon-egg", "Hatch Dragon Egg", "6-8 years", "Forge & Fun", "Surprise", "3D hatch egg with a mini dragon inside — a pocket surprise from the new delivery.", "Plastic egg shell, mini dragon figure."),
    ("fashion", "fashion-play-sets", 2.50, "fashion-play-set", "Fashion Play Set", "6-8 years", "Stage Pop", "Dress-up", "Pocket fashion play set from the new tray — bright colours, ready for a dresser drawer.", "Plastic accessories, card backing."),
    ("(l)", "monster-buddy-bags", 4.50, "monster-buddy-large-bag", "Monster Buddy Large Bag", "6-8 years", "Street Fun", "Bags", "Large monster-buddy bag — a carry-along plush pouch from the new delivery.", "Soft plush pile, zip pouch."),
    ("(m)", "monster-buddy-bags", 3.50, "monster-buddy-medium-bag", "Monster Buddy Medium Bag", "6-8 years", "Street Fun", "Bags", "Medium monster-buddy bag — a mid-size plush pouch from the new tray.", "Soft plush pile, zip pouch."),
    ("small bag", "monster-buddy-bags", 2.50, "monster-buddy-small-bag", "Monster Buddy Small Bag", "3-5 years", "Street Fun", "Bags", "Small monster-buddy bag — a first zip pouch from the new delivery.", "Soft plush pile, zip pouch."),
    ("plush key", "pocket-critter-keyrings", 1.25, "pocket-critter-keyring", "Pocket Critter Keyring", "3-5 years", "Nest & Wool", "Keyrings", "Soft pocket-critter plush charm — a hug-size clip from the new tray.", "Plush pile, polyester fill, metal ring."),
    ("pok", "pocket-critter-keyrings", 1.25, "pocket-critter-keyring", "Pocket Critter Keyring", "3-5 years", "Nest & Wool", "Keyrings", "Soft pocket-critter plush charm — a hug-size clip from the new tray.", "Plush pile, polyester fill, metal ring."),
    ("metal", "metal-keyrings", 1.25, "metal-charm-keyring", "Metal Charm Keyring", "9-12 years", "Street Fun", "Keyrings", "Metal charm keyring from the new tray — a solid desk-and-bag clip.", "Alloy charm, metal ring."),
    ("keyring", "monster-buddy-keyrings", 0.90, "monster-buddy-keyring", "Monster Buddy Keyring", "6-8 years", "Street Fun", "Keyrings", "Soft monster-buddy charm on a clip — bag-ready from the new tray.", "Soft PVC or plush charm, metal ring."),
    ("light up hat", "light-up-hats", 2.50, "light-up-party-hat", "Light-Up Party Hat", "6-8 years", "Party Glow", "Lights", "LED party hat from the new tray — brim lights for photos and play.", "Felt or knit hat, LED brim, batteries as labelled."),
    ("shoulder", "mini-shoulder-bags", 1.75, "mini-shoulder-bag", "Mini Shoulder Bag", "9-12 years", "Street Fun", "Bags", "Mini shoulder bag from the 12-in-bag pack — a first cross-body for days out.", "Printed fabric, adjustable strap."),
    ("push game", "push-pop-games", 2.50, "push-pop-game", "Push Pop Game", "6-8 years", "Street Fun", "Gadgets", "Handheld push-pop speed game from the new tray — lights and bubbles, no extra screen.", "ABS shell, silicone bubbles, LED board."),
    ("cup", "star-buddy-cups", 3.00, "star-buddy-cup", "Star Buddy Cup", "3-5 years", "Nest & Wool", "Drinkware", "Character cup from the new tray — a colourful sipper for snack time.", "Plastic cup, character lid."),
    ("plush toy", "star-buddy-plush", 3.50, "star-buddy-plush", "Star Buddy Plush", "3-5 years", "Nest & Wool", "Comfort", "Soft star-buddy plush from the new delivery — a hug-size friend with stitched features.", "Plush pile, polyester fill, embroidered face."),
    ("labubu bag", "monster-buddy-bags", 4.50, "monster-buddy-bag", "Monster Buddy Bag", "6-8 years", "Street Fun", "Bags", "Monster-buddy bag from the new tray — a zip pouch with a clear face.", "Soft plush pile, zip pouch."),
    ("bags put", "monster-buddy-bags", 4.50, "monster-buddy-bag", "Monster Buddy Bag", "6-8 years", "Street Fun", "Bags", "Monster-buddy bag from the new tray — a zip pouch with a clear face.", "Soft plush pile, zip pouch."),
]

SAFETY = {
    "3-5 years": "Ages 3+. Use under adult supervision. Keep small parts away from under-threes.",
    "6-8 years": "Ages 6+. Not a food item. Supervise first use of lights and batteries.",
    "9-12 years": "Ages 9+. Remove tags and packaging before gifting. Batteries as labelled.",
    "13+ years": "Ages 13+ / teen desk toy. Small parts — not for young children.",
}

FEATURES = {
    "monster-buddy-bags": ["Zip pouch", "Plush face", "Carry-along", "New delivery"],
    "hatch-dragons": ["Hatch egg", "Mini dragon", "Pocket size", "Ages 6+"],
    "fashion-play-sets": ["Dress-up set", "Bright colours", "Pocket box", "Ages 6+"],
    "monster-buddy-keyrings": ["Bag clip", "Soft charm", "Metal ring", "Ages 6+"],
    "light-up-hats": ["LED brim", "Party photos", "One size kids", "Ages 6+"],
    "metal-keyrings": ["Metal charm", "Bag clip", "Desk fidget", "Ages 9+"],
    "mini-shoulder-bags": ["Mini cross-body", "Adjustable strap", "12-in-bag pack", "Ages 9+"],
    "pocket-critter-keyrings": ["Plush charm", "Soft pile", "Bag clip", "Ages 3+"],
    "push-pop-games": ["Push-pop play", "Light-up", "Handheld", "Ages 6+"],
    "star-buddy-cups": ["Character lid", "Snack-time cup", "Bright colour", "Ages 3+"],
    "star-buddy-plush": ["Hug size", "Soft pile", "Stitched face", "Ages 3+"],
}


def folder_norm(name: str) -> str:
    n = name.lower().replace("£", " ").replace("kirings", "keyrings").replace("stich", "stitch")
    n = n.replace("labubu", "labubu")
    return n


def match_rule(folder_name: str):
    n = folder_norm(folder_name)
    for rule in RULES:
        if rule[0] in n:
            return rule
    return None


def images_in(folder: Path) -> list[Path]:
    return sorted(
        [p for p in folder.iterdir() if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}],
        key=lambda p: p.name.lower(),
    )


def polish(im: Image.Image) -> Image.Image:
    im = ImageOps.exif_transpose(im).convert("RGB")
    im = ImageEnhance.Contrast(im).enhance(1.08)
    im = ImageEnhance.Color(im).enhance(1.08)
    im = ImageEnhance.Sharpness(im).enhance(1.2)
    im = ImageEnhance.Brightness(im).enhance(1.03)
    return im


def studio_bg(rgb: np.ndarray) -> tuple[int, int, int]:
    border = np.concatenate(
        [
            rgb[:10, :, :].reshape(-1, 3),
            rgb[-10:, :, :].reshape(-1, 3),
            rgb[:, :10, :].reshape(-1, 3),
            rgb[:, -10:, :].reshape(-1, 3),
        ]
    )
    return tuple(int(v) for v in np.median(border, axis=0))


def content_box(rgb: np.ndarray) -> tuple[int, int, int, int]:
    h, w = rgb.shape[:2]
    bg = np.array(studio_bg(rgb), dtype=np.float32)
    dist = np.linalg.norm(rgb.astype(np.float32) - bg, axis=2)
    mask = dist > max(18.0, float(np.percentile(dist, 50)) * 0.4)
    if mask.mean() > 0.9:
        mask = dist > float(np.percentile(dist, 38))
    if mask.mean() < 0.02:
        return 0, 0, w - 1, h - 1
    ys, xs = np.where(mask)
    pad = int(0.06 * max(w, h))
    return (
        max(0, int(xs.min()) - pad),
        max(0, int(ys.min()) - pad),
        min(w - 1, int(xs.max()) + pad),
        min(h - 1, int(ys.max()) + pad),
    )


def frame_hd(src: Path, dest: Path) -> None:
    im = polish(Image.open(src))
    rgb = np.asarray(im)
    left, top, right, bot = content_box(rgb)
    crop = im.crop((left, top, right + 1, bot + 1))
    max_side = int(CANVAS * INNER)
    crop.thumbnail((max_side, max_side), Image.Resampling.LANCZOS)
    if max(crop.size) < 560:
        scale = 560 / max(crop.size)
        crop = crop.resize((max(1, int(crop.width * scale)), max(1, int(crop.height * scale))), Image.Resampling.LANCZOS)
        crop.thumbnail((max_side, max_side), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (CANVAS, CANVAS), WHITE)
    canvas.paste(crop, ((CANVAS - crop.width) // 2, (CANVAS - crop.height) // 2))
    dest.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(dest, format="JPEG", quality=93, optimize=True, subsampling=0)


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value


def ts_escape(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def emit_product(item: dict, index: int) -> str:
    stock = 16 + (index * 5) % 36
    features = ", ".join(ts_escape(f) for f in item["features"])
    extra = "\n    isNew: true,"
    if index % 8 == 0:
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
    description: {ts_escape(item["short"] + " Centred on a clean white frame so the toy stays sharp on every screen.")},
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
    used_slugs: set[str] = set()

    folders = [p for p in SRC.iterdir() if p.is_dir()]
    folders.sort(key=lambda p: p.name.lower())

    for folder in folders:
        rule = match_rule(folder.name)
        files = images_in(folder)
        if not files:
            print("skip empty", folder.name.encode("unicode_escape").decode())
            continue
        if not rule:
            print("UNMATCHED", folder.name.encode("unicode_escape").decode())
            continue
        _needle, cat, price, prefix, title, age, brand, theme, short, materials = rule
        print("aisle", cat, "x", len(files), "£", price)
        for i, src in enumerate(files, start=1):
            slug = f"{prefix}-{i:02d}" if len(files) > 1 else prefix
            while slug in used_slugs:
                slug = f"{slug}-b"
            used_slugs.add(slug)
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
            im = Image.open(src).convert("RGB")
            im.save(CATEGORY_DIR / f"{cat}.jpg", format="JPEG", quality=91, optimize=True)
            print("category", cat)

    body = ",\n".join(emit_product(item, i) for i, item in enumerate(records))
    OUT_TS.write_text(
        'import type { Product } from "@/lib/types";\n\n'
        "export const advanceStock: Product[] = [\n"
        f"{body}\n"
        "];\n",
        encoding="utf-8",
    )
    print("wrote", OUT_TS.name, "products", len(records), "aisles", len(heroes))


if __name__ == "__main__":
    main()
