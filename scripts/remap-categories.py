#!/usr/bin/env python3
"""Remap misplaced products into clearer aisles and refresh category tiles."""
from __future__ import annotations

import re
import shutil
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]

# Clear visitor-facing remaps: slug -> better category
REMAPS: dict[str, str] = {
    # Plush misplaced under party
    "cloud-pup-plush-pair": "dolls-plush",
    "pink-idol-plush": "dolls-plush",
    "bow-kitty-plush-wand": "glow-wands",
    # Fans / hats / bubbles
    "pocket-breeze-fan": "handheld-fans",
    "sequin-cowboy-hat": "party-spotlight",
    "fairy-light-bubble-wand": "bubble-blowers",
    "kaleido-fan-wand": "glow-wands",
    # Squish / fidget / glow
    "ra-579-31-unicorn-squishy": "glitter-squeeze",
    "ra-103-2key-spinner": "fidget-spinners",
    "ra-116-4key-spinner": "fidget-spinners",
    "ra-117-bun-spinner": "fidget-spinners",
    "jumbo-squishy-surprise-bag": "glitter-squeeze",
    "trio-glow-spinner-wands": "glow-wands",
    "spinner-character-wands": "glow-wands",
    # Christmas glow decor
    "mini-lit-christmas-trees": "christmas-glow",
    "christmas-booth-lanterns": "christmas-glow",
    "red-christmas-lanterns": "christmas-glow",
    # Bag charm → bags aisle
    "fluffy-monster-bag-charm": "monster-buddy-bags",
    # Bubble toys belong with bubble aisle
    "funtasy-bubble-gun": "bubble-blowers",
    "rocket-48-bubble-machine": "bubble-blowers",
    "bubble-bazooka-32": "bubble-blowers",
    # Food / butter "blocks" were miscategorised as building sets
    "ra2895-7-butter-blocks": "sensory-jars",
    "ra2895-8-ugly-orange-blocks": "food-squishies",
    "ra2895-9-potato-blocks": "food-squishies",
    "ra2895-10-corn-blocks": "food-squishies",
    "ra2895-11-pineapple-bun-blocks": "food-squishies",
    "ra2895-12-peanut-blocks": "food-squishies",
    "ra2895-13-7cm-cheese-blocks": "cheese-squishies",
    "ra2895-14-instant-noodle-blocks": "food-squishies",
    "ra2895-15-5cm-cheese-blocks": "cheese-squishies",
    "ra2895-16-cloud-blocks": "sensory-jars",
    "ra-128-egg-blocks": "food-squishies",
    "ram-1003-bear-blocks": "food-squishies",
    "ram-1004-fruit-expression": "fruit-squishies",
    "ram-1005-cheese-expression": "cheese-squishies",
    # Soft jelly character → food squish family (keep clear of outdoor)
    "ra-579-61-jelly-octopus": "food-squishies",
    # Construction / sensory tidying
    "engineering-dump-truck": "building-sets",
    "butter-block-squishy": "sensory-jars",
    "cheddar-block-squishy": "cheese-squishies",
    "dumpling-pop-spinner": "fidget-spinners",
    "rainbow-butter-squishy": "sensory-jars",
}

# Catch-all aisle for mixed novelty / hard-to-shelf gadgets
OTHERS_SLUGS: list[str] = [
    "racers-camera-car",
    "colorful-gear-sport-car",
    "crystal-mood-lamp",
    "rc-tank-truck",
    "brave-geeker-crawler",
]

