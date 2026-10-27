import type { Metadata } from "next";
import { ExternalLink, Mail, MapPin, Navigation, Phone } from "lucide-react";
import { CONTACT, MAPS_EMBED_SRC, MAPS_LINK, SITE_NAME } from "@/lib/constants";
import { img } from "@/lib/media";
import { Container } from "@/components/ui/Container";
import { Section } from "@/components/ui/Section";
import { ContactForm } from "@/components/contact/ContactForm";
import { SocialIcons } from "@/components/ui/SocialIcons";
import { PageHero } from "@/components/ui/PageHero";
import { SafeImage } from "@/components/ui/SafeImage";

export const metadata: Metadata = {
  title: "Contact Us",
};

export default function ContactPage() {
  const query = `${CONTACT.addressLine1}, ${CONTACT.city}`;

  return (
    <>
      <PageHero
        image={img.pageContact}
        eyebrow="The arcade"
        title="Pin the shop. Then say hello."
        description={`We pack from ${query} — drop in, call, or leave a note for the floor team.`}
      />

      <Section className="bg-gradient-to-b from-coral-50 via-sun-50 to-amber-50">
        <Container className="grid gap-8 lg:grid-cols-[1fr_1.05fr]">
          <ContactForm />
          <div className="space-y-4">
            <div className="rounded-[1.6rem] bg-gradient-to-br from-[#E85D8C] via-[#FF8A3D] to-[#FFE566] p-[3px] shadow-[0_0_28px_rgba(232,93,140,0.4)]">
              <div className="overflow-hidden rounded-[1.45rem] bg-white">
                <div className="flex items-start justify-between gap-3 px-4 py-3">
                  <div className="flex items-start gap-2">
                    <MapPin className="mt-0.5 h-5 w-5 text-[#E85D8C]" />
                    <div>
                      <p className="font-display text-sm font-black uppercase tracking-wide text-[#E85D8C]">
                        {SITE_NAME}
                      </p>
                      <p className="text-sm font-semibold text-ink-800">{CONTACT.addressLine1}</p>
                      <p className="text-sm text-ink-500">
                        {CONTACT.city} · {CONTACT.postcode}
                      </p>
                      <p className="text-xs font-bold uppercase tracking-wide text-[#7A4A2B]">
                        {CONTACT.hours}
                      </p>
                    </div>
                  </div>
                  <a
                    href={MAPS_LINK}
                    target="_blank"
                    rel="noreferrer"
                    className="inline-flex items-center gap-1 rounded-full bg-[#E85D8C] px-3 py-1.5 font-display text-[11px] font-black uppercase tracking-wide text-white"
                  >
                    <Navigation className="h-3.5 w-3.5" />
                    Directions
                  </a>
                </div>
                <div className="relative aspect-[16/11] bg-cream-200">
                  <SafeImage
                    src={img.pageContact}
                    alt=""
                    fill
                    sizes="(min-width: 1024px) 45vw, 100vw"
                    quality={72}
                    className="object-cover object-[center_40%]"
                  />
                  <iframe
                    title={`Map of ${CONTACT.addressLine1}, ${CONTACT.city}`}
                    src={MAPS_EMBED_SRC}
                    className="absolute inset-0 h-full w-full border-0"
                    loading="lazy"
                    referrerPolicy="no-referrer-when-downgrade"
                  />
                </div>
                <a
                  href={MAPS_LINK}
                  target="_blank"
                  rel="noreferrer"
                  className="flex items-center justify-center gap-2 py-2.5 text-sm font-extrabold text-[#7A4A2B] hover:text-[#E85D8C]"
                >
                  Open in Google Maps
                  <ExternalLink className="h-4 w-4" />
                </a>
              </div>
            </div>

            <div className="rounded-[1.4rem] bg-gradient-to-r from-[#FFE566] to-[#F7A8BE] p-[3px] shadow-[0_0_18px_rgba(255,193,7,0.45)]">
              <div className="rounded-[1.25rem] bg-white p-4">
                <div className="flex items-center gap-3">
                  <Phone className="h-5 w-5 text-[#F25C38]" />
                  <div>
                    <p className="text-[11px] font-extrabold uppercase tracking-wider text-ink-400">Call the floor</p>
                    <p className="font-display text-base font-extrabold text-ink-900">{CONTACT.phone}</p>
                  </div>
                </div>
                <div className="mt-3 flex items-center gap-3 border-t border-cream-200 pt-3">
                  <Mail className="h-5 w-5 text-[#E85D8C]" />
                  <div>
                    <p className="text-[11px] font-extrabold uppercase tracking-wider text-ink-400">Write the desk</p>
                    <p className="break-all font-display text-base font-extrabold text-ink-900">
                      {CONTACT.email}
                    </p>
                  </div>
                </div>
                <div className="mt-4 border-t border-cream-200 pt-3">
                  <p className="mb-2 text-[11px] font-extrabold uppercase tracking-wider text-ink-400">
                    Channels
                  </p>
                  <SocialIcons size="sm" />
                </div>
              </div>
            </div>
          </div>
        </Container>
      </Section>
    </>
  );
}
