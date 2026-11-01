# Shop CRM integration

The catalogue now comes from **`data/crm/products.json`** and **`data/crm/categories.json`**. The Shop CRM admin (repo `9say9/shop-crm`) edits these over the GitHub Contents API, and each save is a commit to `main`, which triggers the GitHub Pages deploy.

- Bridge: `lib/data/crm.ts`. `products` and `categories` (in `lib/data/products.ts` and `lib/data/categories.ts`) use the CRM JSON when it's non-empty, and otherwise fall back to the legacy TS catalogue.
- Seeded from the legacy catalogue on 1 Nov 2026: 477 visible products and 34 categories. All 541 exported pages were text-identical to the previous build.
- Photos uploaded in the CRM are committed to `public/products/`.
- **Rollback:** put `[]` in both JSON files (the legacy data is used again), or revert this commit.
- Heads-up: catalogue edits should now happen in the CRM. Edits to the old `lib/data/*-stock.ts` files have no effect while the JSON is in use.
