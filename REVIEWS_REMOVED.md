# Reviews and ratings removed

Fake ratings, review counts, testimonials, and review structured data are gone. Category and shop listing pages no longer have a filters sidebar. `npm run build` completed successfully (820 static pages).

Checked in the browser against the static export:

- Homepage at 1280px and 375px: no star rows, no “Loved by Parents” block, no “Top Rated Store” badge, no horizontal overflow.
- Product page `/product/piano-fitness-gym/` at 1280px and 375px: title sits on the badges and price block with no empty rating row. JSON-LD has no `AggregateRating`.
- Category page `/shop/squishies/` : product count and Sort remain. No Filters box, price/brand/theme controls, or “In this category” list. Grid is 2 columns at 375px and 6 columns at 1280px.

## Ratings and review UI

- `components/ui/Rating.tsx` — deleted. Star row plus numeric rating and review count.
- `components/product/ProductCard.tsx` — removed the rating row under the minimum-order line.
- `components/product/ProductTile.tsx` — removed the star row (used on category grids, sale, discover/lookbook, and related products).
- `components/home/BestSellers.tsx` — removed the star row on homepage best-seller cards.
- `app/product/[slug]/page.tsx` — removed the rating next to the category badges, and removed `aggregateRating` / `AggregateRating` / `ratingValue` / `reviewCount` from the product JSON-LD. Organization JSON-LD in `app/layout.tsx` had no review schema and was left as-is.
- `lib/types.ts` — dropped required `rating` and `reviewCount` from `Product`.
- `lib/rank.ts` — `rankScore()` no longer adds a bonus from `reviewCount`. Popularity sorting still uses `rankProducts()` (photo, clear price, squishy boost, then name). There was no separate “sort by rating” option in `SORT_OPTIONS`.

## Product data

`rating` and `reviewCount` lines were removed from every catalogue record:

- `lib/data/products.ts` (190 lines)
- `lib/data/telegram-stock.ts` (650 lines)
- `lib/data/new-stock.ts` (222 lines)
- `lib/data/china-stock.ts` (214 lines)
- `lib/data/advance-stock.ts` (128 lines)
- `lib/data/extra-stock.ts` (64 lines)
- `lib/data/october-new-stock.ts` (40 lines)
- `lib/data/innovative-stock.ts` (22 lines)

Generators no longer emit those fields:

- `scripts/import-telegram-products.py` (fixed 4.6 / 12, and `reviews.ts` dropped from the slug skip list)
- `scripts/import-october-new-products.py`
- `scripts/import-extra-categories.py`
- `scripts/import-new-categories.py`
- `scripts/import-advance-categories.py`

## Testimonials and store-rating claims

- `lib/data/reviews.ts` — deleted. Invented kid and parent quotes (Mia, Noah, Aisha, Leo, and the rest), each with a 5-star rating.
- `components/home/Reviews.tsx` — deleted. “Appreciations & play notes” carousel. It was not mounted on the homepage.
- `components/home/ParentLove.tsx` — deleted. Homepage section “Loved by Parents, Trusted by Kids”.
- `app/page.tsx` — stopped rendering `ParentLove`.
- `components/home/TrustBadges.tsx` — removed the “Top Rated Store / Loved by UK families” badge. The remaining four badges use a 4-column desktop row.
- `components/home/Hero.tsx` — removed the “Parent Approved” claim under the hero.
- `lib/constants.ts` — site description no longer says “trusted UK toy store”.
- `components/product/ProductGrid.tsx` — empty state no longer says “No toys match those filters yet.”

Blog category label “Toy Safety & Reviews” in `lib/data/blog.ts` is an article topic, not a customer-review widget, so it was left in place. No `X happy customers`, `4.9 average`, or “trusted by thousands” copy was present elsewhere.

## Category and shop filters

- `components/shop/CategoryShop.tsx` — removed the Filters box: price range, brand, theme, and the “In this category” list with “+N more”. That box was the mobile filter UI as well (a two-column panel above the grid; there was no separate drawer button). Product count and the Sort dropdown stay. Default sort is still popularity via `rankProducts()`; Newest, Price: Low to High, and Price: High to Low are unchanged.
- `app/shop/[slug]/page.tsx` — no longer passes brand or theme lists into the shop.
- `lib/data/products.ts` — removed `getBrands()` and `getThemes()`, which only fed those dropdowns.
- `lib/constants.ts` — removed `PRICE_RANGES`.
- `components/product/ProductGrid.tsx` — category listings use a `wide` grid: 2 columns on mobile, then 3 / 4 / 5 / 6 from the `sm` breakpoint upward, across the full content width.
- `app/shop/page.tsx` is the category index and had no filter sidebar.

Product photos under `public/images/products/telegram/` were not changed.