# Preferred cover product per category (must belong after remaps)
COVERS: dict[str, str] = {
    "dolls-plush": "snuggle-puppy-plush",
    "ear-buddy-plush": "ear-buddy-plush-pair",
    "bubble-blowers": "animal-bubble-camera-set",
    "role-play": "dream-castle-playset",
    "outdoor-sports": "rocket-48-bubble-machine",
    "handheld-fans": "navy-pocket-fan",
    "glow-wands": "trio-glow-spinner-wands",
    "glitter-squeeze": "jumbo-squishy-surprise-bag",
    "fidget-spinners": "ra-103-2key-spinner",
    "christmas-glow": "mini-lit-christmas-trees",
    "monster-buddy-bags": "fluffy-monster-bag-charm",
    "party-spotlight": "rainbow-cloud-flop-hat",
    "fruit-squishies": "jumbo-peach-squishy",
    "food-squishies": "jelly-gummy-bear",
    "sensory-jars": "rainbow-butter-squishy",
    "building-sets": "dino-expedition-build",
    "action-figures": "hero-league-figure",
    "baby-toddler": "wrap-around-plush-monkey",
    "games-gadgets": "rc-monster-truck",
    "arts-crafts": "giant-strawberry-squishy",
    "others": "racers-camera-car",
    "cheese-squishies": "ra2895-13-7cm-cheese-blocks",
    "outdoor-sports": "ride-on-4x4-jeep",
}

# Product image replacements so landing tiles match category peers
IMAGE_SWAPS: dict[str, str] = {
    # Keep dolls aisle looking like dolls/plush (not random party shots)
    "fashion-girl-twin-gowns": "pink-idol-plush",
    "realistic-baby-care-doll": "snuggle-puppy-plush",
    "kitchen-cook-set": "mermaid-dress-up-set",
    "funtasy-bubble-gun": "animal-bubble-camera-set",
}

def remap_category_slugs() -> int:
    data_dir = ROOT / "lib" / "data"
    all_maps = {**REMAPS, **{slug: "others" for slug in OTHERS_SLUGS}}
    changed = 0
    for path in data_dir.glob("*.ts"):
        text = path.read_text(encoding="utf-8")
        original = text
        for slug, new_cat in all_maps.items():
            # Replace categorySlug only inside the product block that starts with this slug
            pattern = (
                rf'(slug:\s*"{re.escape(slug)}"[\s\S]*?categorySlug:\s*")[^"]+(")'
            )
            text, n = re.subn(pattern, rf"\g<1>{new_cat}\g<2>", text, count=1)
            changed += n
        if text != original:
            path.write_text(text, encoding="utf-8")
            print(f"updated {path.name}")
    return changed


def save_cover(src_product: str, dest_rel: str) -> bool:
    src = ROOT / "public" / "images" / "products" / f"{src_product}.jpg"
    dest = ROOT / "public" / dest_rel.lstrip("/")
    if not src.exists():
        print(f"  skip cover missing product {src_product}")
        return False
    dest.parent.mkdir(parents=True, exist_ok=True)
    im = Image.open(src).convert("RGB")
    im.thumbnail((1000, 1000), Image.Resampling.LANCZOS)
    # pad to square white
    size = max(im.size)
    canvas = Image.new("RGB", (size, size), (255, 255, 255))
    canvas.paste(im, ((size - im.size[0]) // 2, (size - im.size[1]) // 2))
    canvas.save(dest, "JPEG", quality=82, optimize=True, progressive=True)
    print(f"  cover {dest.name} <- {src_product}")
    return True


def refresh_covers() -> None:
    for cat, slug in COVERS.items():
        save_cover(slug, f"images/categories/{cat}.jpg")


def swap_product_images() -> None:
    prod = ROOT / "public" / "images" / "products"
    for dest_slug, src_slug in IMAGE_SWAPS.items():
        src = prod / f"{src_slug}.jpg"
        dest = prod / f"{dest_slug}.jpg"
        if not src.exists():
            print(f"  skip image swap missing {src_slug}")
            continue
        im = Image.open(src).convert("RGB")
        im.thumbnail((1000, 1000), Image.Resampling.LANCZOS)
        size = max(im.size)
        canvas = Image.new("RGB", (size, size), (255, 255, 255))
        canvas.paste(im, ((size - im.size[0]) // 2, (size - im.size[1]) // 2))
        canvas.save(dest, "JPEG", quality=84, optimize=True, progressive=True)
        print(f"  image {dest_slug} <- {src_slug}")


def main() -> None:
    n = remap_category_slugs()
    print(f"remapped {n} products")
    swap_product_images()
    refresh_covers()
    print("done")


if __name__ == "__main__":
    main()
