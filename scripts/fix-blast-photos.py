"""Hide remaining blast/AI older-catalogue photos; crop real keepers; fix Telegram leads."""
from __future__ import annotations

import json
import re
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter, ImageEnhance

ROOT = Path(r"d:\toybloom\site")
PROD = ROOT / "public" / "images" / "products"
HIDDEN_TS = ROOT / "lib" / "data" / "hidden-products.ts"
HIDDEN_MD = ROOT / "HIDDEN_PRODUCTS.md"
TG_STOCK = ROOT / "lib" / "data" / "telegram-stock.ts"
COVERS = ROOT / "lib" / "data" / "category-covers.ts"
MEDIA = ROOT / "lib" / "media.ts"
OUT = ROOT / "scripts" / "_blast-fix.json"

STOCK_FILES = [
    ROOT / "lib" / "data" / "products.ts",
    ROOT / "lib" / "data" / "new-stock.ts",
    ROOT / "lib" / "data" / "extra-stock.ts",
    ROOT / "lib" / "data" / "china-stock.ts",
    ROOT / "lib" / "data" / "advance-stock.ts",
    ROOT / "lib" / "data" / "innovative-stock.ts",
    ROOT / "lib" / "data" / "october-new-stock.ts",
]

# Confirmed real wholesale / desk photos — crop only, never hide.
FORCE_KEEP = {
    "rainbow-butter-squishy",
    "grape-cluster-squishy",
    "gummy-bear-squeeze-box",
    "jelly-gummy-bear",
    "christmas-super-squishy-box",
}

COVER_FALLBACKS = {
    "baby-toddler": "/images/products/telegram/tg-kids-push-car-age-1-3-970-1.webp",
    "board-games": "/images/products/telegram/tg-3d-plastic-playing-cards-7-1.webp",
    "cars-vehicles": "/images/products/telegram/tg-mercedes-metal-model-car-with-light-sound-22cm-725-1.webp",
    "fidget-spinners": "/images/products/telegram/tg-mini-slimes-1181-1.webp",
    "novelty-keyrings": "/images/products/telegram/tg-design-keyrings-200-1.webp",
}


def hidden() -> list[str]:
    return re.findall(r'"([a-z0-9-]+)"', HIDDEN_TS.read_text(encoding="utf-8"))


def names_by_slug() -> dict[str, str]:
    mapping: dict[str, str] = {}
    for path in STOCK_FILES + [TG_STOCK]:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for slug, name in re.findall(r'slug:\s*"([^"]+)"[\s\S]{0,280}?name:\s*"([^"]+)"', text):
            mapping[slug] = name
        for slug, name in re.findall(r'"slug":\s*"([^"]+)"[\s\S]{0,280}?"name":\s*"([^"]+)"', text):
            mapping[slug] = name
    return mapping


def older_slugs() -> list[str]:
    slugs: list[str] = []
    for path in STOCK_FILES:
        text = path.read_text(encoding="utf-8")
        slugs.extend(re.findall(r'(?:slug:|"slug":)\s*"([a-z0-9-]+)"', text))
    # de-dupe, keep order
    seen = set()
    out = []
    for s in slugs:
        if s not in seen:
            seen.add(s)
            out.append(s)
    return out


