import { categories } from "@/lib/data/categories";
import { getProductsByCategory } from "@/lib/data/products";
import { Container } from "@/components/ui/Container";
import { Section } from "@/components/ui/Section";
import { GlowHeading } from "@/components/home/GlowHeading";
import { CategoryTilesClient } from "@/components/home/CategoryTilesClient";

export function CategoryTiles({
  title = "Shop by Category",
  eyebrow = "Every aisle",
}: {
  title?: string;
  eyebrow?: string;
}) {
  const aisles = categories
    .filter((category) => !category.parentSlug)
    .map((category) => {
      const products = getProductsByCategory(category.slug);
      return {
        category,
        count: products.length,
        productNames: products.slice(0, 2).map((product) => product.name),
      };
    })
    .filter((row) => row.count > 0)
    .sort((a, b) => {
      if (a.category.slug === "squishies") return -1;
      if (b.category.slug === "squishies") return 1;
      return a.category.shortName.localeCompare(b.category.shortName);
    });

  return (
    <Section id="all-categories" className="content-visibility-auto scroll-mt-28 bg-cream-50 py-12">
      <Container>
        <div className="mb-8">
          <GlowHeading eyebrow={eyebrow} title={title} href="/shop" />
          <p className="mx-auto mt-3 max-w-xl text-center text-sm text-ink-500">
            Explore every category — one clear pack shot per aisle, {aisles.length} ways to shop.
          </p>
        </div>
        <CategoryTilesClient aisles={aisles} showAll />
      </Container>
    </Section>
  );
}
