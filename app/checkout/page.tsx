import type { Metadata } from "next";
import { Suspense } from "react";
import { img } from "@/lib/media";
import { PageHero } from "@/components/ui/PageHero";
import { Container } from "@/components/ui/Container";
import { Section } from "@/components/ui/Section";
import { CheckoutClient } from "@/components/checkout/CheckoutClient";

export const metadata: Metadata = {
  title: "Checkout",
  robots: { index: false, follow: false },
};

export default function CheckoutPage() {
  return (
    <>
      <PageHero
        image={img.pageShop}
        eyebrow="Checkout"
        title="Almost there"
        description="Confirm delivery details. Payment stays with the method you chose — we do not store card numbers."
      />
      <Section>
        <Container>
          <Suspense fallback={<div className="h-64 animate-pulse rounded-3xl bg-cream-100" />}>
            <CheckoutClient />
          </Suspense>
        </Container>
      </Section>
    </>
  );
}