def score_path(path: Path) -> dict:
    with Image.open(path) as im:
        rgb = im.convert("RGB")
        w, h = rgb.size
        work = rgb
        if max(w, h) > 900:
            work = rgb.resize((int(w * 900 / max(w, h)), int(h * 900 / max(w, h))), Image.Resampling.BILINEAR)
        arr = np.asarray(work, dtype=np.uint8)
        hsv = np.asarray(work.convert("HSV"), dtype=np.uint8)
    s = hsv[:, :, 1].astype(np.float32)
    v = hsv[:, :, 2].astype(np.float32)
    neon = float(((s > 180) & (v > 180)).mean())
    q = (arr.astype(np.int32) // 16).reshape(-1, 3)
    quniq = len({(int(a), int(b), int(c)) for a, b, c in q[:: max(1, q.shape[0] // 4000)]})
    small = np.asarray(work.resize((96, 96), Image.Resampling.BILINEAR), dtype=np.float32)
    grain = float((np.abs(np.diff(small, axis=0)).mean() + np.abs(np.diff(small, axis=1)).mean()) / 2)
    lum = arr.mean(axis=2)
    white = float((lum > 248).mean())
    blown = float(((v > 250) & (s < 18)).mean())
    reasons = []
    if min(w, h) < 280:
        reasons.append("low-res")
    if blown > 0.38:
        reasons.append("blown-out")
    if white > 0.52 and grain < 6.2:
        reasons.append("empty-white / CGI")
    if quniq < 95:
        reasons.append("posterized")
    if quniq < 130 and grain < 5.0:
        reasons.append("flat / cartoon")
    if neon > 0.24 and grain < 7.0:
        reasons.append("neon blast")
    return {
        "w": w,
        "h": h,
        "bytes": path.stat().st_size,
        "neon": round(neon, 4),
        "quniq": quniq,
        "grain": round(grain, 2),
        "white": round(white, 3),
        "blown": round(blown, 3),
        "reasons": reasons,
        "bad": bool(reasons),
    }


def crop_light(im: Image.Image, size: int = 1400) -> Image.Image:
    rgb = im.convert("RGB")
    arr = np.asarray(rgb)
    lum = arr.mean(axis=2)
    content = lum < 250
    if 0.05 < content.mean() < 0.9:
        ys, xs = np.where(content)
        pad = int(0.04 * max(rgb.size))
        box = (
            max(0, int(xs.min()) - pad),
            max(0, int(ys.min()) - pad),
            min(rgb.width, int(xs.max()) + pad + 1),
            min(rgb.height, int(ys.max()) + pad + 1),
        )
        rgb = rgb.crop(box)
    rgb.thumbnail((size, size), Image.Resampling.LANCZOS)
    rgb = rgb.filter(ImageFilter.UnsharpMask(radius=1.05, percent=26, threshold=5))
    rgb = ImageEnhance.Contrast(rgb).enhance(1.02)
    return rgb


def write_hidden(existing: list[str], new_rows: list[tuple[str, str, str]]) -> None:
    merged = []
    for s in existing + [r[0] for r in new_rows]:
        if s not in merged:
            merged.append(s)
    body = "\n".join(f'  "{s}",' for s in merged)
    HIDDEN_TS.write_text(
        "/**\n"
        " * Products hidden until the client supplies real photos (see HIDDEN_PRODUCTS.md).\n"
        " * Data is kept in the stock files; remove a slug here to unhide it.\n"
        " */\n"
        "export const HIDDEN_PRODUCT_SLUGS: string[] = [\n"
        f"{body}\n"
        "];\n",
        encoding="utf-8",
    )
    if not new_rows:
        return
    md = HIDDEN_MD.read_text(encoding="utf-8")
    extra = "\n".join(f"| {slug} | {name} | {reason} |" for slug, name, reason in new_rows)
    marker = "## How to unhide"
    if marker in md:
        md = md.replace(
            marker,
            "## Older catalogue — still blast / AI on 24 Oct 2026\n\n"
            "These were still on the storefront after the first hide pass. "
            "No matching real photo in this workspace.\n\n"
            "| Slug | Name | Reason |\n|---|---|---|\n"
            f"{extra}\n\n"
            + marker,
        )
        HIDDEN_MD.write_text(md, encoding="utf-8")


def fix_telegram_leads() -> dict:
    text = TG_STOCK.read_text(encoding="utf-8")
    promoted = []
    hid = []

    def repl(match: re.Match) -> str:
        slug = match.group(1)
        block = match.group(0)
        imgs = re.findall(r'"(/images/products/telegram/[^"]+)"', block)
        if not imgs:
            return block
        scored = []
        for src in imgs:
            path = ROOT / "public" / src.lstrip("/")
            if not path.exists():
                continue
            with Image.open(path) as im:
                w, h = im.size
            scored.append((w * h, path.stat().st_size, src, w, h))
        if not scored:
            hid.append(slug)
            return block
        scored.sort(reverse=True)
        best_px, _sz, best_src, bw, bh = scored[0]
        if min(bw, bh) < 280 and best_px < 280 * 280:
            hid.append(slug)
            return block
        if imgs[0] != best_src:
            new_order = [best_src] + [s for _, _, s, _, _ in scored if s != best_src]
            inner = ",\n      ".join(f'"{s}"' for s in new_order)
            block = re.sub(r'"images":\s*\[.*?\]', f'"images": [\n      {inner}\n    ]', block, count=1, flags=re.S)
            promoted.append(slug)
        return block

    new_text = re.sub(
        r'\{\s*"slug":\s*"([^"]+)"[\s\S]*?\n  \}',
        repl,
        text,
    )
    if new_text != text:
        TG_STOCK.write_text(new_text, encoding="utf-8")
    return {"promoted": promoted, "hide_tiny": hid}


def retarget_covers(hidden_set: set[str]) -> list[str]:
    text = COVERS.read_text(encoding="utf-8")
    changed = []
    for aisle, fallback in COVER_FALLBACKS.items():
        m = re.search(rf'"{aisle}":\s*"([^"]+)"', text)
        if not m:
            continue
        src = m.group(1)
        slug = Path(src).stem
        slug = re.sub(r"-n?\d+$", "", slug)
        if src.startswith("/images/products/") and not src.startswith("/images/products/telegram/"):
            if slug in hidden_set or aisle in COVER_FALLBACKS:
                # only swap if the current file is a hidden older-catalogue shot
                if slug in hidden_set:
                    text = text.replace(f'"{aisle}": "{src}"', f'"{aisle}": "{fallback}"')
                    changed.append(aisle)
    COVERS.write_text(text, encoding="utf-8")
    return changed


def main() -> None:
    already = hidden()
    already_set = set(already)
    names = names_by_slug()
    hide_rows: list[tuple[str, str, str]] = []
    kept = []
    cropped = []

    for slug in older_slugs():
        if slug in already_set:
            continue
        path = PROD / f"{slug}.jpg"
        if not path.exists():
            continue
        info = score_path(path)
        if slug in FORCE_KEEP or not info["bad"]:
            im = Image.open(path)
            out = crop_light(im)
            out.save(path, "JPEG", quality=90, optimize=True, progressive=True)
            cropped.append(slug)
            kept.append({"slug": slug, **info})
            print(f"KEEP {slug} {info['reasons'] or 'ok'} {info['w']}x{info['h']} grain={info['grain']} white={info['white']}")
            continue
        hide_rows.append((slug, names.get(slug, slug), ", ".join(info["reasons"])))
        print(f"HIDE {slug} {info['reasons']} grain={info['grain']} white={info['white']} q={info['quniq']}")

    tg = fix_telegram_leads()
    for slug in tg["hide_tiny"]:
        if slug not in already_set:
            hide_rows.append((slug, names.get(slug, slug), "All Telegram photos too small"))

    write_hidden(already, hide_rows)
    covers = retarget_covers(already_set | {s for s, _, _ in hide_rows})

    report = {
        "hidden_new": [s for s, _, _ in hide_rows],
        "kept": [k["slug"] for k in kept],
        "cropped": cropped,
        "telegram_promoted": tg["promoted"],
        "telegram_tiny_hidden": tg["hide_tiny"],
        "covers": covers,
    }
    OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(
        f"\nhidden_new={len(hide_rows)} kept={len(kept)} "
        f"tg_promoted={len(tg['promoted'])} tg_tiny={len(tg['hide_tiny'])} covers={covers}"
    )


if __name__ == "__main__":
    main()
