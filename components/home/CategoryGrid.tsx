import Link from "next/link";
import { categories } from "@/lib/data/categories";
import { getProductsByCategory } from "@/lib/data/products";
import { toTitleCase } from "@/lib/utils";
import { Container } from "@/components/ui/Container";
import { Section } from "@/components/ui/Section";
import { FadeIn } from "@/components/motion/FadeIn";
import { ToyPhoto } from "@/components/ui/ToyPhoto";

export function CategoryGrid({
  title = "Featured categories",
  limit,
}: {
  title?: string;
  limit?: number;
}) {
  const topLevel = categories.filter((category) => !category.parentSlug);
  const list = limit ? topLevel.slice(0, limit) : topLevel;

  return (
    <Section>
      <Container>
        <FadeIn>
          <div className="mb-10 flex flex-col justify-between gap-3 sm:flex-row sm:items-end">
            <div>
              <p className="text-xs font-display font-bold uppercase tracking-[0.2em] text-coral-600">
                Find their kind of play
              </p>
              <h2 className="heading-glow mt-2 font-display text-3xl font-extrabold text-ink-900 sm:text-4xl">
                {toTitleCase(title)}
              </h2>
            </div>
            <Link href="/shop" className="text-sm font-display font-semibold text-sky-600 hover:text-sky-700">
              Browse all categories
            </Link>
          </div>
        </FadeIn>
        <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {list.map((category, index) => {
            const products = getProductsByCategory(category.slug);
            const names = products.slice(0, 3).map((product) => product.name);
            return (
              <FadeIn key={category.slug} delay={index * 0.04}>
                <Link
                  href={`/shop/${category.slug}`}
                  className="media-hover group relative block overflow-hidden rounded-3xl shadow-soft"
                >
                  <div className="relative aspect-[5/3] bg-white">
                    <ToyPhoto
                      src={category.image}
                      alt={category.name}
                      sizes="(min-width: 1024px) 33vw, 100vw"
                      fit="contain"
                      className="h-full w-full"
                    />
                    <div className="pointer-events-none absolute inset-0 bg-gradient-to-t from-ink-900/75 via-ink-900/15 to-transparent" />
                  </div>
                  <div className="absolute inset-x-0 bottom-0 p-5 text-white">
                    <h3 className="heading-glow-light font-display text-xl font-extrabold">
                      {toTitleCase(category.shortName)}
                    </h3>
                    <p className="mt-1 line-clamp-2 text-sm text-cream-200">{category.description}</p>
                    {names.length ? (
                      <p className="mt-2 line-clamp-2 text-xs font-semibold text-cream-100">
                        {names.map((name) => toTitleCase(name)).join(" Â· ")}
                        {products.length > names.length ? ` Â· +${products.length - names.length} more` : ""}
                      </p>
                    ) : null}
                  </div>
                </Link>
              </FadeIn>
            );
          })}
        </div>
      </Container>
    </Section>
  );
}
