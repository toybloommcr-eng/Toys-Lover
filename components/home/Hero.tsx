import { ArrowRight, ShieldCheck, Sparkles } from "lucide-react";
import { img } from "@/lib/media";
import { Button } from "@/components/ui/Button";
import { Container } from "@/components/ui/Container";
import { HeroSlider } from "@/components/home/HeroSlider";

const slides = [
  {
    src: img.homeHero,
    alt: "Toddler playing with wooden blocks, train and stacking rings",
  },
  {
    src: img.heroKids2,
    alt: "Children laughing and playing with colourful toys together",
  },
  {
    src: img.heroKids3,
    alt: "Kids enjoying creative playtime with toys at home",
  },
];

export function Hero() {
  return (
    <section className="relative overflow-hidden bg-gradient-to-br from-cream-100 via-[#FFF5EB] to-[#FFE8F0]">
      <Container className="grid items-center gap-8 py-10 lg:grid-cols-[1fr_1.05fr] lg:gap-10 lg:py-14">
        <div className="relative z-10 max-w-xl">
          <p className="mb-3 font-display text-xs font-black uppercase tracking-[0.18em] text-coral-500">
            Toy Bloom · UK toy shop
          </p>
          <h1 className="heading-glow font-display text-5xl font-extrabold leading-[1.05] tracking-tight text-ink-900 sm:text-6xl lg:text-[4rem]">
            <span className="heading-glow-coral">Toys</span> for every
            <br />
            kind of play.
          </h1>
          <p className="mt-4 max-w-md text-base leading-relaxed text-ink-600 sm:text-lg">
            Squishies, STEM, plush, role play and more — browse every aisle with clear box prices and
            happy UK delivery.
          </p>
          <div className="mt-7 flex flex-wrap gap-3">
            <Button href="/#all-categories" size="lg">
              Shop categories
              <ArrowRight className="h-4 w-4" />
            </Button>
            <Button href="/shop" variant="outline" size="lg">
              Browse shop
            </Button>
          </div>
          <ul className="mt-7 flex flex-wrap gap-x-5 gap-y-2 text-sm font-semibold text-ink-600">
            <li className="inline-flex items-center gap-1.5">
              <Sparkles className="h-4 w-4 text-coral-500" />
              Full category range
            </li>
            <li className="inline-flex items-center gap-1.5">
              <ShieldCheck className="h-4 w-4 text-teal-600" />
              Safe &amp; Non-Toxic
            </li>
          </ul>
        </div>
        <HeroSlider slides={slides} />
      </Container>
    </section>
  );
}
