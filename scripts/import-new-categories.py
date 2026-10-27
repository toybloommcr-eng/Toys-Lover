"""Import Toys New Categories: HD centred photos + product records."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageEnhance, ImageOps

ROOT = Path(r"e:\Toys Lover")
SRC = ROOT / "Toys New Categories"
PRODUCT_DIR = ROOT / "public" / "images" / "products"
CATEGORY_DIR = ROOT / "public" / "images" / "categories"
OUT_TS = ROOT / "lib" / "data" / "new-stock.ts"

CANVAS = 1200
INNER = 0.84
WHITE = (255, 255, 255)

SAFETY = {
    "3-5 years": "Ages 3+. Use under adult supervision. Keep small parts away from under-threes.",
    "6-8 years": "Ages 6+. Not a food item. Supervise first use of lights and batteries.",
    "9-12 years": "Ages 9+. Remove tags and packaging before gifting. Batteries as labelled.",
    "13+ years": "Ages 13+ / teen desk toy. Small parts — not for young children.",
}

MATERIALS = {
    "bubble-blowers": "ABS camera body, bubble solution bottles, wrist strap.",
    "christmas-surprise": "PVC figure, foil surprise bag.",
    "ear-buddy-plush": "Soft plush pile, polyester fill, embroidered face.",
    "party-flags": "Printed polyester flag with header tape and eyelets.",
    "party-spotlight": "Mixed party materials as shown — plush, PVC, or LED plastic.",
    "kids-hats": "Lightweight printed bucket-hat fabric.",
    "novelty-keyrings": "Soft PVC charm, metal ring, silicone strap.",
    "light-up-toys": "LED plastic, batteries as labelled.",
    "articulated-keyrings": "3D-printed jointed figure, gold-tone clip and ring.",
    "handheld-fans": "ABS housing, USB-charge fan motor, optional water tank.",
    "bottle-plush": "Plush pile, polyester fill.",
    "christmas-glow": "Resin/plastic lantern with LED snow scene.",
    "glitter-squeeze": "TPR glitter gel, sealed skin.",
    "glow-wands": "LED plastic wand, batteries as labelled.",
    "play-balls": "Inflatable PVC play ball.",
    "halloween-squishies": "Slow-rise PU foam.",
    "fidget-spinners": "Metal alloy spinner with centre bearing.",
}


def folder_key(name: str) -> str:
    n = name.lower().replace("£", "").replace("�", "")
    if n.startswith("all @"):
        return "cameras"
    if "brain" in n:
        return "brainrot"
    if "breathable" in n or "stich" in n:
        return "ears"
    if "england" in n:
        return "flags"
    if "good description" in n:
        return "spotlight"
    if n.startswith("hats"):
        return "hats"
    if n.startswith("kirings"):
        return "keyrings"
    if "spinner light" in n:
        return "glowsticks"
    if n.startswith("light up"):
        return "lightup"
    if "3d" in n and "key" in n:
        return "cats"
    if "fan" in n:
        return "fans"
    if n.startswith("plush"):
        return "bottles"
    if "promotion" in n:
        return "promo"
    if n.startswith("put "):
        return "put"
    if "0.75" in n or "75p" in n:
        return "balls"
    if "1.50" in n:
        return "halloween"
    if "1.25" in n or n.startswith("15 "):
        return "spinners"
    return "unknown"


def images_in(folder: Path) -> list[Path]:
    return sorted(
        [p for p in folder.iterdir() if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}],
        key=lambda p: p.name.lower(),
    )


def polish(im: Image.Image) -> Image.Image:
    im = ImageOps.exif_transpose(im).convert("RGB")
    im = ImageEnhance.Contrast(im).enhance(1.07)
    im = ImageEnhance.Color(im).enhance(1.05)
    im = ImageEnhance.Sharpness(im).enhance(1.18)
    return im


def studio_bg(rgb: np.ndarray) -> tuple[int, int, int]:
    border = np.concatenate(
        [
            rgb[:12, :, :].reshape(-1, 3),
            rgb[-12:, :, :].reshape(-1, 3),
            rgb[:, :12, :].reshape(-1, 3),
            rgb[:, -12:, :].reshape(-1, 3),
        ]
    )
    return tuple(int(v) for v in np.median(border, axis=0))


def content_box(rgb: np.ndarray) -> tuple[int, int, int, int]:
    h, w = rgb.shape[:2]
    bg = np.array(studio_bg(rgb), dtype=np.float32)
    dist = np.linalg.norm(rgb.astype(np.float32) - bg, axis=2)
    mask = dist > max(16.0, float(np.percentile(dist, 48)) * 0.42)
    if mask.mean() > 0.92:
        mask = dist > float(np.percentile(dist, 36))
    if mask.mean() < 0.02:
        return 0, 0, w - 1, h - 1
    ys, xs = np.where(mask)
    pad = int(0.045 * max(w, h))
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
    bg = studio_bg(np.asarray(crop))
    canvas_bg = WHITE
    max_side = int(CANVAS * INNER)
    crop.thumbnail((max_side, max_side), Image.Resampling.LANCZOS)
    if max(crop.size) < 520:
        scale = 520 / max(crop.size)
        crop = crop.resize((int(crop.width * scale), int(crop.height * scale)), Image.Resampling.LANCZOS)
        crop.thumbnail((max_side, max_side), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (CANVAS, CANVAS), canvas_bg)
    x = (CANVAS - crop.width) // 2
    y = (CANVAS - crop.height) // 2
    canvas.paste(crop, (x, y))
    dest.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(dest, format="JPEG", quality=92, optimize=True, subsampling=0)
    cat = CATEGORY_DIR / dest.name
    tile = canvas.copy()
    tile.thumbnail((720, 720), Image.Resampling.LANCZOS)
    # category tiles are written separately from a chosen hero slug


# folder_key, image_index, slug, name, price, age, brand, theme, short, category, features
ITEMS: list[tuple] = [
    ("cameras", 0, "chick-bubble-camera", "Chick Bubble Camera", 6.99, "3-5 years", "BubbleBurst", "Bubbles", "Yellow chick camera that blows bubbles from the orange lens.", "bubble-blowers", ["Chick face", "Bubble lens", "Boxed gift", "Ages 3+"]),
    ("cameras", 1, "frog-bubble-camera", "Frog Bubble Camera", 6.99, "3-5 years", "BubbleBurst", "Bubbles", "Green frog camera with a strap and two bottles of bubble mix.", "bubble-blowers", ["Frog face", "Shoulder strap", "Solution bottles", "Ages 3+"]),
    ("cameras", 2, "pink-octopus-bubble-blower", "Pink Octopus Bubble Blower", 6.99, "3-5 years", "BubbleBurst", "Bubbles", "Pink octopus blower with a spinning fan and a carry handle.", "bubble-blowers", ["Octopus body", "Fan blower", "Carry handle", "Ages 3+"]),
    ("cameras", 3, "animal-bubble-camera-set", "Animal Bubble Camera Set", 6.99, "3-5 years", "BubbleBurst", "Bubbles", "Chick, frog, panda, and bunny cameras in matching Bubble Toys boxes.", "bubble-blowers", ["Four animal faces", "Window boxes", "One style per box", "Ages 3+"]),
    ("cameras", 5, "panda-bubble-camera", "Panda Bubble Camera", 6.99, "3-5 years", "BubbleBurst", "Bubbles", "Cream panda camera with black ears and a dark bubble lens.", "bubble-blowers", ["Panda face", "Window box", "Bubble lens", "Ages 3+"]),
    ("cameras", 6, "bunny-bubble-camera", "Bunny Bubble Camera", 6.99, "3-5 years", "BubbleBurst", "Bubbles", "White bunny camera with a pink nose and matching bubble lens.", "bubble-blowers", ["Bunny ears", "Pink lens", "Window box", "Ages 3+"]),
    ("cameras", 7, "green-octopus-bubble-blower", "Green Octopus Bubble Blower", 6.99, "3-5 years", "BubbleBurst", "Bubbles", "Mint octopus blower with a yellow handle and a spinning bubble fan.", "bubble-blowers", ["Mint octopus", "Fan blower", "Handle grip", "Ages 3+"]),
    ("cameras", 8, "octopus-bubble-blower-pair", "Octopus Bubble Blower Pair", 6.99, "3-5 years", "BubbleBurst", "Bubbles", "Pink and green octopus blowers with bubble mix sachets on the side.", "bubble-blowers", ["Two colours", "Solution sachets", "Garden play", "Ages 3+"]),
    ("brainrot", 0, "christmas-surprise-figure-bag", "Christmas Surprise Figure Bag", 2.99, "6-8 years", "Stage Pop", "Surprise", "Red Christmas surprise bags with a row of festive mini figures in front.", "christmas-surprise", ["Blind bag", "Festive figures", "Display box", "Ages 6+"]),
    ("ears", 0, "glowing-ear-buddy-plush", "Glowing Ear Buddy Plush", 14.99, "3-5 years", "Nest & Wool", "Comfort", "Blue long-ear buddy with a warm glow in the tummy when you squeeze.", "ear-buddy-plush", ["Long ears", "Tummy glow", "Soft pile", "Ages 3+"]),
    ("ears", 1, "ear-buddy-plush-pair", "Blue & Pink Ear Buddy Plush", 14.99, "3-5 years", "Nest & Wool", "Comfort", "Matching blue and pink long-ear plushes sitting side by side.", "ear-buddy-plush", ["Blue and pink", "Hug size", "Embroidered faces", "Ages 3+"]),
    ("flags", 0, "st-george-england-flag", "St George England Flag", 4.99, "9-12 years", "Open Air", "Britain", "White flag with the red Cross of St George — the England pack from this tray.", "party-flags", ["England cross", "Header eyelets", "Outdoor display", "Polyester"]),
    ("flags", 1, "union-jack-flag", "Union Jack Flag", 4.99, "9-12 years", "Open Air", "Britain", "Full Union Jack in red, white, and blue with metal eyelets.", "party-flags", ["Union Jack", "Eyelets", "Garden or window", "Polyester"]),
    ("spotlight", 0, "pop-star-figure-pack", "Pop Star Figure Pack", 14.99, "9-12 years", "Stage Pop", "Collectibles", "Window box of pop-star mini figures in bright stage outfits.", "party-spotlight", ["Figure pack", "Window box", "Mix of looks", "Ages 9+"]),
    ("spotlight", 1, "world-cup-mini-figures", "World Cup Mini Figures", 14.99, "6-8 years", "Forge & Fun", "Sport", "Football World Cup board packed with kit-coloured mini players.", "party-spotlight", ["Football kits", "Collector board", "Desk display", "Ages 6+"]),
    ("spotlight", 4, "funky-frights-set", "Funky Frights Squeeze Set", 14.99, "6-8 years", "Squish Lane", "Halloween", "Neon ghosts, pumpkins, and a grave tray from the Funky Frights box.", "party-spotlight", ["Glow squeezes", "Halloween tray", "Mixed shapes", "Ages 6+"]),
    ("spotlight", 5, "jumbo-squishy-surprise-bag", "Jumbo Squishy Surprise Bag", 14.99, "6-8 years", "Squish Lane", "Sensory", "100+ style surprise bag — axolotls, bears, cubes, and glitter balls.", "party-spotlight", ["Surprise mix", "100+ styles", "Squeeze and stretch", "Ages 6+"]),
    ("spotlight", 7, "rainbow-pocket-figures", "Rainbow Pocket Figures", 14.99, "9-12 years", "Stage Pop", "Collectibles", "Rainbow wall of pocket vinyl figures in a shop display.", "party-spotlight", ["Blind-box style", "Rainbow row", "Desk collectible", "Ages 9+"]),
    ("spotlight", 10, "bunny-glow-wands", "Bunny Glow Wands", 14.99, "3-5 years", "Party Glow", "Lights", "Pink and blue bunny wands with spinning light heads.", "party-spotlight", ["Bunny heads", "LED spin", "Pink or blue", "Ages 3+"]),
    ("spotlight", 11, "neon-cowboy-hats", "Neon Cowboy Hats", 14.99, "9-12 years", "Party Glow", "Dress-up", "LED cowboy hats that outline the brim in party colours.", "party-spotlight", ["Light-up brim", "Party colours", "Dress-up", "Ages 9+"]),
    ("spotlight", 13, "trio-glow-spinner-wands", "Trio Glow Spinner Wands", 14.99, "3-5 years", "Party Glow", "Lights", "Blue, pink, and gold spinner wands with a glowing ring on top.", "party-spotlight", ["Three colours", "Spinning ring", "Music-ready", "Ages 3+"]),
    ("spotlight", 14, "toy-light-sabres", "Toy Light Sabres", 14.99, "6-8 years", "Party Glow", "Lights", "Five extendable glow sabres in a row — silver hilts, lit blades.", "party-spotlight", ["Extendable blade", "LED glow", "Play fight", "Ages 6+"]),
    ("spotlight", 15, "bunny-led-wands", "Bunny LED Wands", 14.99, "3-5 years", "Party Glow", "Lights", "Pink and tan bunny wands with a spinning colour wheel.", "party-spotlight", ["Bunny handle", "Colour wheel", "Party wand", "Ages 3+"]),
    ("spotlight", 18, "rainbow-cloud-flop-hat", "Rainbow Cloud Flop Hat", 14.99, "6-8 years", "Street Fun", "Dress-up", "Blue-and-pink cloud hat with long flop ears that hang down.", "party-spotlight", ["Flop ears", "Rainbow plush", "One size kids", "Ages 6+"]),
    ("spotlight", 20, "snowman-flop-hat", "Snowman Flop Hat", 14.99, "6-8 years", "Street Fun", "Dress-up", "Snowman hat with a red Santa hat on top and long white arms.", "party-spotlight", ["Festive snowman", "Flop arms", "Photo hat", "Ages 6+"]),
    ("spotlight", 21, "pumpkin-flop-hat", "Pumpkin Flop Hat", 14.99, "6-8 years", "Street Fun", "Halloween", "Orange pumpkin hat with a carved face and long white flop arms.", "party-spotlight", ["Halloween pumpkin", "Flop arms", "Soft plush", "Ages 6+"]),
    ("spotlight", 22, "rainbow-cat-flop-hat", "Rainbow Cat Flop Hat", 14.99, "6-8 years", "Street Fun", "Dress-up", "Pastel cat hat with a rainbow face and hanging ear-arms.", "party-spotlight", ["Rainbow cat", "Flop ears", "Soft pile", "Ages 6+"]),
    ("spotlight", 23, "blue-speed-flop-hat", "Blue Speed Flop Hat", 14.99, "6-8 years", "Street Fun", "Dress-up", "Blue hedgehog-style hat with long flop ears for photos.", "party-spotlight", ["Speed-blue plush", "Flop ears", "Dress-up", "Ages 6+"]),
    ("spotlight", 24, "dark-bow-flop-hat", "Dark Bow Flop Hat", 14.99, "6-8 years", "Street Fun", "Dress-up", "Black hat with a skull bow and long hanging ears.", "party-spotlight", ["Dark bow", "Flop ears", "Photo hat", "Ages 6+"]),
    ("spotlight", 25, "yellow-goggle-flop-hat", "Yellow Goggle Flop Hat", 14.99, "6-8 years", "Street Fun", "Dress-up", "Yellow minion-style hat with goggles and long flop arms.", "party-spotlight", ["Goggle face", "Yellow plush", "Flop arms", "Ages 6+"]),
    ("spotlight", 26, "night-dragon-flop-hat", "Night Dragon Flop Hat", 14.99, "6-8 years", "Street Fun", "Dress-up", "Black dragon hat with glowing-style eyes and long flop wings.", "party-spotlight", ["Dragon face", "Flop wings", "Soft plush", "Ages 6+"]),
    ("spotlight", 27, "dark-hero-mask", "Dark Hero Mask", 14.99, "9-12 years", "Forge & Fun", "Dress-up", "Black-and-red hero mask still in its bag — party dress-up.", "party-spotlight", ["Full face mask", "Party dress-up", "Bagged", "Ages 9+"]),
    ("spotlight", 28, "web-hero-mask", "Web Hero Mask", 14.99, "9-12 years", "Forge & Fun", "Dress-up", "Red web-pattern hero mask for pretend missions.", "party-spotlight", ["Web print", "Full face", "Dress-up", "Ages 9+"]),
    ("spotlight", 29, "gold-armor-mask", "Gold Armor Mask", 14.99, "9-12 years", "Forge & Fun", "Dress-up", "Gold armour-face mask with a glowing-style eye slit.", "party-spotlight", ["Gold armour look", "Party mask", "Bagged", "Ages 9+"]),
    ("spotlight", 30, "bow-kitty-flop-hat", "Bow Kitty Flop Hat", 14.99, "6-8 years", "Street Fun", "Dress-up", "White kitty hat with a bow and long flop ears.", "party-spotlight", ["Bow kitty", "Flop ears", "Soft pile", "Ages 6+"]),
    ("spotlight", 31, "bow-kitty-plush-wand", "Bow Kitty Plush Wand", 14.99, "3-5 years", "Party Glow", "Lights", "Plush kitty wand with flop ears — a light-stick for parties.", "party-spotlight", ["Plush wand", "Kitty head", "Party stick", "Ages 3+"]),
    ("spotlight", 32, "cloud-pup-plush-pair", "Cloud Pup Plush Pair", 14.99, "3-5 years", "Nest & Wool", "Comfort", "White and sky-blue cloud-pup plushes with stitched smiles.", "party-spotlight", ["Two pups", "Soft pile", "Hug size", "Ages 3+"]),
    ("spotlight", 33, "sleepy-unicorn-bag", "Sleepy Unicorn Plush Bag", 14.99, "6-8 years", "Nest & Wool", "Comfort", "Pink unicorn backpack-plush with a horn and sleepy eyes.", "party-spotlight", ["Unicorn bag", "Soft pile", "Wear or hug", "Ages 6+"]),
    ("spotlight", 34, "pink-idol-plush", "Pink Idol Plush", 14.99, "6-8 years", "Nest & Wool", "Comfort", "Pink idol-style plush still wrapped from the new delivery.", "party-spotlight", ["Pink plush", "Gift wrap on", "Hug size", "Ages 6+"]),
    ("spotlight", 35, "flop-ear-glow-headband", "Flop-Ear Glow Headband", 14.99, "6-8 years", "Party Glow", "Lights", "LED flop-ear headband worn from the back — ears hang and light up.", "party-spotlight", ["LED ears", "Headband", "Party photos", "Ages 6+"]),
    ("spotlight", 36, "neon-star-wand", "Neon Star Wand", 14.99, "3-5 years", "Party Glow", "Lights", "Rainbow LED star on a black handle — shown glowing in the dark.", "party-spotlight", ["Star outline", "Rainbow LED", "Night glow", "Ages 3+"]),
    ("spotlight", 38, "neon-unicorn-wand", "Neon Unicorn Wand", 14.99, "3-5 years", "Party Glow", "Lights", "Unicorn-head LED wand glowing pink, purple, and mint.", "party-spotlight", ["Unicorn outline", "Rainbow LED", "Night glow", "Ages 3+"]),
    ("spotlight", 39, "neon-heart-wand", "Neon Heart Wand", 14.99, "3-5 years", "Party Glow", "Lights", "Heart-outline LED wand with a candy-stripe handle.", "party-spotlight", ["Heart outline", "Rainbow LED", "Party wand", "Ages 3+"]),
    ("spotlight", 40, "neon-unicorn-wand-trio", "Neon Unicorn Wand Trio", 14.99, "3-5 years", "Party Glow", "Lights", "Pink, green, and blue unicorn wands lit against black.", "party-spotlight", ["Three colours", "Unicorn heads", "LED outline", "Ages 3+"]),
    ("spotlight", 41, "fibre-optic-party-wands", "Fibre-Optic Party Wands", 14.99, "3-5 years", "Party Glow", "Lights", "Star-tip fibre wands in white, pink, blue, and red.", "party-spotlight", ["Fibre tips", "Assorted colours", "Party bag", "Ages 3+"]),
    ("spotlight", 42, "spinner-character-wands", "Spinner Character Wands", 14.99, "3-5 years", "Party Glow", "Lights", "Pink, gold, and blue spinner wands with a character in the ring.", "party-spotlight", ["Spinning ring", "Three colours", "Music light", "Ages 3+"]),
    ("spotlight", 44, "kaleido-fan-wand", "Kaleido Fan Wand", 14.99, "6-8 years", "Party Glow", "Lights", "Round kaleidoscope fan wand with a spinning rainbow disc.", "party-spotlight", ["Spinning disc", "Rainbow LED", "Night glow", "Ages 6+"]),
    ("spotlight", 45, "bow-glow-wand", "Bow Glow Wand", 14.99, "3-5 years", "Party Glow", "Lights", "Bow-shaped LED wand glowing purple and blue.", "party-spotlight", ["Bow outline", "Rainbow LED", "Party wand", "Ages 3+"]),
    ("spotlight", 46, "club-glow-wand", "Club Glow Wand", 14.99, "3-5 years", "Party Glow", "Lights", "Club-head LED wand with a rainbow outline on a stripe stick.", "party-spotlight", ["Club outline", "Rainbow LED", "Night glow", "Ages 3+"]),
    ("spotlight", 47, "pine-tree-glow-wands", "Pine Tree Glow Wands", 14.99, "3-5 years", "Party Glow", "Lights", "Three pine-tree LED wands in blue, green, and white outlines.", "party-spotlight", ["Tree outline", "Three colours", "Festive glow", "Ages 3+"]),
    ("hats", 0, "candy-sports-bucket-hats", "Candy Sports Bucket Hats", 5.99, "9-12 years", "Street Fun", "Street", "Pink and mint bucket hats with an all-over sports word print.", "kids-hats", ["Pink and mint", "Bucket brim", "All-over print", "Kids size"]),
    ("hats", 1, "cool-sports-bucket-hats", "Cool Sports Bucket Hats", 5.99, "9-12 years", "Street Fun", "Street", "Blue, black-and-white, and stripe bucket hats from the same print family.", "kids-hats", ["Blue and mono", "Stripe option", "Bucket brim", "Kids size"]),
    ("hats", 2, "mixed-sports-bucket-hats", "Mixed Sports Bucket Hats", 5.99, "9-12 years", "Street Fun", "Street", "The full colour mix of sports-print bucket hats in one shot.", "kids-hats", ["Mixed colours", "Street print", "One style, many colours", "Kids size"]),
    ("hats", 3, "red-sports-bucket-hats", "Red Sports Bucket Hats", 5.99, "9-12 years", "Street Fun", "Street", "Red and light-pink sports-print bucket hats stacked together.", "kids-hats", ["Red and blush", "Bucket brim", "All-over print", "Kids size"]),
    ("keyrings", 0, "speed-crew-keyrings", "Speed Crew Keyrings", 2.99, "9-12 years", "Street Fun", "Keyrings", "Yellow, purple, and red speed-crew charms on Forever Sports straps.", "novelty-keyrings", ["Three crew charms", "Wrist straps", "Bag clip", "Ages 9+"]),
    ("keyrings", 1, "mini-sneaker-keyrings", "Mini Sneaker Keyrings", 2.99, "9-12 years", "Street Fun", "Keyrings", "Mini high-top charms in blue, purple, red, green, pink, and black.", "novelty-keyrings", ["Six colourways", "Mini sneaker", "Sports strap", "Ages 9+"]),
    ("keyrings", 3, "alien-crew-keyrings", "Alien Crew Keyrings", 2.99, "6-8 years", "Street Fun", "Keyrings", "Blue, mint, and red long-ear alien charms plus a heart charm.", "novelty-keyrings", ["Alien ears", "Heart extra", "Soft PVC", "Ages 6+"]),
    ("keyrings", 4, "cartoon-crew-keyrings", "Cartoon Crew Keyrings", 2.99, "6-8 years", "Street Fun", "Keyrings", "Cartoon animal charms on bright name straps — a mixed crew pack.", "novelty-keyrings", ["Mixed cartoons", "Name straps", "Bag clip", "Ages 6+"]),
    ("keyrings", 5, "hedgehog-duo-keyrings", "Hedgehog Duo Keyrings", 2.99, "9-12 years", "Street Fun", "Keyrings", "Blue hedgehog and dark rival charms on a speed strap.", "novelty-keyrings", ["Two charms", "Soft PVC", "Bag clip", "Ages 9+"]),
    ("keyrings", 6, "yellow-duo-keyrings", "Yellow Duo Keyrings", 2.99, "6-8 years", "Street Fun", "Keyrings", "Two yellow overalls charms on matching yellow straps.", "novelty-keyrings", ["Pair pack", "Soft PVC", "Bag clip", "Ages 6+"]),
    ("keyrings", 7, "hero-trio-keyrings", "Hero Trio Keyrings", 2.99, "9-12 years", "Street Fun", "Keyrings", "Red web hero, black rival, and extra hero charms on red straps.", "novelty-keyrings", ["Three heroes", "Soft PVC", "Bag clip", "Ages 9+"]),
    ("keyrings", 8, "coffee-bear-keyrings", "Coffee Bear Keyrings", 2.99, "9-12 years", "Street Fun", "Keyrings", "Bear and cup charms on green coffee-style straps.", "novelty-keyrings", ["Bear and cup", "Soft PVC", "Bag clip", "Ages 9+"]),
    ("lightup", 0, "mini-lit-christmas-trees", "Mini Lit Christmas Trees", 1.99, "6-8 years", "Nightfield", "Christmas", "Three table-top Christmas trees with warm lights and gifts at the base.", "light-up-toys", ["Warm LEDs", "Table size", "Gift scene", "Indoor"]),
    ("lightup", 1, "reindeer-snow-lanterns", "Reindeer Snow Lanterns", 1.99, "6-8 years", "Nightfield", "Christmas", "Pair of snow-globe lanterns with a deer scene inside.", "light-up-toys", ["Snow scene", "Pair", "Warm LED", "Indoor"]),
    ("lightup", 2, "led-snow-globe-lanterns", "LED Snow Globe Lanterns", 1.99, "6-8 years", "Nightfield", "Christmas", "White lantern snow globes in a counter display.", "light-up-toys", ["Counter display", "Warm LED", "Snow globe", "Indoor"]),
    ("lightup", 3, "glowing-snowman-set", "Glowing Snowman Set", 1.99, "6-8 years", "Nightfield", "Christmas", "Three white snowmen with warm lights in a boxed set.", "light-up-toys", ["Three snowmen", "Warm LED", "Window sill", "Indoor"]),
    ("lightup", 4, "christmas-booth-lanterns", "Christmas Booth Lanterns", 1.99, "6-8 years", "Nightfield", "Christmas", "Red and cream phone-booth lanterns with a Santa scene inside.", "light-up-toys", ["Booth shape", "Santa scene", "Warm LED", "Indoor"]),
    ("lightup", 5, "glowing-star-trees", "Glowing Star Trees", 1.99, "6-8 years", "Nightfield", "Christmas", "Two star-shaped lit trees in warm gold.", "light-up-toys", ["Star trees", "Warm LED", "Pair", "Indoor"]),
    ("lightup", 6, "white-village-trees", "White Village Trees", 1.99, "6-8 years", "Nightfield", "Christmas", "Tray of small white Christmas trees for a village display.", "light-up-toys", ["Village set", "White trees", "Warm LED", "Indoor"]),
    ("lightup", 7, "santa-house-lanterns", "Santa House Lanterns", 1.99, "6-8 years", "Nightfield", "Christmas", "White house lanterns with Santa and a tree in the window.", "light-up-toys", ["House lantern", "Santa window", "Warm LED", "Indoor"]),
    ("lightup", 8, "snow-scene-lanterns", "Snow Scene Lanterns", 1.99, "6-8 years", "Nightfield", "Christmas", "Clear lanterns with a tree and snow inside.", "light-up-toys", ["Clear globe", "Snow scene", "Warm LED", "Indoor"]),
    ("lightup", 9, "red-christmas-lanterns", "Red Christmas Lanterns", 1.99, "6-8 years", "Nightfield", "Christmas", "Classic red lanterns with a festive scene in the glass.", "light-up-toys", ["Red lantern", "Festive scene", "Warm LED", "Indoor"]),
    ("lightup", 10, "butterfly-light-wands", "Butterfly Light Wands", 1.99, "3-5 years", "Party Glow", "Lights", "Pink, green, and purple butterfly wands with glitter wings.", "light-up-toys", ["Butterfly top", "Three colours", "Party wand", "Ages 3+"]),
    ("lightup", 11, "gold-snow-lanterns", "Gold Snow Lanterns", 1.99, "6-8 years", "Nightfield", "Christmas", "Antique-gold lanterns with a lit snow village inside.", "light-up-toys", ["Gold finish", "Snow village", "Warm LED", "Indoor"]),
    ("lightup", 12, "hanging-snow-lantern", "Hanging Snow Lantern", 1.99, "6-8 years", "Nightfield", "Christmas", "Gold hanging lantern with a boxed snow scene.", "light-up-toys", ["Hanging loop", "Snow scene", "Gift box", "Indoor"]),
    ("lightup", 15, "character-3d-night-light", "Character 3D Night Light", 1.99, "6-8 years", "Nightfield", "Lights", "Acrylic character lamp that changes colour on a black base.", "light-up-toys", ["Colour change", "Acrylic plate", "Remote-ready", "Ages 6+"]),
    ("lightup", 16, "lace-heart-wands", "Lace Heart Wands", 1.99, "3-5 years", "Party Glow", "Lights", "Blue, hot-pink, blush, and lilac heart wands with lace and ribbon.", "light-up-toys", ["Heart top", "Lace trim", "Four colours", "Ages 3+"]),
    ("lightup", 18, "star-princess-wands", "Star Princess Wands", 1.99, "3-5 years", "Party Glow", "Lights", "Pink, blue, and purple star wands with a glitter fill.", "light-up-toys", ["Star top", "Three colours", "Princess play", "Ages 3+"]),
    ("lightup", 19, "fibre-unicorn-wands", "Fibre Unicorn Wands", 1.99, "3-5 years", "Party Glow", "Lights", "White fibre wands with unicorn, heart, and star handles.", "light-up-toys", ["Fibre glow", "Character handles", "Party wand", "Ages 3+"]),
    ("lightup", 20, "lollipop-light-wands", "Lollipop Light Wands", 1.99, "3-5 years", "Party Glow", "Lights", "Swirl lollipop wands in pink, yellow, and mint.", "light-up-toys", ["Lollipop top", "Three colours", "LED swirl", "Ages 3+"]),
    ("cats", 1, "rainbow-sphynx-keyring-set", "Rainbow Sphynx Keyring Set", 4.99, "13+ years", "Street Fun", "Keyrings", "Jointed rainbow sphynx cats on gold clips — pink, mint, and sunset.", "articulated-keyrings", ["3D jointed", "Rainbow colours", "Gold clip", "Desk fidget"]),
    ("cats", 3, "sphynx-keyring-duo", "Sphynx Keyring Duo", 4.99, "13+ years", "Street Fun", "Keyrings", "Mint-lilac and sunset sphynx cats on a dark tray.", "articulated-keyrings", ["Two colours", "Poseable joints", "Gold clip", "Bag charm"]),
    ("cats", 5, "sunset-sphynx-keyring", "Sunset Sphynx Keyring", 4.99, "13+ years", "Street Fun", "Keyrings", "Pink-to-orange jointed sphynx cat with a gold ring.", "articulated-keyrings", ["Sunset fade", "Poseable", "Gold ring", "Bag charm"]),
    ("cats", 7, "teal-jointed-lizard", "Teal Jointed Lizard", 4.99, "13+ years", "Street Fun", "Keyrings", "Teal-and-lime 3D jointed lizard from the same 3D tray.", "articulated-keyrings", ["Jointed lizard", "Teal print", "Poseable", "Desk fidget"]),
    ("fans", 0, "navy-pocket-fan", "Navy Pocket Fan", 6.99, "9-12 years", "Cool Breeze", "Gadgets", "Navy Coolfor pocket fan standing beside its box.", "handheld-fans", ["USB charge", "Pocket size", "Stand base", "Ages 9+"]),
    ("fans", 1, "lilac-pocket-fan", "Lilac Pocket Fan", 6.99, "9-12 years", "Cool Breeze", "Gadgets", "Lilac handheld fan with a folding handle and matching box.", "handheld-fans", ["Fold handle", "USB charge", "Lilac", "Ages 9+"]),
    ("fans", 2, "mint-table-fan", "Mint Table Fan", 6.99, "9-12 years", "Cool Breeze", "Gadgets", "Square mint desk fan with a round grille.", "handheld-fans", ["Desk stand", "Quiet grille", "Mint", "Ages 9+"]),
    ("fans", 4, "mint-handle-fan", "Mint Handle Fan", 6.99, "9-12 years", "Cool Breeze", "Gadgets", "Green handheld fan next to a purple handle fan and box.", "handheld-fans", ["Handle grip", "USB charge", "Two colours shown", "Ages 9+"]),
    ("fans", 5, "sage-table-fan", "Sage Table Fan", 6.99, "9-12 years", "Cool Breeze", "Gadgets", "Sage square table fan beside its illustrated box.", "handheld-fans", ["Table fan", "Sage colour", "Desk use", "Ages 9+"]),
    ("fans", 6, "chrome-spray-fan", "Chrome Spray Fan", 11.99, "9-12 years", "Cool Breeze", "Gadgets", "Silver icy-fan spray mister with a water window in the handle.", "handheld-fans", ["Mist spray", "Chrome body", "Ages 8+", "USB charge"]),
    ("fans", 7, "purple-spray-fan", "Purple Spray Fan", 11.99, "9-12 years", "Cool Breeze", "Gadgets", "Purple handheld spray fan next to the Hand-held Spray Fan box.", "handheld-fans", ["Mist spray", "Purple", "Ages 8+", "USB charge"]),
    ("bottles", 0, "sports-bottle-plush-set", "Sports Bottle Plush Set", 2.49, "3-5 years", "Nest & Wool", "Comfort", "Five bottle-shaped plushes in pink, red-white-blue, white, lime, and purple.", "bottle-plush", ["Five colours", "Bottle shape", "Soft pile", "Ages 3+"]),
    ("promo", 0, "santa-snow-train", "Santa Snow Train", 3.99, "6-8 years", "Nightfield", "Christmas", "Bronze locomotive with Santa decorating a tree in a lit snow carriage.", "christmas-glow", ["Snow carriage", "Warm LED", "Shelf decor", "Indoor"]),
    ("promo", 1, "santa-glow-lantern-pair", "Santa Glow Lantern Pair", 3.99, "6-8 years", "Nightfield", "Christmas", "Two black lanterns with Santa and a tree glowing inside.", "christmas-glow", ["Pair of lanterns", "Santa scene", "Warm LED", "Indoor"]),
    ("put", 0, "glitter-unicorn-squeeze-box", "Glitter Unicorn Squeeze Box", 4.99, "3-5 years", "Squish Lane", "Sensory", "Counter box of glitter unicorn and critter squeezes.", "glitter-squeeze", ["Glitter gel", "Unicorn mix", "Display box", "Ages 3+"]),
    ("put", 2, "gummy-bear-squeeze-box", "Gummy Bear Squeeze Box", 4.99, "3-5 years", "Squish Lane", "Sensory", "Rainbow gummy-bear squeezes standing in their counter tray.", "glitter-squeeze", ["Gummy bears", "Glitter fill", "Counter tray", "Ages 3+"]),
    ("put", 3, "glitter-unicorn-trio", "Glitter Unicorn Trio", 4.99, "3-5 years", "Squish Lane", "Sensory", "Yellow, mint, and lilac glitter unicorns from the squeeze tray.", "glitter-squeeze", ["Three unicorns", "Glitter gel", "Slow squish", "Ages 3+"]),
    ("put", 4, "happy-duck-squeeze", "Happy Duck Squeeze", 4.99, "3-5 years", "Squish Lane", "Sensory", "Purple, teal, and orange glitter ducks from the Happy Ducks box.", "glitter-squeeze", ["Duck shapes", "Glitter gel", "Three colours", "Ages 3+"]),
    ("put", 5, "squeeze-hair-brushes", "Squeeze Hair Brushes", 4.99, "6-8 years", "Squish Lane", "Sensory", "Glitter hairbrush squeezes in a Sugar Balls tray.", "glitter-squeeze", ["Brush shape", "Glitter gel", "Desk fidget", "Ages 6+"]),
    ("put", 6, "glitter-critter-squeeze", "Glitter Critter Squeeze", 4.99, "3-5 years", "Squish Lane", "Sensory", "Blue, green, and pink glitter critters from the Squeeze Toys box.", "glitter-squeeze", ["Cute critters", "Glitter gel", "Display box", "Ages 3+"]),
    ("put", 8, "ear-buddy-squeeze-box", "Ear Buddy Squeeze Box", 4.99, "3-5 years", "Squish Lane", "Sensory", "Blue and pink long-ear glitter squeezes in a counter box.", "glitter-squeeze", ["Long ears", "Glitter gel", "Four in view", "Ages 3+"]),
    ("put", 9, "stretching-puppy-squeeze", "Stretching Puppy Squeeze", 4.99, "3-5 years", "Squish Lane", "Sensory", "Glitter stretching puppies in the farm-tray box.", "glitter-squeeze", ["Puppy stretch", "Glitter gel", "Display box", "Ages 3+"]),
    ("put", 10, "glitter-blob-squeeze", "Glitter Blob Squeeze", 4.99, "6-8 years", "Squish Lane", "Sensory", "Green, pink, and purple glitter blobs in the black counter tray.", "glitter-squeeze", ["Blob fidget", "Glitter gel", "Desk size", "Ages 6+"]),
    ("put", 11, "crystal-fruit-squeeze", "Crystal Fruit Squeeze", 4.99, "3-5 years", "Squish Lane", "Sensory", "Pear, orange, and apple glitter fruits standing in a row.", "glitter-squeeze", ["Fruit shapes", "Crystal glitter", "Three colours", "Ages 3+"]),
    ("put", 14, "cube-squeeze-balls", "Cube Squeeze Balls", 4.99, "6-8 years", "Squish Lane", "Sensory", "Blue, pink, green, and yellow glitter squeeze balls.", "glitter-squeeze", ["Ball fidget", "Four colours", "Glitter gel", "Ages 6+"]),
    ("put", 18, "mini-glitter-dinos", "Mini Glitter Dinos", 4.99, "3-5 years", "Squish Lane", "Sensory", "Tiny glitter dinosaurs in orange, purple, pink, and mint.", "glitter-squeeze", ["Mini dinos", "Four colours", "Glitter gel", "Ages 3+"]),
    ("put", 19, "cloud-pup-squeeze", "Cloud Pup Squeeze", 4.99, "3-5 years", "Squish Lane", "Sensory", "Cloud-pup and pal squeezes in pastel glitter from the counter box.", "glitter-squeeze", ["Cloud pups", "Pastel glitter", "Display box", "Ages 3+"]),
    ("put", 20, "crystal-unicorn-squeeze", "Crystal Unicorn Squeeze", 4.99, "3-5 years", "Squish Lane", "Sensory", "Clear pink glitter unicorn shown close so the sparkle is obvious.", "glitter-squeeze", ["Unicorn", "Crystal glitter", "Studio shot", "Ages 3+"]),
    ("put", 21, "glitter-axolotl-squeeze", "Glitter Axolotl Squeeze", 4.99, "3-5 years", "Squish Lane", "Sensory", "Sky-blue glitter axolotl with a smile and sparkly tail.", "glitter-squeeze", ["Axolotl", "Sky glitter", "Studio shot", "Ages 3+"]),
    ("put", 24, "grape-cluster-squeeze", "Grape Cluster Squeeze", 4.99, "3-5 years", "Squish Lane", "Sensory", "Long glitter grape clusters in a green farm-style box.", "glitter-squeeze", ["Grape cluster", "Glitter gel", "Display box", "Ages 3+"]),
    ("put", 25, "crystal-critter-set", "Crystal Critter Set", 4.99, "3-5 years", "Squish Lane", "Sensory", "Tiny clear glitter animals on a white card — unicorns and pals.", "glitter-squeeze", ["Mini set", "Crystal glitter", "Gift card", "Ages 3+"]),
    ("glowsticks", 0, "character-glow-wands", "Character Glow Wands", 6.99, "3-5 years", "Party Glow", "Lights", "Kuromi-style crew of character wands in pink, red, blue, and purple.", "glow-wands", ["Character tops", "LED glow", "Party pack look", "Ages 3+"]),
    ("glowsticks", 1, "princess-electric-glow-stick", "Princess Electric Glow Stick", 6.99, "3-5 years", "Party Glow", "Lights", "Blue or pink electric glow stick with a spinning rainbow ring and a princess in the centre.", "glow-wands", ["36 cm wand", "Lights and music", "Pink or blue", "Ages 3+"]),
    ("glowsticks", 4, "rainbow-heart-glow-sticks", "Rainbow Heart Glow Sticks", 6.99, "3-5 years", "Party Glow", "Lights", "Bunch of heart fibre sticks glowing pink, green, blue, and gold.", "glow-wands", ["Heart tops", "Fibre glow", "Party bunch", "Ages 3+"]),
    ("balls", 0, "character-play-balls", "Character Play Balls", 2.49, "3-5 years", "Open Air", "Outdoor", "Yellow, green, pink, blue, and red inflatable balls with cartoon faces.", "play-balls", ["Five colours", "Face print", "Inflatable", "Garden play"]),
    ("halloween", 0, "halloween-butter-squishy", "Halloween Butter Squishy", 4.5, "6-8 years", "Squish Lane", "Halloween", "Slow-rise butter brick in Halloween wrap — pumpkins, bats, and trick-or-treat.", "halloween-squishies", ["Slow rise", "Halloween wrap", "Butter brick", "Ages 6+"]),
    ("spinners", 0, "hero-fidget-spinner-range", "Hero Fidget Spinner Range", 3.99, "13+ years", "Street Fun", "Gadgets", "Shield, web, armour, and lightning spinner faces in metal colours.", "fidget-spinners", ["Metal spinner", "Hero faces", "Assorted colours", "Desk fidget"]),
]

HERO_SLUG = {
    "bubble-blowers": "animal-bubble-camera-set",
    "christmas-surprise": "christmas-surprise-figure-bag",
    "ear-buddy-plush": "ear-buddy-plush-pair",
    "party-flags": "union-jack-flag",
    "party-spotlight": "rainbow-cloud-flop-hat",
    "kids-hats": "candy-sports-bucket-hats",
    "novelty-keyrings": "mini-sneaker-keyrings",
    "light-up-toys": "lace-heart-wands",
    "articulated-keyrings": "rainbow-sphynx-keyring-set",
    "handheld-fans": "chrome-spray-fan",
    "bottle-plush": "sports-bottle-plush-set",
    "christmas-glow": "santa-snow-train",
    "glitter-squeeze": "crystal-unicorn-squeeze",
    "glow-wands": "princess-electric-glow-stick",
    "play-balls": "character-play-balls",
    "halloween-squishies": "halloween-butter-squishy",
    "fidget-spinners": "hero-fidget-spinner-range",
}


def ts_escape(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def emit_product(item: dict, index: int) -> str:
    stock = 18 + (index * 7) % 40
    features = ", ".join(ts_escape(f) for f in item["features"])
    desc = (
        f"{item['short']} Photographed from the new delivery, centred in a square frame "
        f"so the toy is easy to recognise on every screen."
    )
    extra = "\n    isNew: true,"
    if index % 7 == 0:
        extra += "\n    isBestSeller: true,"
    return f"""  {{
    slug: {ts_escape(item['slug'])},
    name: {ts_escape(item['name'])},
    price: {item['price']},
    ageRange: {ts_escape(item['age'])},
    brand: {ts_escape(item['brand'])},
    theme: {ts_escape(item['theme'])},
    categorySlug: {ts_escape(item['cat'])},
    images: [],
    shortDescription: {ts_escape(item['short'])},
    description: {ts_escape(desc)},
    features: [{features}],
    safety: {ts_escape(SAFETY[item['age']])},
    materials: {ts_escape(MATERIALS[item['cat']])},{extra}
    stock: {stock},
  }}"""


def main() -> None:
    folders: dict[str, Path] = {}
    for folder in SRC.iterdir():
        if folder.is_dir():
            folders[folder_key(folder.name)] = folder
    print("folders", {k: v.name for k, v in folders.items()})

    PRODUCT_DIR.mkdir(parents=True, exist_ok=True)
    CATEGORY_DIR.mkdir(parents=True, exist_ok=True)

    records = []
    for i, row in enumerate(ITEMS):
        key, idx, slug, name, price, age, brand, theme, short, cat, features = row
        folder = folders.get(key)
        if not folder:
            print("MISSING FOLDER", key)
            continue
        files = images_in(folder)
        if idx >= len(files):
            print("MISSING INDEX", key, idx, "have", len(files))
            continue
        src = files[idx]
        dest = PRODUCT_DIR / f"{slug}.jpg"
        frame_hd(src, dest)
        print(f"{slug}: {src.name} -> {dest.stat().st_size // 1024}kb")
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
                "features": features,
            }
        )

    for cat, slug in HERO_SLUG.items():
        src = PRODUCT_DIR / f"{slug}.jpg"
        if src.exists():
            im = Image.open(src).convert("RGB")
            im.save(CATEGORY_DIR / f"{cat}.jpg", format="JPEG", quality=90, optimize=True)
            print("category tile", cat)

    body = ",\n".join(emit_product(item, i) for i, item in enumerate(records))
    OUT_TS.write_text(
        'import type { Product } from "@/lib/types";\n\n'
        "export const newStock: Product[] = [\n"
        f"{body}\n"
        "];\n",
        encoding="utf-8",
    )
    print("wrote", OUT_TS, "products", len(records))


if __name__ == "__main__":
    main()
