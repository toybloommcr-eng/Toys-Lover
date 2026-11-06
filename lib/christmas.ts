import type { Product } from "@/lib/types";

/** UK Christmas window: 1 Nov through end of Christmas Day (25 Dec) Europe/London. */
export function isChristmasSeason(now: Date = new Date()): boolean {
  const parts = new Intl.DateTimeFormat("en-GB", {
    timeZone: "Europe/London",
    month: "numeric",
    day: "numeric",
  }).formatToParts(now);
  const month = Number(parts.find((p) => p.type === "month")?.value);
  const day = Number(parts.find((p) => p.type === "day")?.value);
  if (month === 11) return true;
  if (month === 12 && day <= 25) return true;
  return false;
}

const CHRISTMAS_NAME =
  /christmas|xmas|santa|snowman|reindeer|advent|festive|noel|gingerbread|holly|nutcracker|elf\b|merry/i;
const HALLOWEEN_NAME = /halloween|funky.?fright|pumpkin|witch|spook|skeleton|bat\b|ghost/i;

export function isChristmasProduct(
  product: Pick<Product, "categorySlug" | "name" | "slug">,
): boolean {
  const hay = `${product.name} ${product.slug}`;
  if (product.categorySlug === "christmas-squishies") return true;
  if (product.categorySlug === "seasonal") {
    if (HALLOWEEN_NAME.test(hay) && !CHRISTMAS_NAME.test(hay)) return false;
    return CHRISTMAS_NAME.test(hay) || !HALLOWEEN_NAME.test(hay);
  }
  return CHRISTMAS_NAME.test(hay);
}
