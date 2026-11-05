/**
 * Shop CRM bridge.
 * data/crm/products.json + data/crm/categories.json are written by the Shop CRM admin
 * (via the GitHub Contents API). When they exist and are non-empty they are the single
 * source of truth for the shop; otherwise the legacy TypeScript catalogue is used.
 * To roll back: delete data/crm/*.json (or set them to []).
 */
import type { AgeRange, Category, Product } from "@/lib/types";
import crmProductsJson from "@/data/crm/products.json";
import crmCategoriesJson from "@/data/crm/categories.json";

type CrmProduct = Partial<Product> & {
  id?: string; title?: string; category?: string; active?: boolean; tags?: string[]; sku?: string; costPrice?: number;
  compareAtPrice?: number | null;
};
type CrmCategory = Partial<Category> & { slug: string; name: string };

const AGES: AgeRange[] = ["0-2 years", "3-5 years", "6-8 years", "9-12 years", "13+ years"];
const isMoqLine = (f: string) => /^(minimum order|min order|box of\s*\d+)/i.test(f.trim());
const slugify = (s: string) => s.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "");

export function crmToProduct(p: CrmProduct): Product {
  const moqLabel = p.moqLabel || (p.piecesPerBox ? `Min order: ${p.piecesPerBox} pcs` : undefined);
  const features = (p.features ?? []).filter((f) => !isMoqLine(f) && f !== moqLabel);
  return {
    slug: p.slug || slugify(p.title || p.id || "item"),
    name: p.title || p.name || "Untitled",
    price: Number(p.price) || 0,
    compareAtPrice: p.compareAtPrice ? Number(p.compareAtPrice) : undefined,
    ageRange: AGES.includes(p.ageRange as AgeRange) ? (p.ageRange as AgeRange) : "6-8 years",
    brand: p.brand || p.tags?.[0] || "Toy Bloom",
    theme: p.theme || p.tags?.[1] || "",
    categorySlug: p.category || p.categorySlug || "",
    images: p.images?.length ? p.images : ["/icon.png"],
    shortDescription: p.shortDescription || (p.description || "").slice(0, 140),
    description: p.description || "",
    features: moqLabel ? [moqLabel, ...features] : features,
    safety: p.safety || "",
    materials: p.materials || "",
    isNew: p.isNew,
    isBestSeller: p.isBestSeller,
    piecesPerBox: p.piecesPerBox,
    moqUnit: p.moqUnit,
    moqLabel,
    priceTBC: p.priceTBC ? true : undefined,
    stock: Math.max(0, Number(p.stock) || 0),
  };
}

export function crmToCategory(c: CrmCategory | string): Category {
  const o: CrmCategory = typeof c === "string" ? { slug: slugify(c), name: c } : c;
  return {
    slug: o.slug, name: o.name, shortName: o.shortName || o.name,
    description: o.description || "", longDescription: o.longDescription || o.description || "",
    image: o.image || "/icon.png", accent: o.accent || "sky", ageLabel: o.ageLabel || "All ages",
    ...(o.parentSlug ? { parentSlug: o.parentSlug } : {}),
  };
}

const rawProducts = crmProductsJson as unknown as CrmProduct[];
const rawCategories = crmCategoriesJson as unknown as (CrmCategory | string)[];

/** null = CRM not in use, fall back to legacy catalogue */
export const crmProducts: Product[] | null = rawProducts.length ? rawProducts.filter((p) => p.active !== false).map(crmToProduct) : null;
export const crmCategories: Category[] | null = rawCategories.length ? rawCategories.map(crmToCategory) : null;
