import type { Metadata } from "next";
import { SITE_NAME } from "@/lib/constants";
import { img } from "@/lib/media";
import { PageHero } from "@/components/ui/PageHero";
import { Container } from "@/components/ui/Container";
import { Section } from "@/components/ui/Section";

export const metadata: Metadata = {
  title: "Terms of Use",
};

export default function TermsPage() {
  return (
    <>
      <PageHero
        image={img.heroToys}
        eyebrow="Legal"
        title="Terms of Use"
        description="A simple template for how this storefront is meant to be used."
      />
      <Section>
        <Container className="max-w-3xl space-y-6 text-ink-600">
          <p className="leading-relaxed">
            By browsing {SITE_NAME}, you agree to use the site for lawful shopping and information.
            Product copy, photos, and prices on this demo are placeholders for design review.
          </p>
          <h2 className="heading-glow font-display text-2xl font-extrabold text-ink-900">Orders</h2>
          <p className="leading-relaxed">
            A live checkout would form a contract when we confirm the order by email. We may cancel
            if an item is mispriced or out of stock, and we will notify you promptly.
          </p>
          <h2 className="heading-glow font-display text-2xl font-extrabold text-ink-900">Intellectual Property</h2>
          <p className="leading-relaxed">
            Branding, layout, original photography, and original text belong to {SITE_NAME}. This
            preview is for design review and is not a live shop.
          </p>
          <h2 className="heading-glow font-display text-2xl font-extrabold text-ink-900">Limitation</h2>
          <p className="leading-relaxed">
            Always follow on-box safety guidance and supervise play as recommended. We are not
            liable for misuse outside those instructions.
          </p>
        </Container>
      </Section>
    </>
  );
}
