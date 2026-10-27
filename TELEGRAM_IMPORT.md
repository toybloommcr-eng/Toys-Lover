# Telegram wholesale toy import

Imported on branch `telegram-products` from `curated_with_images.json`, key `toys`, entries with `add == true` only. The `perfumes` key was not read. No perfume, fragrance, body spray, or air freshener products were added.

## Count

**325 products** added as `telegramStock` in `lib/data/products.ts` (after `octoberNewStock`). No slug collisions with the existing catalog. All 325 photo files were already present under `public/images/products/telegram/`.

## What changed

- `scripts/import-telegram-products.py` reads the curated JSON and writes `lib/data/telegram-stock.ts`.
- Each line uses the given slug, a tidied display name (spelling fixes such as Stitch, Halloween, Dinosaur, Bluey, title case, prices removed from the name), `price` = unit price in GBP, and `piecesPerBox` = minimum order quantity.
- Copy (`shortDescription`, `description`, `features`) comes from the Telegram caption and notes. Features include `Minimum order: N pcs, £X.XX each` plus any bulk or case pricing from notes.
- Brand is Toy Bloom Wholesale. Theme is chosen from the product. Age range is 3–5 years unless the caption states another age. Rating 4.6, review count 12, stock 50, `isNew` true. Safety and materials use the agreed wholesale wording.
- `Product.priceTBC` marks lines with no unit price. Those show **Price on request** instead of £0.00, and add-to-cart is replaced with **Ask for price** linking to the contact page.
- Wholesale unit prices are labelled **Each**. The minimum order is shown separately, so a 20-piece minimum at £2.50 is not displayed as a £2.50 box.
- `productGallery()` keeps Telegram `images` arrays (order preserved, first image on cards, full gallery on the product page). Every other product still uses `/images/products/<slug>.jpg`.
- Product photos use `object-contain` on a white background. `/images/products/telegram/` paths match the framed/studio photo treatment.
- `npm run build` completed and wrote the static export to `out/` (851 routes).

## Price on request

These 10 lines have `unit_price` null (`price: 0`, `priceTBC: true`):

| Product | Slug |
| --- | --- |
| Labubu Soft Toy with Keyring | `tg-labubu-soft-toy-with-keyring-1947` |
| Labubu Squishy | `tg-lububu-squishy-2083` |
| Labubu Lay Down | `tg-lububu-lay-down-2089` |
| Angel Labubu with Wings | `tg-angel-labubu-with-wings-2164` |
| Labubu Bag | `tg-labubu-bag-2237` |
| Series-5 | `tg-series-5-2272` |
| Labubu - New Range | `tg-labubu-new-range-2372` |
| Rainbow Big Size Labubu (Back in Stock) | `tg-rainbow-big-size-labubu-back-in-stock-2467` |
| Dumplings Rainbow & Squeeze Cube | `tg-dumplings-rainbow-squeeze-cube-3426` |
| USB Digital Cooling Fans | `tg-usb-digital-cooling-fans-3614` |
