import type { Metadata } from "next";
import { SITE_NAME } from "@/lib/constants";
import { img } from "@/lib/media";
import { PageHero } from "@/components/ui/PageHero";
import { Container } from "@/components/ui/Container";
import { Section } from "@/components/ui/Section";

export const metadata: Metadata = {
  title: "Privacy Policy",
};

export default function PrivacyPage() {
  return (
    <>
      <PageHero
        image={img.pageContact}
        eyebrow="Legal"
        title="Privacy Policy"
        description={`How ${SITE_NAME} would treat your information in a live store — this preview keeps data in your browser only.`}
      />
      <Section>
        <Container className="max-w-3xl space-y-6 text-ink-600">
          <p className="leading-relaxed">
            This frontend demo stores cart and wishlist items in your browser’s local storage. We
            do not transmit checkout or contact-form fields to a server.
          </p>
          <h2 className="heading-glow font-display text-2xl font-extrabold text-ink-900">Information We Would Collect</h2>
          <p className="leading-relaxed">
            A production shop would collect name, email, phone, shipping address, and order history
            to fulfill purchases and answer support questions. Payment details would be handled by
            a certified processor — never stored as raw card numbers on our servers.
          </p>
          <h2 className="heading-glow font-display text-2xl font-extrabold text-ink-900">Cookies</h2>
          <p className="leading-relaxed">
            Essential cookies keep a session together. Analytics, if added later, should be
            optional and explained at first visit.
          </p>
          <h2 className="heading-glow font-display text-2xl font-extrabold text-ink-900">Your Rights</h2>
          <p className="leading-relaxed">
            You may request a copy, correction, or deletion of account data by emailing
            hello@toybloom.example. Children do not create accounts — parents shop on their
            behalf.
          </p>
        </Container>
      </Section>
    </>
  );
}
