import type { Metadata } from "next";
import { SITE_NAME } from "@/lib/constants";
import { img } from "@/lib/media";
import { PageHero } from "@/components/ui/PageHero";
import { Container } from "@/components/ui/Container";
import { Section } from "@/components/ui/Section";

export const metadata: Metadata = {
  title: "Shipping & Returns",
};

export default function ShippingPage() {
  return (
    <>
      <PageHero
        image={img.pageShop}
        eyebrow="Policies"
        title="Shipping & returns, written in plain language."
        description={`${SITE_NAME} packs from Manchester, United Kingdom. Here is exactly what happens after you click “place order.”`}
      />
      <Section>
        <Container className="prose-custom max-w-3xl space-y-8 text-ink-600">
          <section>
            <h2 className="heading-glow font-display text-2xl font-extrabold text-ink-900">Shipping</h2>
            <p className="mt-3 leading-relaxed">
              Most UK orders leave within one working day. Delivery across the United Kingdom is
              typically 1–3 working days. You will receive a tracking note. Free standard shipping
              applies over £60; a flat UK fee applies below that.
            </p>
            <p className="mt-3 leading-relaxed">
              Local pickup is available at our Manchester shop. We will email when the bag is ready.
            </p>
          </section>
          <section>
            <h2 className="heading-glow font-display text-2xl font-extrabold text-ink-900">Returns</h2>
            <p className="mt-3 leading-relaxed">
              Unused items in original packaging can be returned within 14 days of delivery. Toys
              that have been played with cannot be restocked for hygiene and safety — except when
              we sent the wrong item or something arrived damaged.
            </p>
          </section>
          <section>
            <h2 className="heading-glow font-display text-2xl font-extrabold text-ink-900">Gifts</h2>
            <p className="mt-3 leading-relaxed">
              We can hide prices on packing slips and add a short note. Tell us in checkout
              comments so the surprise stays intact.
            </p>
          </section>
        </Container>
      </Section>
    </>
  );
}
