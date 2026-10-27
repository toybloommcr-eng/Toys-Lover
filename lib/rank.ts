import type { Product } from "@/lib/types";

export function hasClearPrice(product: Pick<Product, "price" | "priceTBC">) {
  return !product.priceTBC && product.price > 0;
}

export function hasGoodPhoto(product: Pick<Product, "images">) {
  const src = product.images?.[0] ?? "";
  return src.startsWith("/images/products/");
}

const SQUISHY_LISTING_SLUGS = new Set([
  "squishies",
  "jumbo-squishies",
  "small-squishies",
  "sugar-squishies",
  "wax-squishies",
  "butter-squishies",
  "crunchy-squishies",
  "vaseline-squishies",
  "dumpling-squishies",
  "christmas-squishies",
]);

export function isSquishyListing(product: Pick<Product, "categorySlug" | "name">) {
  return SQUISHY_LISTING_SLUGS.has(product.categorySlug) || /squish|squeeze|needoh|dumpling/i.test(product.name);
}

/** Higher scores sort first: real photo and a clear price, with squishies boosted. */
export function rankScore(product: Product) {
  const photo = hasGoodPhoto(product);
  const price = hasClearPrice(product);
  let score = 0;
  if (photo && price) score += 100;
  else if (photo) score += 40;
  else if (price) score += 20;
  if (!photo) score -= 40;
  if (product.priceTBC || product.price <= 0) score -= 50;
  if (isSquishyListing(product)) score += 35;
  // Stronger listings: more real photos, best sellers, fresh Telegram stock with cleaned photos.
  score += Math.min(product.images?.length ?? 0, 4) * 6;
  if (product.isBestSeller) score += 15;
  if (product.slug.startsWith("tg-")) score += 10;
  return score;
}

export function rankProducts<T extends Product>(items: T[]): T[] {
  return [...items].sort((a, b) => rankScore(b) - rankScore(a) || tieBreak(a.slug) - tieBreak(b.slug));
}

/** Stable pseudo-random tiebreak so equal scores do not list alphabetically. */
function tieBreak(slug: string) {
  let h = 2166136261;
  for (let i = 0; i < slug.length; i++) h = Math.imul(h ^ slug.charCodeAt(i), 16777619);
  return h >>> 0;
}
