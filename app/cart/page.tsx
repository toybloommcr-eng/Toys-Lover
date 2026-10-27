import type { Metadata } from "next";
import { img } from "@/lib/media";
import { PageHero } from "@/components/ui/PageHero";
import { Container } from "@/components/ui/Container";
import { Section } from "@/components/ui/Section";
import { CartView } from "@/components/cart/CartView";

export const metadata: Metadata = {
  title: "Cart",
};

export default function CartPage() {
  return (
    <>
      <PageHero
        image={img.heroToys}
        eyebrow="The bag"
        title="Check the trolley"
        description="Change quantities here. Pay is a separate, locked step — nothing is billed on this screen."
      />
      <Section>
        <Container>
          <CartView />
        </Container>
      </Section>
    </>
  );
}
