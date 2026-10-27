import { getBestSellers } from "@/lib/data/products";
import { Container } from "@/components/ui/Container";
import { Section } from "@/components/ui/Section";
import { ProductGrid } from "@/components/product/ProductGrid";
import { GlowHeading } from "@/components/home/GlowHeading";
import { Button } from "@/components/ui/Button";

export function TrendingShowcase() {
  const bestsellers = getBestSellers().slice(0, 8);

  return (
    <Section id="trending" className="bg-sky-50 py-6">
      <Container>
        <div className="mb-5 flex flex-col items-start justify-between gap-3 sm:flex-row sm:items-end">
          <GlowHeading eyebrow="Trending" title="What’s flying out" tone="sky" />
          <Button href="/shop" variant="outline" size="sm">
            Shop all
          </Button>
        </div>
        <ProductGrid products={bestsellers} />
      </Container>
    </Section>
  );
}
