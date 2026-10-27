import type { Metadata } from "next";
import Link from "next/link";
import { brandCards } from "@/lib/data/brands";
import { toTitleCase } from "@/lib/utils";
import { img } from "@/lib/media";
import { PageHero } from "@/components/ui/PageHero";
import { Container } from "@/components/ui/Container";
import { Section } from "@/components/ui/Section";
import { ToyPhoto } from "@/components/ui/ToyPhoto";

export const metadata: Metadata = {
  title: "Brands",
};

export default function BrandsPage() {
  return (
    <>
      <PageHero
        image={img.heroToys}
        eyebrow="Labels"
        title="Houses we invite onto the shelf."
        description="Makers chosen for finish, spare parts, and how the toy feels after a month of real play."
      />
      <Section>
        <Container>
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {brandCards.map((brand) => (
              <Link
                key={brand.name}
                href={`/shop/${brand.slug}`}
                className="media-hover group overflow-hidden rounded-[1.75rem] bg-white shadow-card"
              >
                <ToyPhoto
                  src={brand.image}
                  alt={`${brand.name} toys`}
                  sizes="(min-width: 1024px) 33vw, 50vw"
                  fit="contain"
                  className="aspect-[4/3]"
                />
                <div className="p-5">
                  <h2 className="heading-glow-soft font-display text-2xl font-extrabold text-sky-700">
                    {toTitleCase(brand.name)}
                  </h2>
                  <p className="mt-2 text-sm font-medium text-ink-500">{brand.blurb}</p>
                </div>
              </Link>
            ))}
          </div>
        </Container>
      </Section>
    </>
  );
}
