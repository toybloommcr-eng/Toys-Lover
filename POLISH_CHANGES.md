# Polish changes

Telegram stock is regenerated from `C:\Users\Adeel\toybloom_work\curated_v2.json` (`toys` where `add == true` only). The `perfumes` key is never read. `npm run build` completes as a static export.

## Counts

- **Minimum orders shown:** 765 products. All 325 Telegram lines use the curated `moq_label` verbatim (for example `Min order: 15 packs (1 box)`), with `piecesPerBox` set to `min_qty` and optional `moqUnit` / `moqLabel`. The other 440 products show `Min order: N pcs` from `piecesPerBox`. The same label is the first feature. Old `Minimum order: 1 pcs` feature lines are removed.
- **Names tidied:** 325 Telegram titles. Final titles live in `scripts/telegram_name_map.py` (reviewed slug → name dict produced by the importer, plus a few caption overrides).
- **Products re-categorised:** 367 existing products moved to a new aisle. All 325 Telegram products were categorised from name + original text. 73 existing products already matched their new aisle.
- **Per-category counts:** see `CATEGORY_COUNTS.md`. 20 categories, none empty, no Others bucket.

## What shoppers see

- Product tiles, product cards and product pages show the minimum-order line.
- Listings use `rankProducts()` in `lib/rank.ts`: real photo plus a clear price first, squishies boosted, price-on-request and weak photos lower.
- Homepage and shop page lead with a Squishies section that links to `/shop/squishies/`.

## Doubtful

- **Thin captions** were given a clearer title in the name map: Series 4 / Series 5 collectible figures, Christmas Assortment, Wakuku Character Figures, Baby Lovely Doll, Baby Cry Doll, Be Happy Princess Doll, Light-Up Trend Toys, Pets Home 2-in-1 Playset, Sugar Peanut Squishy, Angel Unicorn Pegasus Figure, Jeffy Mom and Dad Dolls, Labubu Collectible. The Telegram text does not name a character for Series 4, Series 5 or the bare “Christmas” post.
- **Stick → Stitch** on “Stick side bag”. The request listed Stich and Atich, not Stick. The surrounding stock is Stitch bags, so the title says Stitch.
- **Once → Ones** and **advert → advent** (advent calendars) are applied across titles.
- **Gel Gun** stays a short title. That is the whole caption.
- **Fruit Garden Bucket Set** stayed in Outdoor & Sports from its old aisle. The name does not say ball, blaster or bike.
- **Glow-in-the-dark stickers** landed in Light-Up Toys because the title says “glow”, not Arts & Stationery.
- **K-Pop keyrings** are in Keyrings & Bag Charms. Other K-Pop lines are in K-Pop & Collectible Figures (`action-figures`, URL kept).
- **Labubu squishies** are in Squishies, not the Labubu aisle, so every squishy is on one page.
- **Dumpling keyrings / dumpling spinners** follow the squishy rule when the title says dumpling.
- **China fidget blurbs** say “slow-rise” even on spinners and push-pops. Those names stay in Fidget & Sensory. Other “slow-rise” food blocks stay in Squishies.
- **Baby & Toddler** has 3 products (gym, musical mat, push car). Most soft toys sit in Plush.
- **Arts, Crafts & Stationery** has 5 products.
- **10 Telegram lines** are price on request. They sort below priced photos.
- **Retired aisle URLs** (fruit-squishies, sensory-jars, games-gadgets, educational-stem, and the other micro-aisles) are no longer pages. In-site links point at the new aisles. Kept slugs such as `dolls-plush`, `action-figures`, `board-games`, `fidget-spinners`, `party-spotlight`, `building-sets`, `arts-crafts`, `bubble-blowers`, `novelty-keyrings` and `light-up-toys` still resolve, with updated names where the aisle is broader.
