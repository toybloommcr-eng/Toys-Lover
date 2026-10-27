import type { Metadata } from "next";
import Link from "next/link";
import { AGE_GUIDES } from "@/lib/data/ages";
import { categories } from "@/lib/data/categories";
import { getProductsByCategory } from "@/lib/data/products";
import { toTitleCase } from "@/lib/utils";
import { Container } from "@/components/ui/Container";
import { Section } from "@/components/ui/Section";
import { GlowHeading } from "@/components/home/GlowHeading";
import { PageHero } from "@/components/ui/PageHero";
import { img } from "@/lib/media";

type Props = { params: { slug: string } };

export function generateStaticParams() {
  return AGE_GUIDES.map((guide) => ({ slug: guide.slug }));
}

export function generateMetadata(): Metadata {
  return {
    title: "Shop by Category",
    description: "Age aisles have been replaced. Browse every category and its products.",
    robots: { index: false, follow: true },
  };
}

/** Age browsing removed — show every category instead. */
export default function AgePage(_props: Props) {
  return (
    <>
      <PageHero
        image={img.pageShop}
        eyebrow="Categories only"
        title="Age filters removed."
        description="Browse by category instead. Every aisle is listed below with its products."
      />
      <Section>
        <Container>
          <GlowHeading title="All Categories" href="/shop#all-categories" />
          <div className="mt-8 flex flex-wrap justify-center gap-2">
            {categories.map((category) => {
              const count = getProductsByCategory(category.slug).length;
              return (
                <Link
                  key={category.slug}
                  href={`/shop/${category.slug}`}
                  className="rounded-full border border-cream-300 bg-white px-3 py-1.5 font-display text-xs font-bold text-ink-700 shadow-soft transition hover:border-coral-300 hover:text-coral-600"
                >
                  {toTitleCase(category.shortName)}
                  <span className="ml-1.5 text-ink-400">({count})</span>
                </Link>
              );
            })}
          </div>
          <p className="mt-8 text-center">
            <Link
              href="/shop#all-categories"
              className="font-display text-sm font-black uppercase tracking-wide text-coral-600 hover:text-coral-700"
            >
              Open full category shop →
            </Link>
          </p>
        </Container>
      </Section>
    </>
  );
}
