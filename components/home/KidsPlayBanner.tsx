import { ArrowRight, Sparkles } from "lucide-react";
import { img, categoryImage } from "@/lib/media";
import { toTitleCase } from "@/lib/utils";
import { Container } from "@/components/ui/Container";
import { Section } from "@/components/ui/Section";
import { Button } from "@/components/ui/Button";
import { SafeImage } from "@/components/ui/SafeImage";

const moments = [
  { src: img.gardenPlay, label: "Garden Play" },
  { src: categoryImage["outdoor-sports"], label: "Bubble Fun" },
  { src: img.outdoor, label: "Sports Balls" },
];

export function KidsPlayBanner() {
  return (
    <Section className="py-8">
      <Container>
        <div className="overflow-hidden rounded-[2rem] bg-gradient-to-br from-mint-500 via-sky-500 to-coral-400 p-1 shadow-lift">
          <div className="overflow-hidden rounded-[1.85rem] bg-ink-900">
            <div className="relative min-h-[220px] lg:min-h-[320px]">
              <SafeImage
                src={img.gardenPlay}
                alt="Children playing outdoors with a kite, ball, and toys on the grass"
                fill
                sizes="(min-width: 1152px) 1152px, 100vw"
                quality={64}
                className="object-cover object-[center_35%]"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-ink-900/80 via-ink-900/20 to-transparent" />
              <div className="relative z-10 grid gap-6 p-6 lg:grid-cols-[1.1fr_0.9fr] lg:items-end lg:p-10">
                <div className="max-w-lg text-white">
                  <p className="inline-flex items-center gap-2 text-xs font-display font-extrabold uppercase tracking-[0.2em] text-sun-200">
                    <Sparkles className="h-4 w-4" />
                    Weekend Energy
                  </p>
                  <h2 className="mt-3 font-display text-2xl font-extrabold sm:text-4xl">
                    {toTitleCase("Sunshine, kites, and the toy they take outside.")}
                  </h2>
                  <p className="mt-3 text-sm text-cream-100 sm:text-base">
                    A different kind of play than the living-room rug — scooters, balls, and garden
                    games packed from our UK shop.
                  </p>
                  <Button href="/shop/outdoor-sports" size="lg" variant="sun" className="mt-6">
                    Shop Outdoor Toys
                    <ArrowRight className="h-4 w-4" />
                  </Button>
                </div>
                <div className="hidden grid-cols-3 gap-3 sm:grid">
                  {moments.map((moment) => (
                    <div
                      key={moment.label}
                      className="media-hover overflow-hidden rounded-2xl border-2 border-white/40 bg-white/10 shadow-card"
                    >
                      <div className="media-hover-frame relative aspect-[3/4]">
                        <SafeImage
                          src={moment.src}
                          alt={moment.label}
                          fill
                          sizes="20vw"
                          quality={72}
                          className={
                            moment.src.includes("/products/") || moment.src.includes("/categories/")
                              ? "object-contain bg-white p-2"
                              : "object-cover object-center"
                          }
                        />
                      </div>
                      <p className="bg-white/95 px-2 py-1.5 text-center font-display text-[11px] font-extrabold text-ink-800">
                        {moment.label}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </Container>
    </Section>
  );
}
