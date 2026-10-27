import type { Metadata } from "next";
import { getSaleProducts } from "@/lib/data/products";
import { img } from "@/lib/media";
import { Container } from "@/components/ui/Container";
import { Section } from "@/components/ui/Section";
import { ProductGrid } from "@/components/product/ProductGrid";
import { PageHero } from "@/components/ui/PageHero";

export const metadata: Metadata = {
  title: "Sale",
};

export default function SalePage() {
  const deals = getSaleProducts();

  return (
    <>
      <PageHero
        image={img.pageSale}
        eyebrow="Red tickets"
        title="Pounds off. Same safety sheet."
        description="Short-run reductions. Free UK shipping still kicks in over £60."
      />
      <Section>
        <Container>
          <ProductGrid products={deals} compact />
        </Container>
      </Section>
    </>
  );
}
