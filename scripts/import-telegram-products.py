"""Build lib/data/telegram-stock.ts from curated_v3.json toys (add == true only).

Never reads the perfumes key. Names are written to scripts/telegram_name_map.py
(a reviewed slug -> title dict). Categories for the existing catalogue are
written to lib/data/assigned-categories.ts.
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(r"C:\Users\Adeel\toybloom_work\curated_v3.json")
OUT = ROOT / "lib" / "data" / "telegram-stock.ts"
NAME_MAP_PATH = ROOT / "scripts" / "telegram_name_map.py"
ASSIGNED_PATH = ROOT / "lib" / "data" / "assigned-categories.ts"
COVERS_PATH = ROOT / "lib" / "data" / "category-covers.ts"
DATA = ROOT / "lib" / "data"
PUBLIC = ROOT / "public"

SKIP_SLUG_FILES = {
    "categories.ts",
    "brands.ts",
    "blog.ts",
    "faqs.ts",
    "ages.ts",
    "about.ts",
    "telegram-stock.ts",
    "assigned-categories.ts",
    "category-covers.ts",
}

STOCK_FILES = [
    "products.ts",
    "new-stock.ts",
    "advance-stock.ts",
    "extra-stock.ts",
    "china-stock.ts",
    "innovative-stock.ts",
    "october-new-stock.ts",
]

BLOCKED = ("perfume", "fragrance", "body spray", "air freshener", "eau de", "cologne")

SAFETY = (
    "Ages 3+. Adult supervision recommended. "
    "Not suitable for children under 36 months (small parts)."
)

# Hand fixes where the caption is too thin for a tidy title alone.
NAME_OVERRIDES = {
    "tg-sony-angles-2290": "Sonny Angels Figures",
    "tg-fidget-spinners-in-stich-bluye-spider-man-and-poke-1936": "Character Fidget Spinners (Stitch, Bluey, Spider-Man, Pokemon)",
    "tg-k-pop-med-surprise-box-2585": "K-Pop Medium Surprise Box",
    "tg-bigger-crocs-charms-pack-1828": "Bigger Crocs Charms (pack)",
    "tg-airplane-series-763": "Airplane Toy Series",
    "tg-labubu-in-rabbits-2094": "Labubu Rabbit Style",
    "tg-series-4-2159": "Series 4 Collectible Figures",
    "tg-series-5-2272": "Series 5 Collectible Figures",
    "tg-christmas-2512": "Christmas Assortment",
    "tg-wakuku-2311": "Wakuku Character Figures",
    "tg-baby-lovely-2630": "Baby Lovely Doll",
    "tg-baby-cry-2654": "Baby Cry Doll",
    "tg-be-happy-princess-with-2643": "Be Happy Princess Doll",
    "tg-light-up-in-trend-123": "Light-Up Trend Toys",
    "tg-cactus-smiley-206": "Cactus Smiley Toy",
    "tg-pets-home-2in1-565": "Pets Home 2-in-1 Playset",
    "tg-sugar-peanut-with-individual-packaging-3663": "Sugar Peanut Squishy",
    "tg-angel-with-unicorn-pegasus-972": "Angel Unicorn Pegasus Figure",
    "tg-fuggler-ball-2249": "Fuggler Ball",
    "tg-flashing-top-2626": "Flashing Light-Up Top",
    "tg-jeffy-mom-and-dad-1714": "Jeffy Mom and Dad Dolls",
    "tg-trends-accessories-for-phone-and-laptop-with-popul-633": "Character Phone and Laptop Accessories",
    "tg-stitch-bluey-pokemon-etc-997": "Stitch Bluey and Pokémon Plush Mix",
    "tg-labubu-new-range-2372": "Labubu Collectible",
    "tg-design-of-music-guns-977": "Music Toy Guns",
    "tg-barking-dogs-in-box-971": "Barking Dogs",
    "tg-beauty-fashion-set-642": "Beauty Fashion Playset",
    "tg-keyrings-876": "Character Keyrings",
    "tg-blankets-1308": "Character Blankets",
    "tg-blankets-1520": "Printed Blankets",
    "tg-bedding-1492": "Character Bedding",
}

SPELLING = [
    (r"\bsonny?\s+angles\b", "Sonny Angels"),
    (r"\bsony\s+angels\b", "Sonny Angels"),
    (r"\blububu\b", "Labubu"),
    (r"\bk\s*-?\s*pop\b", "K-Pop"),
    (r"\bkpop\b", "K-Pop"),
    (r"\btrynasours?\b", "Tyrannosaurus"),
    (r"\bdinasours?\b", "Dinosaur"),
    (r"\bhelloween\b", "Halloween"),
    (r"\bhaloween\b", "Halloween"),
    (r"\bharror\b", "Horror"),
    (r"\bbluye\b", "Bluey"),
    (r"\bcalenders?\b", "Calendar"),
    (r"\badvert\b", "Advent"),
    (r"\batich\b", "Stitch"),
    (r"\bstich\b", "Stitch"),
    (r"(?<!glow )(?<!glow-)\bstick\b", "Stitch"),
    (r"\bsumer\b", "Summer"),
    (r"\bairobus\b", "Airbus"),
    (r"\bfigurs\b", "Figures"),
    (r"\bfigur\b", "Figure"),
    (r"\bpokémon\b", "Pokémon"),
    (r"\bpokemon\b", "Pokémon"),
    (r"\bonce\b", "Ones"),
    (r"\bfull+\b", "Full"),
    (r"\bdesigns\s+off\b", "designs of"),
    (r"(\d+)\s*pics\b", r"\1pcs"),
    (r"(\d+)pics\b", r"\1pcs"),
    (r"(\d+)\s*pic\b", r"\1pcs"),
    (r"(\d+)pic\b", r"\1pcs"),
]

JUNK_PHRASES = [
    "available now",
    "back in stock",
    "in stock now",
    "in stock",
    "back to stock",
    "new style",
    "new range",
    "in offer",
    "for kids fun",
    "with popular and famous characters",
]

JUNK_WORDS = {
    "new",
    "all",
    "latest",
    "popular",
    "trendy",
    "trends",
    "just",
    "etc",
}

ACRONYMS = {
    "LED",
    "USB",
    "FIFA",
    "BMW",
    "RC",
    "XXL",
    "XL",
    "DIY",
    "TV",
    "HD",
    "UK",
    "USA",
    "3D",
    "4D",
    "2D",
    "PVC",
    "PP",
}
SMALL = {"a", "an", "the", "and", "or", "of", "for", "with", "in", "on", "to", "vs", "per"}
EMOJI_RE = re.compile(
    "["
    "\U0001F1E0-\U0001F1FF"
    "\U0001F300-\U0001FAFF"
    "\U00002600-\U000027BF"
    "\U0001F900-\U0001F9FF"
    "\uFE0F"
    "\u200D"
    "]+",
    flags=re.UNICODE,
)

SQUISHY_OLD = {
    "fruit-squishies",
    "food-squishies",
    "sensory-jars",
    "crunchy-squishies",
    "cheese-squishies",
    "glitter-squeeze",
    "halloween-squishies",
    "festive-dumplings",
}

OLD_FALLBACK = {
    "fruit-squishies": "squishies",
    "food-squishies": "squishies",
    "sensory-jars": "squishies",
    "crunchy-squishies": "squishies",
    "cheese-squishies": "squishies",
    "glitter-squeeze": "squishies",
    "halloween-squishies": "squishies",
    "festive-dumplings": "squishies",
    "dolls-plush": "plush-soft-toys",
    "ear-buddy-plush": "plush-soft-toys",
    "bottle-plush": "plush-soft-toys",
    "star-buddy-plush": "plush-soft-toys",
    "plush-soft-toys": "plush-soft-toys",
    "action-figures": "action-figures",
    "hatch-dragons": "action-figures",
    "games-gadgets": "cars-vehicles",
    "fidget-spinners": "fidget-spinners",
    "push-pop-games": "fidget-spinners",
    "light-up-toys": "light-up-toys",
    "glow-swords": "light-up-toys",
    "glow-wands": "light-up-toys",
    "light-up-hats": "light-up-toys",
    "light-up-glasses": "light-up-toys",
    "light-up-gloves": "light-up-toys",
    "christmas-glow": "seasonal",
    "novelty-keyrings": "novelty-keyrings",
    "articulated-keyrings": "novelty-keyrings",
    "monster-buddy-keyrings": "novelty-keyrings",
    "metal-keyrings": "novelty-keyrings",
    "pocket-critter-keyrings": "novelty-keyrings",
    "bubble-blowers": "bubble-blowers",
    "outdoor-sports": "outdoor-sports",
    "play-balls": "outdoor-sports",
    "building-sets": "building-sets",
    "educational-stem": "building-sets",
    "arts-crafts": "arts-crafts",
    "role-play": "role-play",
    "fashion-play-sets": "role-play",
    "board-games": "board-games",
    "baby-toddler": "baby-toddler",
    "monster-buddy-bags": "bags-accessories",
    "mini-shoulder-bags": "bags-accessories",
    "party-spotlight": "party-spotlight",
    "party-flags": "party-spotlight",
    "kids-hats": "party-spotlight",
    "halloween-hats": "seasonal",
    "funky-frights": "seasonal",
    "christmas-surprise": "seasonal",
    "handheld-fans": "home-gifts",
    "star-buddy-cups": "home-gifts",
    "bath-bomb-gifts": "home-gifts",
    "others": "home-gifts",
}


def fix_spelling(value: str) -> str:
    text = EMOJI_RE.sub(" ", value or "")
    text = text.replace("–", " ").replace("—", " ").replace("•", " ")
    for pattern, repl in SPELLING:
        text = re.sub(pattern, repl, text, flags=re.IGNORECASE)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def title_word(word: str, is_first: bool) -> str:
    if not word:
        return word
    match = re.match(r"^(\W*)(.*?)(\W*)$", word)
    if match and match.group(2) and match.group(2) != word:
        return f"{match.group(1)}{title_word(match.group(2), is_first)}{match.group(3)}"
    if word.lower() == "k-pop":
        return "K-Pop"
    if word.upper() in ACRONYMS:
        return word.upper()
    if re.fullmatch(r"\d+(cm|mm|oz|ml|pcs|pc|in|kg|g)", word, flags=re.IGNORECASE):
        return word.lower()
    if re.fullmatch(r"\d+\"", word):
        return word
    if word.lower() in {"2in1", "2-in-1"}:
        return "2-in-1"
    if "-" in word:
        return "-".join(title_word(part, True) for part in word.split("-"))
    if re.fullmatch(r"[A-Za-z]{0,4}\d{2,}", word) or re.fullmatch(r"\d+[A-Za-z]{1,3}", word):
        return word.upper()
    lower = word.lower()
    if lower in {"pokemon", "pokémon"}:
        return "Pokémon"
    if not is_first and lower in SMALL:
        return lower
    return lower[:1].upper() + lower[1:]


def title_case(value: str) -> str:
    bits = re.split(r"(\s+)", value.strip())
    seen = False
    out = []
    for bit in bits:
        if bit.isspace() or bit == "":
            out.append(bit)
            continue
        out.append(title_word(bit, not seen))
        seen = True
    return "".join(out).strip()


def dedupe_words(value: str) -> str:
    out = []
    seen: set[str] = set()
    for word in value.split():
        key = re.sub(r"[^\w+-]", "", word).lower()
        if key and key in seen:
            continue
        if key:
            seen.add(key)
        out.append(word)
    return " ".join(out)


def tidy_name(name: str) -> str:
    text = fix_spelling(name)
    for phrase in JUNK_PHRASES:
        text = re.sub(re.escape(phrase), " ", text, flags=re.IGNORECASE)
    text = re.sub(r"£\s*\d[\d.,]*", " ", text)
    text = re.sub(r"\b\d+[.,]\d{2}\b", " ", text)
    text = re.sub(r"[()]", " ", text)
    words = []
    for word in text.split():
        bare = re.sub(r"^[^\w]+|[^\w]+$", "", word)
        if bare.lower() in JUNK_WORDS:
            continue
        words.append(word)
    text = " ".join(words)
    text = re.sub(r"\s+", " ", text).strip(" -/,|&")
    text = dedupe_words(text)
    tidied = title_case(text)
    tidied = re.sub(r"\s+", " ", tidied).strip(" -/,")
    return tidied or "Toy"


def clean_clause(line: str) -> str:
    line = fix_spelling(line)
    line = re.sub(r"£\s*\d[\d.,]*", "", line)
    line = re.sub(r"\b\d+[.,]\d{2}\s*p?\b", "", line)
    line = re.sub(r"\s*@+\s*", " ", line)
    line = re.sub(r"\s+", " ", line).strip(" .,-/|*")
    if len(line) < 3:
        return ""
    if re.search(r"\bminimum\s+order\b", line, flags=re.IGNORECASE):
        return ""
    if re.fullmatch(
        r"(available now|in stock now|back in stock( now)?|new|or|just|price|dm.*|note batteries.*|only box selling|selling just box.*|hot sellers?.*|minimum\s+\d+\s*pcs?.*)",
        line,
        flags=re.IGNORECASE,
    ):
        return ""
    return line[0].upper() + line[1:]


def copy_from_text(text: str, name: str) -> tuple[str, str]:
    raw = text or ""
    raw = re.sub(r"stoc\s*/\s*k\b", "stock", raw, flags=re.IGNORECASE)
    chunks = re.split(r"[\n]+|(?:\s+/\s+)", raw)
    clauses: list[str] = []
    seen: set[str] = set()
    for chunk in chunks:
        clause = clean_clause(chunk)
        key = clause.lower()
        if not clause or key in seen:
            continue
        seen.add(key)
        clauses.append(clause)
    if not clauses:
        clauses = [name]
    description = ". ".join(clause.rstrip(".") for clause in clauses) + "."
    description = re.sub(r"\s+", " ", description).strip()
    short = description
    if len(short) > 170:
        short = short[:167].rsplit(" ", 1)[0].rstrip(".,; ") + "."
    return short, description


def money(value: float) -> str:
    return f"£{value:.2f}"


def features_for(price: float | None, moq_label: str, notes: list[str]) -> list[str]:
    rows = [moq_label]
    if price is None:
        rows.append("Price on request")
    else:
        rows.append(f"{money(price)} each")
    for note in notes:
        cleaned = fix_spelling(note).strip()
        if not cleaned or cleaned.lower() == "price tbc":
            continue
        if re.search(r"fix 2|re-matched|photos moved|possible duplicate|not added|box rate|single was", cleaned, flags=re.IGNORECASE):
            continue
        if re.search(r"minimum\s+order|min\s+order", cleaned, flags=re.IGNORECASE):
            continue
        cleaned = cleaned[0].upper() + cleaned[1:]
        if cleaned not in rows:
            rows.append(cleaned)
    return rows


def age_range(name: str, text: str) -> str:
    blob = f"{name} {text}".lower()
    if re.search(r"age\s*1\s*[-–to]+\s*3|ages?\s*0\b|toddler", blob):
        return "0-2 years"
    if re.search(r"ages?\s*13|13\+", blob):
        return "13+ years"
    if re.search(r"ages?\s*9\b|9-12|9\+", blob):
        return "9-12 years"
    if re.search(r"ages?\s*6\b|6-8|8\+", blob):
        return "6-8 years"
    return "3-5 years"


def _has(blob: str, *parts: str) -> bool:
    return any(part in blob for part in parts)


def _word(blob: str, *words: str) -> bool:
    return any(re.search(rf"\b{re.escape(item)}\b", blob) for item in words)


# Slug-level aisle locks. Applied after classify() so a rebuild keeps these remaps.
CATEGORY_OVERRIDES = {
    "christmas-surprise-figure-bag": "seasonal",
    "night-dragon-flop-hat": "party-spotlight",
    "spinner-character-wands": "light-up-toys",
    "trio-glow-spinner-wands": "light-up-toys",
    "toy-light-sabres": "light-up-toys",
    "super-driver-blue": "role-play",
    "character-3d-night-light": "light-up-toys",
    "glowing-snowman-set": "seasonal",
    "glowing-star-trees": "seasonal",
    "hanging-snow-lantern": "seasonal",
    "led-snow-globe-lanterns": "seasonal",
    "reindeer-snow-lanterns": "seasonal",
    "snow-scene-lanterns": "seasonal",
    "white-village-trees": "seasonal",
    "glowing-ear-buddy-plush": "plush-soft-toys",
    "super-arrow-set": "outdoor-sports",
    "kaleido-fan-wand": "light-up-toys",
    "marine-swat-justice-ship": "cars-vehicles",
    "teal-jointed-lizard": "novelty-keyrings",
    "volt-workshop-kit": "building-sets",
    "rk-1144-novelty-keyring": "novelty-keyrings",
    "rk-1145-ice-cream-keyring": "novelty-keyrings",
    "rk-1146-toast-keyring": "novelty-keyrings",
    "rk-1148-bun-keyring": "novelty-keyrings",
    "rk-1149-fries-keyring": "novelty-keyrings",
    "rk-1150-panda-pumpkin-keyring": "novelty-keyrings",
    "rk-1154-strawberry-keyring": "novelty-keyrings",
    "tg-lol-surprise-balls-152": "dolls",
    "tg-dinosaur-wings-300": "party-spotlight",
    "tg-k-pop-advent-calendar-2591": "seasonal",
}


def classify(name: str, text: str, old_slug: str, is_squishy: bool) -> tuple[str, str]:
    """Prefer the product name. Description is used for squishy signals and as a backup."""
    _force = {
        "airplane toy series": ("cars-vehicles", "vehicle"),
        "airplane series": ("cars-vehicles", "vehicle"),
        "3d stegosaurus": ("action-figures", "figure"),
        "lol surprise balls": ("dolls", "doll"),
        "dinosaur wings": ("party-spotlight", "party"),
        "k-pop advent calendar": ("seasonal", "seasonal"),
        "night dragon flop hat": ("party-spotlight", "party"),
        "toy light sabres": ("light-up-toys", "light"),
        "trio glow spinner wands": ("light-up-toys", "light"),
        "spinner character wands": ("light-up-toys", "light"),
        "christmas surprise figure bag": ("seasonal", "seasonal"),
        "super driver musical wheel (blue)": ("role-play", "role"),
        "character 3d night light": ("light-up-toys", "light"),
        "white village trees": ("seasonal", "seasonal"),
        "glowing snowman set": ("seasonal", "seasonal"),
        "glowing star trees": ("seasonal", "seasonal"),
        "hanging snow lantern": ("seasonal", "seasonal"),
        "led snow globe lanterns": ("seasonal", "seasonal"),
        "reindeer snow lanterns": ("seasonal", "seasonal"),
        "snow scene lanterns": ("seasonal", "seasonal"),
        "kaleido fan wand": ("light-up-toys", "light"),
        "super arrow set": ("outdoor-sports", "outdoor"),
        "glowing ear buddy plush": ("plush-soft-toys", "plush"),
        "marine swat justice ship": ("cars-vehicles", "vehicle"),
        "teal jointed lizard": ("novelty-keyrings", "keyring"),
        "volt workshop kit": ("building-sets", "build"),
    }
    if fix_spelling(name).lower().strip() in _force:
        return _force[fix_spelling(name).lower().strip()]
    name_blob = fix_spelling(name).lower()
    full = fix_spelling(f"{name} {text}").lower()

    def squishy_blob(blob: str) -> bool:
        if _has(blob, "slow-rise", "slow rise", "smusher"):
            return True
        if _word(blob, "squishy", "squishies", "squish", "needoh", "dumpling", "dumplings", "vaseline", "maltose"):
            return True
        if _word(blob, "squeeze", "squeezes") and not _has(blob, "water"):
            return True
        if _word(blob, "butter", "cheese") and _has(blob, "block", "brick", "stick", "packet", "tub", "jar", "squish", "squeeze"):
            return True
        if _word(blob, "jumbo") and not _word(blob, "plush", "teddy", "bag"):
            return True
        if _word(blob, "puffer") and _has(blob, "squish", "ball"):
            return True
        if _word(blob, "crunchy") and _has(blob, "squish", "fidget", "foam"):
            return True
        return False

    fidget_name = _word(name_blob, "spinner", "spinners", "slime", "slimes") or _has(
        name_blob, "push-pop", "push pop", "pop-it", "pop it", "fidget"
    )
    if is_squishy or old_slug in SQUISHY_OLD or squishy_blob(name_blob) or (squishy_blob(full) and not fidget_name):
        return "squishies", "squishy"

    def from_name(blob: str) -> tuple[str, str] | None:
        if _word(blob, "labubu", "lububu"):
            return "labubu", "labubu"
        if _has(blob, "advent"):
            return "seasonal", "seasonal"
        if _word(blob, "hat", "hats", "mask", "masks") or _has(blob, "flop hat", "flop-hat"):
            if _has(blob, "christmas", "halloween", "santa", "pumpkin"):
                return "seasonal", "seasonal"
            return "party-spotlight", "party"
        if _word(blob, "wand", "wands") and _has(blob, "glow", "light", "led", "spinner", "fibre", "fiber"):
            return "light-up-toys", "light"
        if _has(blob, "sabre", "saber"):
            return "light-up-toys", "light"
        if _has(blob, "gym", "musical mat", "tummy") or _has(blob, "age 1-3", "age 1–3"):
            return "baby-toddler", "baby"
        if _word(blob, "keyring", "keyrings", "keychain", "keychains") or _has(blob, "bag charm"):
            return "novelty-keyrings", "keyring"
        if _word(blob, "charm", "charms") and not _word(blob, "doll", "plush"):
            return "novelty-keyrings", "charm"
        if _has(blob, "k-pop", "k pop") or _word(blob, "k-pop", "kpop", "huntrix") or _has(blob, "sonny angel", "sony angel"):
            return "action-figures", "kpop"
        if _word(blob, "doll", "dolls", "barbie") or _has(blob, "cry baby", "baby lovely", "baby cry"):
            return "dolls", "doll"
        if _has(blob, "princess") and _has(blob, "doll", "baby", "lovely", "happy", "beauty"):
            return "dolls", "doll"
        if _word(blob, "blanket", "blankets", "bedding", "towel", "towels", "umbrella", "fan", "fans") or _has(
            blob, "cushion", "frame", "framed", "bath bomb", "lunch box"
        ):
            return "home-gifts", "home"
        if _word(blob, "cup", "cups", "bottle", "bottles"):
            return "home-gifts", "home"
        bag_blob = re.sub(r"\bgift bags?\b", " ", blob)
        if _word(bag_blob, "bag", "bags", "purse", "purses", "backpack", "trolley") or _has(bag_blob, "back pack", "school bag", "accessories"):
            return "bags-accessories", "bag"
        if _has(blob, "bubble") or _has(blob, "water blaster", "water game", "splash water", "water ball", "water gun"):
            return "bubble-blowers", "bubble"
        if _has(blob, "christmas", "halloween", "santa", "grinch", "advent", "pumpkin", "xmas"):
            return "seasonal", "seasonal"
        if _word(blob, "plush", "plushie", "teddy", "teddies") or _has(blob, "soft toy", "soft toys", "jellycat", "jelly cat", "ear buddy", "super soft", "barking dog"):
            return "plush-soft-toys", "plush"
        if _word(blob, "stitch", "bluey", "kuromi", "capybara", "panda", "bingo") and not _has(
            blob, "car", "bag", "cup", "light", "keyring", "make up", "makeup", "card", "bubble", "wand", "stick"
        ):
            return "plush-soft-toys", "plush"
        if (
            _word(blob, "slime", "slimes", "spinner", "spinners")
            or _has(blob, "pop-it", "pop it", "push-pop", "push pop", "fidget", "stress ball")
        ) and not _word(blob, "wand", "wands"):
            return "fidget-spinners", "fidget"
        if _has(blob, "stretch toy", "stretch toys"):
            return "fidget-spinners", "fidget"
        if _has(blob, "light-up", "light up", "glow", "neon", "lantern", "flashing") or _word(blob, "led"):
            return "light-up-toys", "light"
        if _has(blob, "playset", "play set", "role-play", "role play", "beauty fashion"):
            return "role-play", "role"
        if _has(blob, "kitchen", "make up", "makeup", "salon", "doctor", "castle", "vacuum", "vanity", "cosmetic", "steering", "guitar", "piano", "stroller", "dress-up", "dress up"):
            return "role-play", "role"
        if _has(blob, "build", "blocks", "building", "gear "):
            return "building-sets", "build"
        if _word(blob, "block", "blocks"):
            return "building-sets", "build"
        if _word(blob, "car", "cars", "truck", "trucks", "jeep", "suv", "tractor") or _has(
            blob, "mercedes", "bmw", "range rover", "airbus", "aircraft", "transformer", "remote control", "die-cast", "die cast", "racer", "garage"
        ) or _word(blob, "rc"):
            return "cars-vehicles", "vehicle"
        if _word(blob, "bike", "bikes"):
            return "outdoor-sports", "bike"
        if _word(blob, "figure", "figures", "figurine", "godzilla", "minecraft", "wakuku", "tyrannosaurus") or _has(
            blob, "avengers", "surprise bag", "surprise box", "blind box", "pop mart", "brain rot", "brainrot", "stranger things", "minions"
        ):
            return "action-figures", "figure"
        if _word(blob, "dragon", "dragons", "dinosaur", "dinosaurs", "spider", "spiders", "tyrannosaurus") and not _has(blob, "track"):
            return "action-figures", "figure"
        if _has(blob, "basketball game", "football game", "soccer game", "table game", "tabletop"):
            return "board-games", "game"
        if _word(blob, "gun", "guns", "ball", "balls", "football", "basketball", "skateboard", "dart", "darts") or _has(
            blob, "gel gun", "gel blaster", "blaster", "bow and arrow", "bullet", "binocular"
        ):
            return "outdoor-sports", "outdoor"
        if "track" in blob or _word(blob, "train"):
            return "building-sets", "track"
        if _word(blob, "card", "cards", "puzzle", "puzzles") or _has(blob, "board game", "trading card"):
            return "board-games", "game"
        if _has(blob, "pen", "pencil", "sticker", "tattoo", "stationery", "bead", "bracelet", "calendar", "craft"):
            return "arts-crafts", "arts"
        if _word(blob, "hat", "hats", "mask", "masks", "flag", "flags", "costume", "wand", "wands", "headband") or _has(blob, "air horn", "cactus"):
            return "party-spotlight", "party"
        if _has(blob, "baby", "toddler", "rattle", "teether"):
            return "baby-toddler", "baby"
        return None

    named = from_name(name_blob)
    if named:
        return named
    backed = from_name(full)
    if backed and backed[1] != "fallback":
        return backed[0], "description"
    if old_slug in OLD_FALLBACK:
        return OLD_FALLBACK[old_slug], "fallback"
    return "arts-crafts", "unmatched"



def theme_for(name: str, category: str) -> str:
    blob = name.lower()
    pairs = [
        ("christmas", "Christmas"),
        ("halloween", "Halloween"),
        ("labubu", "Labubu"),
        ("stitch", "Stitch"),
        ("bluey", "Bluey"),
        ("squish", "Squishy"),
        ("dinosaur", "Dinosaur"),
        ("dragon", "Dragon"),
        ("k-pop", "K-Pop"),
        ("football", "Football"),
        ("slime", "Sensory"),
        ("bubble", "Bubbles"),
        ("plush", "Plush"),
        ("doll", "Dolls"),
        ("car", "Vehicles"),
        ("light", "Lights"),
        ("keyring", "Keyrings"),
    ]
    for needle, theme in pairs:
        if re.search(rf"\b{re.escape(needle)}\b", blob):
            return theme
    fallback = {
        "plush-soft-toys": "Plush",
        "dolls": "Dolls",
        "squishies": "Squishy",
        "labubu": "Labubu",
        "action-figures": "Characters",
        "cars-vehicles": "Vehicles",
        "outdoor-sports": "Outdoor",
        "board-games": "Games",
        "role-play": "Pretend Play",
        "building-sets": "Building",
        "light-up-toys": "Lights",
        "seasonal": "Seasonal",
        "bags-accessories": "Bags",
        "novelty-keyrings": "Keyrings",
        "home-gifts": "Home",
        "arts-crafts": "Crafts",
        "fidget-spinners": "Sensory",
        "bubble-blowers": "Bubbles",
        "party-spotlight": "Party",
        "baby-toddler": "Baby",
    }
    return fallback.get(category, "Play")


BOX_QTY_PATTERNS = [
    re.compile(r"\bbox of\s*(\d+)\b", re.I),
    re.compile(r"\b(\d+)\s*(?:pcs|pc|pieces)?\s*in (?:a |the )?box\b", re.I),
    re.compile(r"\b(\d+)\s+in (?:a )?case\b", re.I),
    re.compile(r"\bcase of\s*(\d+)\b", re.I),
    re.compile(r"\b(\d+)\s+per box\b", re.I),
    re.compile(r"\bpack of\s*(\d+)\b", re.I),
    re.compile(r"complete items in box:\s*(\d+)", re.I),
    re.compile(r"carton pack:\s*(\d+)", re.I),
    re.compile(r"\b(\d+)\s*pcs per display\b", re.I),
    re.compile(r"\b(\d+)\s+per display(?: box)?\b", re.I),
]


def stated_box_qty(blob: str) -> int | None:
    """One clear box/case quantity. Conflicting numbers are not a single box size."""
    found: list[int] = []
    for pattern in BOX_QTY_PATTERNS:
        found.extend(int(match.group(1)) for match in pattern.finditer(blob or ""))
    unique = {qty for qty in found if qty > 0}
    if len(unique) == 1:
        return unique.pop()
    return None


def format_moq_label(qty: int, unit: str = "pcs") -> str:
    if qty == 1 and unit in {"pc", "pcs"}:
        return "Min order: 1 pc"
    word = "pcs" if unit in {"pc", "pcs"} else unit
    return f"Min order: {qty} {word} (1 box)"


def resolve_squishy_moq(blob: str, min_qty: int, unit: str, label: str) -> tuple[int, str, str | None]:
    """Return pieces, label, and a change reason. Reason is None when nothing should change."""
    stated = stated_box_qty(blob)
    old = int(min_qty or 1)
    unit = unit or "pcs"
    if stated is not None and stated != old:
        if old > 12 and stated < old:
            return old, label, None
        reason = f"product text states a box/case of {stated}"
        return stated, format_moq_label(stated, unit), reason
    if stated is not None and stated == old:
        wanted = format_moq_label(stated, unit)
        if label == wanted:
            return old, label, None
        return old, wanted, f"product text states a box/case of {stated}"
    if old > 12:
        return old, label, None
    if old == 12 and (not label or re.search(r"\b12\b", label)):
        return old, label or format_moq_label(12, unit), None
    if stated == 12:
        return 12, format_moq_label(12, unit), None if old == 12 else "product text states a box of 12"
    return 12, format_moq_label(12, unit), "squishy minimum is 12 pcs (1 box); no different box or case quantity in the product text"


def existing_slugs() -> set[str]:
    found: set[str] = set()
    for path in DATA.glob("*.ts"):
        if path.name in SKIP_SLUG_FILES:
            continue
        found.update(re.findall(r'slug:\s*"([^"]+)"', path.read_text(encoding="utf-8")))
    return found


def blocked(item: dict) -> bool:
    blob = " ".join(
        [item.get("name") or "", item.get("text") or "", " ".join(item.get("notes") or [])]
    ).lower()
    return any(word in blob for word in BLOCKED)


def parse_stock_products() -> list[dict]:
    products = []
    for filename in STOCK_FILES:
        text = (DATA / filename).read_text(encoding="utf-8")
        matches = list(re.finditer(r"\bslug:\s*\"([^\"]+)\"", text))
        for index, match in enumerate(matches):
            end = matches[index + 1].start() if index + 1 < len(matches) else match.start() + 4000
            window = text[match.start() : end]
            if "categorySlug" not in window:
                continue
            name = re.search(r"\bname:\s*\"([^\"]+)\"", window)
            cat = re.search(r"\bcategorySlug:\s*\"([^\"]+)\"", window)
            short = re.search(r"\bshortDescription:\s*\"([^\"]*)\"", window)
            desc = re.search(r"\bdescription:\s*\"([^\"]*)\"", window)
            price = re.search(r"\bprice:\s*([0-9.]+)", window)
            features = re.search(r"\bfeatures:\s*\[(.*?)\]", window, flags=re.S)
            pieces = re.search(r"\bpiecesPerBox:\s*(\d+)", window)
            moq = re.search(r'\bmoqLabel:\s*"([^"]*)"', window)
            if not name or not cat:
                continue
            slug = match.group(1)
            feature_text = features.group(1) if features else ""
            products.append(
                {
                    "slug": slug,
                    "name": name.group(1),
                    "text": f"{name.group(1)} {short.group(1) if short else ''} {desc.group(1) if desc else ''} {feature_text}",
                    "old": cat.group(1),
                    "price": float(price.group(1)) if price else 0,
                    "tbc": "priceTBC" in window[:900],
                    "image": f"/images/products/{slug}.jpg",
                    "source": filename,
                    "pieces": int(pieces.group(1)) if pieces else 1,
                    "moqLabel": moq.group(1) if moq else "",
                }
            )
    # products.ts lists stock spreads; keep the first definition of each slug.
    seen = set()
    unique = []
    for product in products:
        if product["slug"] in seen:
            continue
        if product["slug"].startswith("tg-"):
            continue
        seen.add(product["slug"])
        unique.append(product)
    return unique


def py_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def write_name_map(names: dict[str, str]) -> None:
    lines = [
        '"""Reviewed Telegram product titles. Written by scripts/import-telegram-products.py."""',
        "",
        "NAME_MAP: dict[str, str] = {",
    ]
    for slug in sorted(names):
        lines.append(f"    {py_string(slug)}: {py_string(names[slug])},")
    lines.append("}")
    lines.append("")
    NAME_MAP_PATH.write_text("\n".join(lines), encoding="utf-8")


def write_assigned(mapping: dict[str, str]) -> None:
    lines = [
        "/** Existing catalogue categories. Written by scripts/import-telegram-products.py. */",
        "",
        "export const assignedCategory: Record<string, string> = {",
    ]
    for slug in sorted(mapping):
        lines.append(f"  {json.dumps(slug)}: {json.dumps(mapping[slug])},")
    lines.append("};")
    lines.append("")
    ASSIGNED_PATH.write_text("\n".join(lines), encoding="utf-8")


def write_covers(covers: dict[str, str]) -> None:
    lines = [
        "/** Best in-category product photo for each aisle. Written by scripts/import-telegram-products.py. */",
        "",
        "export const categoryCovers: Record<string, string> = {",
    ]
    for slug in sorted(covers):
        lines.append(f"  {json.dumps(slug)}: {json.dumps(covers[slug])},")
    lines.append("};")
    lines.append("")
    COVERS_PATH.write_text("\n".join(lines), encoding="utf-8")


def rank_key(product: dict) -> tuple:
    src = (product.get("images") or [None])[0] or product.get("image") or ""
    photo = bool(src) and (src.startswith("/images/products/"))
    if src.startswith("/images/products/") and not src.startswith("/images/products/telegram/"):
        photo = (PUBLIC / src.lstrip("/")).exists()
    clear = (not product.get("tbc")) and float(product.get("price") or 0) > 0
    score = 0
    if photo and clear:
        score += 100
    elif photo:
        score += 40
    elif clear:
        score += 20
    if product.get("tbc") or float(product.get("price") or 0) <= 0:
        score -= 50
    if not photo:
        score -= 40
    if product.get("category") == "squishies":
        score += 35
    return (score, int(bool(photo)), int(clear))


def main() -> int:
    payload = json.loads(SOURCE.read_text(encoding="utf-8"))
    if "perfumes" in payload:
        pass
    toys = [item for item in payload["toys"] if item.get("add")]
    taken = existing_slugs()
    products = []
    skipped = []
    missing_images = []
    renamed = []
    doubtful_names = []
    name_map: dict[str, str] = {}
    category_notes = []
    squishy_flags: list[tuple[str, str, str, str]] = []

    for item in toys:
        if blocked(item):
            skipped.append(item.get("slug"))
            continue
        slug = item["slug"]
        if slug in taken:
            base = slug
            n = 2
            while slug in taken:
                slug = f"{base}-{n}"
                n += 1
            renamed.append((base, slug))
        taken.add(slug)
        raw_name = item.get("name") or slug
        name = NAME_OVERRIDES.get(item["slug"], tidy_name(raw_name))
        name_map[slug] = name
        if name == "Toy" or len(name) < 8 or raw_name.strip().lower() != name.lower() and len(name.split()) < 2:
            doubtful_names.append((slug, raw_name, name))
        price = item.get("unit_price")
        min_qty = int(item.get("min_qty") or 1)
        moq_unit = item.get("moq_unit") or "pcs"
        moq_label = item.get("moq_label") or f"Min order: {min_qty} pcs"
        notes = [str(note) for note in (item.get("notes") or [])]
        text = item.get("text") or ""
        short, description = copy_from_text(text, name)
        images = [str(src) for src in (item.get("images") or [])]
        for src in images:
            if not (PUBLIC / src.lstrip("/")).exists():
                missing_images.append(src)
        category, why = classify(name, f"{text} {description}", "", bool(item.get("is_squishy")))
        if slug in CATEGORY_OVERRIDES:
            category, why = CATEGORY_OVERRIDES[slug], "override"
        category_notes.append((name, category, why))
        product = {
            "slug": slug,
            "name": name,
            "price": 0 if price is None else price,
            "ageRange": age_range(name, text),
            "brand": "Toy Bloom Wholesale",
            "theme": theme_for(name, category),
            "categorySlug": category,
            "images": images,
            "shortDescription": short,
            "description": description,
            "features": features_for(None if price is None else float(price), moq_label, notes),
            "safety": SAFETY,
            "materials": "See packaging.",
            "isNew": True,
            "piecesPerBox": min_qty,
            "moqUnit": moq_unit,
            "moqLabel": moq_label,
            "stock": 50,
        }
        if price is None:
            product["priceTBC"] = True
        if category == "squishies":
            blob = f"{name}\n{text}\n{description}\n" + "\n".join(notes)
            pieces, moq_label, why = resolve_squishy_moq(blob, min_qty, moq_unit, moq_label)
            if why and (pieces != min_qty or moq_label != product["moqLabel"]):
                squishy_flags.append((slug, product["moqLabel"], moq_label, why))
            product["piecesPerBox"] = pieces
            product["moqUnit"] = moq_unit
            product["moqLabel"] = moq_label
            product["features"][0] = moq_label
        products.append(product)

    write_name_map(name_map)
    body = json.dumps(products, ensure_ascii=False, indent=2)
    OUT.write_text(
        'import type { Product } from "@/lib/types";\n\n'
        "/** Generated by scripts/import-telegram-products.py. Do not edit by hand. */\n"
        f"export const telegramStock: Product[] = {body};\n",
        encoding="utf-8",
    )

    assigned: dict[str, str] = {}
    existing_rows = []
    recategorised = 0
    for row in parse_stock_products():
        category, why = classify(row["name"], row["text"], row["old"], False)
        if row["slug"] in CATEGORY_OVERRIDES:
            category, why = CATEGORY_OVERRIDES[row["slug"]], "override"
        assigned[row["slug"]] = category
        if category != row["old"]:
            recategorised += 1
        row["category"] = category
        row["why"] = why
        row["images"] = [row["image"]] if (PUBLIC / "images" / "products" / f"{row['slug']}.jpg").exists() else []
        existing_rows.append(row)
    write_assigned(assigned)

    grouped: dict[str, list] = {}
    for product in products:
        grouped.setdefault(product["categorySlug"], []).append(
            {
                "price": product["price"],
                "tbc": product.get("priceTBC"),
                "images": product["images"],
                "category": product["categorySlug"],
                "name": product["name"],
            }
        )
    for row in existing_rows:
        grouped.setdefault(row["category"], []).append(row)

    covers = {}
    counts = Counter()
    for slug, rows in grouped.items():
        counts[slug] = len(rows)
        best = max(rows, key=rank_key)
        image = (best.get("images") or [None])[0]
        if not image:
            image = "/images/categories/squishies.jpg"
        covers[slug] = image
    write_covers(covers)

    plush_old = {"dolls-plush", "ear-buddy-plush", "bottle-plush", "star-buddy-plush"}
    category_updates: dict[str, str] = {}
    moq_updates: dict[str, tuple[int, str]] = {}
    review_changed: list[tuple[str, str, str, str]] = []
    review_left: list[tuple[str, str]] = []
    for row in existing_rows:
        if row["old"] in plush_old:
            category_updates[row["slug"]] = row["category"]
        pieces = int(row.get("pieces") or 1)
        stored = row.get("moqLabel") or ""
        old_label = stored or f"Min order: {pieces} pcs"
        if row["category"] == "squishies":
            new_pieces, new_label, why = resolve_squishy_moq(row["text"], pieces, "pcs", stored or old_label)
            if why and (new_pieces != pieces or new_label != old_label):
                squishy_flags.append((row["slug"], old_label, new_label, why))
                moq_updates[row["slug"]] = (new_pieces, new_label)
        elif pieces <= 1:
            stated = stated_box_qty(row["text"])
            if stated and stated > 1:
                new_label = format_moq_label(stated)
                review_changed.append((row["slug"], old_label, new_label, f"product text states a box/case of {stated}"))
                moq_updates[row["slug"]] = (stated, new_label)
            else:
                review_left.append((row["slug"], row["name"]))

    def patch_stock(text: str) -> str:
        matches = list(re.finditer(r'\bslug:\s*"([^"]+)"', text))
        if not matches:
            return text
        parts: list[str] = []
        cursor = 0
        for index, match in enumerate(matches):
            end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
            parts.append(text[cursor:match.start()])
            window = text[match.start():end]
            slug = match.group(1)
            if slug in category_updates:
                window = re.sub(
                    r'categorySlug:\s*"[^"]*"',
                    f'categorySlug: "{category_updates[slug]}"',
                    window,
                    count=1,
                )
            if slug in moq_updates:
                pieces, label = moq_updates[slug]
                if re.search(r"\bpiecesPerBox:\s*\d+", window):
                    window = re.sub(r"\bpiecesPerBox:\s*\d+", f"piecesPerBox: {pieces}", window, count=1)
                else:
                    window = re.sub(
                        r"(\n\s*)stock:\s*",
                        rf"\1piecesPerBox: {pieces},\n\1stock: ",
                        window,
                        count=1,
                    )
                rendered = json.dumps(label, ensure_ascii=False)
                if re.search(r'\bmoqLabel:\s*"[^"]*"', window):
                    window = re.sub(r'\bmoqLabel:\s*"[^"]*"', f"moqLabel: {rendered}", window, count=1)
                else:
                    window = re.sub(
                        r"(\n\s*)stock:\s*",
                        rf"\1moqLabel: {rendered},\n\1stock: ",
                        window,
                        count=1,
                    )
            parts.append(window)
            cursor = end
        parts.append(text[cursor:])
        updated = "".join(parts)
        return re.sub(r"\n\r?\n(\s*(?:piecesPerBox|moqLabel|stock):)", r"\n\1", updated)

    for filename in STOCK_FILES:
        path = DATA / filename
        original = path.read_text(encoding="utf-8")
        updated = patch_stock(original)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            print(f"patched {filename}")

    flag_lines = [
        "# Squishy minimum orders",
        "",
        "Every Squishies product is at least 12 pcs (1 box) unless its own text states a different box or case quantity. Existing box quantities above 12 were left as they were.",
        "",
        "| Slug | Old | New | Reason |",
        "| --- | --- | --- | --- |",
    ]
    for slug, old, new, why in squishy_flags:
        flag_lines.append(f"| `{slug}` | {old} | {new} | {why} |")
    flag_lines.append("")
    flag_lines.append(f"{len(squishy_flags)} products changed.")
    flag_lines.append("")
    (ROOT / "SQUISHY_MOQ_FLAGS.md").write_text("\n".join(flag_lines), encoding="utf-8")

    review_lines = [
        "# Older catalogue minimum orders",
        "",
        "Non-Telegram products that were on a minimum of 1. A box quantity was set only when the product name, description, or features state one. Squishies are listed in `SQUISHY_MOQ_FLAGS.md`.",
        "",
        "## Changed",
        "",
        "| Slug | Old | New | Reason |",
        "| --- | --- | --- | --- |",
    ]
    if review_changed:
        for slug, old, new, why in review_changed:
            review_lines.append(f"| `{slug}` | {old} | {new} | {why} |")
    else:
        review_lines.append("| — | — | — | No older non-squishy product stated a box or case quantity while still on a minimum of 1. |")
    review_lines.extend(["", "## Left at 1", ""])
    for slug, name in review_left:
        review_lines.append(f"- `{slug}` — {name}")
    review_lines.append("")
    review_lines.append(f"{len(review_changed)} changed. {len(review_left)} left at 1.")
    review_lines.append("")
    (ROOT / "MOQ_REVIEW.md").write_text("\n".join(review_lines), encoding="utf-8")

    names = {}
    cat_text = (DATA / "categories.ts").read_text(encoding="utf-8")
    for match in re.finditer(r'slug:\s*"([^"]+)"[\s\S]{0,240}?name:\s*"([^"]+)"', cat_text):
        names[match.group(1)] = match.group(2)
    count_lines = [
        "# Category counts",
        "",
        "Generated from the catalogue after `scripts/import-telegram-products.py`. Every product sits in one aisle.",
        "",
        "| Category | Slug | Products |",
        "| --- | --- | ---: |",
    ]
    total = 0
    for slug, count in counts.most_common():
        total += count
        count_lines.append(f"| {names.get(slug, slug)} | `{slug}` | {count} |")
    count_lines.append(f"| **Total** | | **{total}** |")
    count_lines.append("")
    count_lines.append("Dolls and Plush & Soft Toys are separate aisles. Plush keyrings stay in Keyrings & Bag Charms.")
    count_lines.append("")
    (ROOT / "CATEGORY_COUNTS.md").write_text("\n".join(count_lines), encoding="utf-8")

    print(f"wrote {len(products)} telegram products -> {OUT}")
    print(f"names {len(name_map)} -> {NAME_MAP_PATH}")
    print(f"assigned existing {len(assigned)} recategorised {recategorised}")
    print("skipped perfume-like", skipped)
    print("renamed slugs", renamed)
    print("missing images", len(missing_images))
    print("price on request", sum(1 for product in products if product.get("priceTBC")))
    print("MOQ labels", sum(1 for product in products if product.get("moqLabel")))
    print("--- category counts (telegram + existing) ---")
    for slug, count in counts.most_common():
        print(f"  {count:4} {slug}")
    print("--- telegram category ---")
    tg_counts = Counter(product["categorySlug"] for product in products)
    for slug, count in tg_counts.most_common():
        print(f"  {count:4} {slug}")
    fallback = [row for row in existing_rows if row["why"] == "fallback"]
    unmatched = [row for row in existing_rows if row["why"] == "unmatched"]
    print("existing fallback", len(fallback), "unmatched", len(unmatched))
    for row in unmatched[:40]:
        print(" UNMATCHED", row["old"], row["name"])
    for row in fallback:
        print(" FALLBACK", row["old"], "->", row["category"], row["name"])
    tg_unmatched = [note for note in category_notes if note[2] in {"fallback", "unmatched"}]
    print("telegram weak", len(tg_unmatched))
    for note in tg_unmatched:
        print(" TG", note[2], note[1], note[0])
    print("--- doubtful short names ---")
    for slug, raw, name in doubtful_names:
        if raw.strip() != name:
            print(f"  {name}  <=  {raw}")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
