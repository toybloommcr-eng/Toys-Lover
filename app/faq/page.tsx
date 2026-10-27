import type { Metadata } from "next";
import { faqGroups, faqs } from "@/lib/data/faqs";
import { img } from "@/lib/media";
import { toTitleCase } from "@/lib/utils";
import { PageHero } from "@/components/ui/PageHero";
import { Container } from "@/components/ui/Container";
import { Section } from "@/components/ui/Section";
import { Accordion } from "@/components/ui/Accordion";

export const metadata: Metadata = {
  title: "FAQ",
};

export default function FaqPage() {
  return (
    <>
      <PageHero
        image={img.heroKids2}
        eyebrow="Help"
        title="Questions parents actually ask."
        description="Shipping, returns, safety, age guidance, and how Pay Now deposits work with Stripe and PayPal."
      />
      <Section>
        <Container className="space-y-12">
          {faqGroups.map((group) => (
            <div key={group}>
              <h2 className="heading-glow mb-4 font-display text-2xl font-extrabold text-ink-900">
                {toTitleCase(group)}
              </h2>
              <Accordion items={faqs.filter((item) => item.group === group)} />
            </div>
          ))}
        </Container>
      </Section>
    </>
  );
}
