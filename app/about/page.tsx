import type { Metadata } from "next";
import { SITE_NAME } from "@/lib/constants";
import { gallery, team, timeline, values } from "@/lib/data/about";
import { img } from "@/lib/media";
import { toTitleCase } from "@/lib/utils";
import { Container } from "@/components/ui/Container";
import { Section } from "@/components/ui/Section";
import { FadeIn } from "@/components/motion/FadeIn";
import { PageHero } from "@/components/ui/PageHero";
import { SafeImage } from "@/components/ui/SafeImage";

export const metadata: Metadata = {
  title: "Who We Are",
};

export default function AboutPage() {
  return (
    <>
      <PageHero
        image={img.pageAbout}
        eyebrow="Who We Are"
        title={`${SITE_NAME} — a UK shop built around play, not noise.`}
        description="Manchester arcade counter. Honest ages. Toys we would give our own kids."
      />

      <Section className="pt-10">
        <Container>
          <div className="grid grid-cols-2 gap-3 md:grid-cols-3">
            {gallery.map((shot, index) => (
              <FadeIn key={shot.src} delay={index * 0.04}>
                <div className="media-hover media-hover-frame relative aspect-square overflow-hidden rounded-3xl bg-white shadow-soft">
                  <SafeImage
                    src={shot.src}
                    alt={shot.alt}
                    fill
                    sizes="(min-width: 768px) 33vw, 50vw"
                    className={
                      shot.src.includes("/products/")
                        ? "object-contain p-4"
                        : "object-cover object-center"
                    }
                  />
                </div>
              </FadeIn>
            ))}
          </div>
        </Container>
      </Section>

      <Section tone="white" className="py-12">
        <Container>
          <div className="grid gap-4 md:grid-cols-3">
            {values.map((value) => (
              <article key={value.title} className="media-hover overflow-hidden rounded-3xl shadow-card">
                <div className="media-hover-frame relative aspect-[4/3]">
                  <SafeImage
                    src={value.image}
                    alt={value.title}
                    fill
                    quality={72}
                    className={
                      value.image.includes("/products/") || value.image.includes("/categories/")
                        ? "object-contain bg-white p-4"
                        : "object-cover"
                    }
                    sizes="33vw"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-ink-900/70 to-transparent" />
                  <h2 className="heading-glow-light absolute bottom-4 left-4 font-display text-2xl font-extrabold text-white">
                    {toTitleCase(value.title)}
                  </h2>
                </div>
              </article>
            ))}
          </div>
        </Container>
      </Section>

      <Section className="py-12">
        <Container>
          <h2 className="heading-glow mb-6 font-display text-3xl font-extrabold text-ink-900">Our Story, In Frames</h2>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {timeline.map((item) => (
              <article key={item.year} className="media-hover overflow-hidden rounded-3xl bg-white shadow-soft">
                <div className="media-hover-frame relative aspect-[4/3]">
                  <SafeImage src={item.image} alt={item.title} fill className="object-cover" sizes="25vw" />
                </div>
                <div className="p-4">
                  <p className="text-xs font-display font-extrabold text-coral-600">{item.year}</p>
                  <h3 className="heading-glow-soft font-display text-lg font-extrabold text-ink-900">
                    {toTitleCase(item.title)}
                  </h3>
                </div>
              </article>
            ))}
          </div>
        </Container>
      </Section>

      <Section tone="white" className="py-12">
        <Container>
          <h2 className="heading-glow mb-6 font-display text-3xl font-extrabold text-ink-900">The Faces</h2>
          <div className="grid gap-5 md:grid-cols-3">
            {team.map((member) => (
              <article key={member.name} className="media-hover overflow-hidden rounded-3xl shadow-card">
                <div className="media-hover-frame relative aspect-[3/4]">
                  <SafeImage src={member.image} alt={member.name} fill className="object-cover" sizes="33vw" />
                  <div className="absolute inset-x-0 bottom-0 bg-gradient-to-t from-ink-900 to-transparent p-5 text-white">
                    <h3 className="heading-glow-light font-display text-xl font-extrabold">
                      {member.name}
                    </h3>
                    <p className="text-sm font-bold text-sun-200">{member.role}</p>
                  </div>
                </div>
              </article>
            ))}
          </div>
        </Container>
      </Section>
    </>
  );
}
