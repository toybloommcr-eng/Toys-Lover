"""Import New Products folder: HD frames + october-new-stock.ts."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageEnhance, ImageOps

ROOT = Path(r"e:\Toys Lover")
SRC = ROOT / "New Products"
PRODUCT_DIR = ROOT / "public" / "images" / "products"
CATEGORY_DIR = ROOT / "public" / "images" / "categories"
OUT_TS = ROOT / "lib" / "data" / "october-new-stock.ts"

CANVAS = 1400
INNER = 0.86
WHITE = (255, 255, 255)

# Explicit catalog: filename, slug, name, box_price, single_each|None, pieces, category, age, brand, theme, short, materials, features
PRODUCTS = [
    (
        "1 GBP Each.jpeg",
        "christmas-super-squishy-box",
        "Christmas Super Squishy Collection",
        8.99,
        1.0,
        12,
        "christmas-surprise",
        "3-5 years",
        "Squish Lane",
        "Christmas",
        "Six Merry Christmas Super Squishy characters — Santa, snowman, gingerbread, elf, reindeer and tree. Sold as a full display box.",
        "Soft PU foam, clear gift box per piece.",
        ["Merry Christmas boxes", "6 character designs", "Complete items in box: 12 pcs", "Price £8.99 box · £1 each"],
    ),
    (
        "3D Printed Model.jpeg",
        "3d-printed-gear-ball",
        "3D Printed Gear Ball Model",
        24.99,
        2.5,
        16,
        "fidget-spinners",
        "9-12 years",
        "Forge & Fun",
        "Fidget",
        "Articulated 3D-printed gear balls in clear cubes. PLA biodegradable material, ages 8+. Full display tray of 16.",
        "PLA biodegradable plastic, clear display cube.",
        ["PLA biodegradable", "Clear cube each", "Complete items in box: 16 pcs", "Price £24.99 box · £2.50 each"],
    ),
    (
        "Big Into Energy 6GBP Each.jpeg",
        "big-into-energy-surprise",
        "Big Into Energy Surprise Box",
        6.0,
        None,
        24,
        "christmas-surprise",
        "3-5 years",
        "Squish Lane",
        "Surprise",
        "Big Into Energy surprise calendar-style box with 24 soft character figures. One full set per box at £6.",
        "Soft character figures, cardboard surprise tray.",
        ["24 surprise figures", "Calendar-style box", "Complete items in box: 24 pcs", "Price £6.00 box"],
    ),
    (
        "fidget spinning ball.jpeg",
        "fidget-spinning-ball",
        "Fidget Spinning Ball",
        19.99,
        2.5,
        12,
        "fidget-spinners",
        "6-8 years",
        "Street Fun",
        "Fidget",
        "Fingertip stress-relief spinning balls in individual galaxy boxes. Display tray holds 12 pcs.",
        "ABS segments, yellow button, retail gift box.",
        ["12 PCS display", "Smooth fingertip feel", "Complete items in box: 12 pcs", "Price £19.99 box · £2.50 each"],
    ),
    (
        "Fruit Combo Squish 1.5 GBP.jpeg",
        "fruit-combo-squishy",
        "Fruit Combo Squishy",
        12.99,
        1.5,
        12,
        "fruit-squishies",
        "3-5 years",
        "Squish Lane",
        "Fruit",
        "Fruit Combo Squishy assortment — peach, grape, mango, citrus and more. Labelled 12 PCS on the display lid.",
        "Soft PU / TPR sensory foam. Not a food item.",
        ["12 PCS labelled", "Bouncy & squishy soft", "Complete items in box: 12 pcs", "Price £12.99 box · £1.50 each"],
    ),
    (
        "WhatsApp Image 2026-10-10 at 8.42.55 PM (5).jpeg",
        "soft-cotton-fruit-squishy",
        "Soft Cotton Fruit Squishy",
        12.99,
        1.5,
        12,
        "fruit-squishies",
        "3-5 years",
        "Squish Lane",
        "Fruit",
        "Soft-as-cotton fruit squishies — strawberry, grape, mango, peach and orange. 12 pieces in the display tray.",
        "Soft PU / TPR sensory foam. Not a food item.",
        ["Soft as cotton", "Totally stress relieving", "Complete items in box: 12 pcs", "Price £12.99 box · £1.50 each"],
    ),
    (
        "New one.jpeg",
        "aircraft-tanks-2in1",
        "2 In 1 Aircraft & Tanks",
        12.99,
        None,
        1,
        "action-figures",
        "6-8 years",
        "DIDAI",
        "Vehicles",
        "Camouflage tank with fighter jet on top — battery omni-directional drive, music and spin lighting ball.",
        "ABS body, B/O chassis, LED lighting as labelled.",
        ["2-in-1 aircraft & tank", "Music & lights", "Omni-directional B/O", "Price £12.99"],
    ),
    (
        "Super Driver 3.50 GBP.jpeg",
        "super-driver-blue",
        "Super Driver Musical Wheel (Blue)",
        3.5,
        None,
        1,
        "role-play",
        "3-5 years",
        "ARREDO",
        "Driving",
        "ARREDO Super Driver interactive steering wheel — flashing lights and sound effects. Blue grip edition at £3.50.",
        "ABS steering wheel, electronic lights and sounds, batteries as labelled.",
        ["Flashing lights & sounds", "Try-me packaging", "Ages 3+", "Price £3.50"],
    ),
    (
        "WhatsApp Image 2026-10-10 at 8.42.55 PM (2).jpeg",
        "super-driver-red",
        "Super Driver Musical Wheel (Red)",
        3.5,
        None,
        1,
        "role-play",
        "3-5 years",
        "ARREDO",
        "Driving",
        "ARREDO Super Driver interactive steering wheel — flashing lights and sound effects. Red grip edition at £3.50.",
        "ABS steering wheel, electronic lights and sounds, batteries as labelled.",
        ["Flashing lights & sounds", "Try-me packaging", "Ages 3+", "Price £3.50"],
    ),
    (
        "£2 each 24 in box.jpeg",
        "dumpling-face-squishy-24",
        "Dumpling Face Squishy",
        35.99,
        2.0,
        24,
        "festive-dumplings",
        "6-8 years",
        "Squish Lane",
        "Food",
        "Kawaii dumpling / bao squishies in blue, pink, cream and rainbow. £2 each — full box holds 24 pcs.",
        "Soft PU / TPR sensory foam. Not a food item.",
        ["£2 each", "Stretchy spiral dumpling", "Complete items in box: 24 pcs", "Price £35.99 box"],
    ),
    (
        "£6 each.jpeg",
        "squishy-surprise-bag",
        "Squishy Surprise Bag",
        6.0,
        None,
        1,
        "glitter-squeeze",
        "6-8 years",
        "Squish Lane",
        "Surprise",
        "Squishy Surprise Bag — 100+ styles to collect. Squeeze, stretch and squish. £6 each bag.",
        "Assorted soft PU / gel sensory toys. Not a food item.",
        ["100+ styles", "Squeeze stretch squish", "Surprise assortment", "Price £6.00 each"],
    ),
    (
        "£9.50 each item.jpeg",
        "fluffy-monster-bag-charm",
        "Fluffy Monster Bag Charm",
        9.5,
        None,
        1,
        "dolls-plush",
        "6-8 years",
        "Nest & Wool",
        "Plush",
        "Ultra-fluffy round plush bag charms in pink, grey and cream. Soft faux fur — £9.50 each item.",
        "Faux fur pile, polyester fill, bead eyes.",
        ["Ultra-soft faux fur", "Bag / vanity charm", "Pink grey cream colours", "Price £9.50 each"],
    ),
    (
        "£9.50 each.jpeg",
        "needoh-tis-the-squeeze",
        "NeeDoh Tis The Squeeze Set",
        9.5,
        None,
        12,
        "glitter-squeeze",
        "6-8 years",
        "NeeDoh",
        "Sensory",
        "NeeDoh Tis The Squeeze variety set — burger, ice cream, glitter bear, jellyfish and more. 12 pieces in the tray at £9.50.",
        "NeeDoh sensory gel / foam. Not a food item.",
        ["12 unique NeeDoh styles", "Surprise door box", "Complete items in box: 12 pcs", "Price £9.50 set"],
    ),
    (
        "WhatsApp Image 2026-10-10 at 8.42.55 PM.jpeg",
        "gear-train-transparent",
        "Gear Train Transparent",
        9.99,
        None,
        1,
        "educational-stem",
        "3-5 years",
        "YJ Toys",
        "Trains",
        "Transparent GEAR Train with visible colourful gears, music and lights. Battery electric function.",
        "Clear ABS body, coloured gears, B/O lights and music.",
        ["Transparent gear body", "Music & light", "Electric function", "Price £9.99"],
    ),
    (
        "WhatsApp Image 2026-10-10 at 8.42.55 PM (1).jpeg",
        "marine-swat-justice-ship",
        "Marine Swat Justice Ship",
        8.99,
        None,
        1,
        "action-figures",
        "3-5 years",
        "GHD Europe",
        "Vehicles",
        "Marine Swat Police Justice Ship — 360° bump-and-go movement with cabin lights and music.",
        "ABS hull, LED cabin lights, B/O chassis.",
        ["360° movement", "Lights & music", "Police boat play", "Price £8.99"],
    ),
    (
        "WhatsApp Image 2026-10-10 at 8.42.55 PM (3).jpeg",
        "colorful-gear-sport-car",
        "Colorful Gear Sport Car",
        7.99,
        None,
        1,
        "action-figures",
        "3-5 years",
        "OPO Europe",
        "Vehicles",
        "Transparent Colorful Sport Car with dynamic internal gears, colourful lighting and music. Ages 3+.",
        "Clear ABS shell, coloured gears, LED and sound.",
        ["Gear design visible", "Colourful lighting music", "Ages 3+", "Price £7.99"],
    ),
    (
        "WhatsApp Image 2026-10-10 at 8.44.41 PM.jpeg",
        "mermaid-bath-bomb-gift",
        "Mermaid Bath Bomb Gift Box",
        9.99,
        None,
        12,
        "bath-bomb-gifts",
        "6-8 years",
        "Bath Bloom",
        "Bath",
        "Mermaid bath bombs with a surprise toy inside. 12 colourful bombs plus collectible sea charms in the gift box.",
        "Bath bomb 60g class, plastic surprise charm. Adult supervision in bath.",
        ["Surprise toy inside", "Complete items in box: 12 pcs", "Mermaid undersea theme", "Price £9.99 box"],
    ),
    (
        "WhatsApp Image 2026-10-10 at 8.44.41 PM (1).jpeg",
        "animal-bath-bomb-gift",
        "Animal Bath Bomb Gift Box",
        9.99,
        None,
        12,
        "bath-bomb-gifts",
        "6-8 years",
        "Bath Bloom",
        "Bath",
        "Forest animal bath bomb gift — 12 bombs with hidden mini animals (tiger, giraffe, rabbit and more).",
        "Bath bomb ~60g, plastic surprise figure. Adult supervision in bath.",
        ["Hidden toy inside", "Complete items in box: 12 pcs", "12 animal charms", "Price £9.99 box"],
    ),
    (
        "WhatsApp Image 2026-10-10 at 8.44.42 PM.jpeg",
        "sea-bath-bomb-gift",
        "Sea Bath Bomb Gift Box",
        9.99,
        None,
        12,
        "bath-bomb-gifts",
        "6-8 years",
        "Bath Bloom",
        "Bath",
        "Ocean-theme bath bomb gift box — 12 bombs (≈5.3 cm / 60g) with a surprise sea toy inside.",
        "Bath bomb ~60g, plastic surprise figure. Adult supervision in bath.",
        ["Surprise sea toy", "Complete items in box: 12 pcs", "22.5×16.2×5.5 cm box", "Price £9.99 box"],
    ),
    (
        "WhatsApp Image 2026-10-10 at 8.44.42 PM (1).jpeg",
        "candy-house-bath-bombs",
        "Candy House Bath Bombs",
        9.99,
        None,
        12,
        "bath-bomb-gifts",
        "6-8 years",
        "Bath Bloom",
        "Bath",
        "Candy House series bath bombs (STC-0275) — 12 PCS display with sweet surprise charms. Master carton 288 pcs.",
        "Bath bomb 60g / Ø4.8 cm, plastic charm. Adult supervision in bath.",
        ["STC-0275", "Complete items in box: 12 pcs", "Surprise toy inside", "Price £9.99 box"],
    ),
    (
        "WhatsApp Image 2026-10-10 at 8.44.42 PM (2).jpeg",
        "ocean-series-bath-bombs",
        "Ocean Series Bath Bombs",
        9.99,
        None,
        12,
        "bath-bomb-gifts",
        "6-8 years",
        "Bath Bloom",
        "Bath",
        "Ocean series bath bombs (STC-0272) — 12 PCS with mermaid, octopus, whale and shell surprises.",
        "Bath bomb 60g / Ø4.8 cm, plastic charm. Adult supervision in bath.",
        ["STC-0272", "Complete items in box: 12 pcs", "Ocean surprise toys", "Price £9.99 box"],
    ),
]

SAFETY = {
    "3-5 years": "Ages 3+. Use under adult supervision. Keep small parts away from under-threes.",
    "6-8 years": "Ages 6+. Not a food item unless labelled bath-safe. Supervise bath play and batteries.",
    "9-12 years": "Ages 9+. Remove tags and packaging before gifting. Batteries as labelled.",
}


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
        crop = crop.resize(
            (max(1, int(crop.width * scale)), max(1, int(crop.height * scale))),
            Image.Resampling.LANCZOS,
        )
        crop.thumbnail((max_side, max_side), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (CANVAS, CANVAS), WHITE)
    canvas.paste(crop, ((CANVAS - crop.width) // 2, (CANVAS - crop.height) // 2))
    dest.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(dest, format="JPEG", quality=93, optimize=True, subsampling=0)


def ts_escape(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def find_src(filename: str) -> Path | None:
    direct = SRC / filename
    if direct.exists():
        return direct
    target = filename.lower()
    for p in SRC.iterdir():
        if p.name.lower() == target:
            return p
    # £ may be mojibake on Windows — match by distinctive stems
    aliases = {
        "£2 each 24 in box.jpeg": lambda n: "24 in box" in n.lower(),
        "£6 each.jpeg": lambda n: "6 each" in n.lower() and "24" not in n.lower() and "big" not in n.lower() and "9.50" not in n.lower(),
        "£9.50 each item.jpeg": lambda n: "9.50 each item" in n.lower(),
        "£9.50 each.jpeg": lambda n: "9.50 each" in n.lower() and "item" not in n.lower(),
    }
    matcher = aliases.get(filename)
    if matcher:
        for p in SRC.iterdir():
            if matcher(p.name):
                return p
    return None


def emit(item: dict, index: int) -> str:
    stock = max(item["pieces"] * 2, 12 + (index * 3) % 40)
    features = ", ".join(ts_escape(f) for f in item["features"])
    compare = ""
    if item["each"] is not None:
        compare = f"\n    compareAtPrice: {item['each']},"
    pieces = ""
    if item["pieces"] > 1:
        pieces = f"\n    piecesPerBox: {item['pieces']},"
    return f"""  {{
    slug: {ts_escape(item["slug"])},
    name: {ts_escape(item["name"])},
    price: {item["price"]},{compare}
    ageRange: {ts_escape(item["age"])},
    brand: {ts_escape(item["brand"])},
    theme: {ts_escape(item["theme"])},
    categorySlug: {ts_escape(item["cat"])},
    images: [],
    shortDescription: {ts_escape(item["short"])},
    description: {ts_escape(item["short"] + " Photographed from the New Products delivery in a sharp HD white frame.")},
    features: [{features}],
    safety: {ts_escape(SAFETY[item["age"]])},
    materials: {ts_escape(item["materials"])},
    isNew: true,
    isBestSeller: true,{pieces}
    stock: {stock},
  }}"""


def main() -> None:
    PRODUCT_DIR.mkdir(parents=True, exist_ok=True)
    CATEGORY_DIR.mkdir(parents=True, exist_ok=True)

    records = []
    heroes: dict[str, str] = {}

    for i, row in enumerate(PRODUCTS):
        filename, slug, name, price, each, pieces, cat, age, brand, theme, short, materials, features = row
        src = find_src(filename)
        if not src:
            print("MISSING", filename.encode("unicode_escape").decode())
            continue
        dest = PRODUCT_DIR / f"{slug}.jpg"
        frame_hd(src, dest)
        print(f"{slug}: {dest.stat().st_size // 1024}kb from {src.name.encode('unicode_escape').decode()}")
        records.append(
            {
                "slug": slug,
                "name": name,
                "price": price,
                "each": each,
                "pieces": pieces,
                "cat": cat,
                "age": age,
                "brand": brand,
                "theme": theme,
                "short": short,
                "materials": materials,
                "features": features,
            }
        )
        heroes.setdefault(cat, slug)

    for cat, slug in heroes.items():
        src = PRODUCT_DIR / f"{slug}.jpg"
        if src.exists() and cat == "bath-bomb-gifts":
            im = Image.open(src).convert("RGB")
            im.save(CATEGORY_DIR / f"{cat}.jpg", format="JPEG", quality=91, optimize=True)
            print("category hero", cat)

    body = ",\n".join(emit(item, i) for i, item in enumerate(records))
    OUT_TS.write_text(
        'import type { Product } from "@/lib/types";\n\n'
        "export const octoberNewStock: Product[] = [\n"
        f"{body}\n"
        "];\n",
        encoding="utf-8",
    )
    print("wrote", OUT_TS.name, "products", len(records))


if __name__ == "__main__":
    main()
