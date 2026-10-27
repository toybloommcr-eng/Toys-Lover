import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { categories, getCategory } from "@/lib/data/categories";
import { getProductsByCategory, SQUISHY_CATEGORY_SLUGS } from "@/lib/data/products";
import { toTitleCase } from "@/lib/utils";
import { Container } from "@/components/ui/Container";
import { Section } from "@/components/ui/Section";
import { CategoryShop } from "@/components/shop/CategoryShop";
import { PageHero } from "@/components/ui/PageHero";

type Props = { params: { slug: string } };

export function generateStaticParams() {
  return categories.map((category) => ({ slug: category.slug }));
}

export function generateMetadata({ params }: Props): Metadata {
  const category = getCategory(params.slug);
  return { title: category?.name ?? "Category" };
}

export default function CategoryPage({ params }: Props) {
  const category = getCategory(params.slug);
  if (!category) notFound();

  const products = getProductsByCategory(category.slug);
  const showSquishyPills = category.slug === "squishies" || category.parentSlug === "squishies";

  return (
    <>
      <PageHero
        image={category.image}
        eyebrow={`${products.length} products in this category`}
        title={category.name}
        description={category.longDescription}
      />
      <Section>
        <Container>
          {showSquishyPills ? (
            <div className="mb-6 flex flex-wrap justify-center gap-2">
              <Link
                href="/shop/squishies"
                className={`rounded-full border px-3 py-1.5 font-display text-xs font-bold shadow-soft transition ${
                  category.slug === "squishies"
                    ? "border-[#E85D8C] bg-[#E85D8C] text-white"
                    : "border-[#E85D8C]/30 bg-white text-ink-700 hover:border-[#E85D8C] hover:text-[#E85D8C]"
                }`}
              >
                All
                <span className="ml-1.5 opacity-80">({getProductsByCategory("squishies").length})</span>
              </Link>
              {SQUISHY_CATEGORY_SLUGS.map((slug) => {
                const sub = getCategory(slug);
                const count = getProductsByCategory(slug).length;
                if (!sub || !count) return null;
                const active = category.slug === slug;
                return (
                  <Link
                    key={slug}
                    href={`/shop/${slug}`}
                    className={`rounded-full border px-3 py-1.5 font-display text-xs font-bold shadow-soft transition ${
                      active
                        ? "border-[#E85D8C] bg-[#E85D8C] text-white"
                        : "border-[#E85D8C]/30 bg-white text-ink-700 hover:border-[#E85D8C] hover:text-[#E85D8C]"
                    }`}
                  >
                    {toTitleCase(sub.shortName)}
                    <span className="ml-1.5 opacity-80">({count})</span>
                  </Link>
                );
              })}
            </div>
          ) : null}
          <CategoryShop category={category} products={products} />
        </Container>
      </Section>
    </>
  );
}
