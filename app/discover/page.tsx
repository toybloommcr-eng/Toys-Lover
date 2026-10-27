import type { Metadata } from "next";
import Link from "next/link";
import { getLookbook } from "@/lib/data/products";
import { posts } from "@/lib/data/blog";
import { img, categoryImage } from "@/lib/media";
import { categoryCovers } from "@/lib/data/category-covers";
import { GlowHeading } from "@/components/home/GlowHeading";
import { Container } from "@/components/ui/Container";
import { Section } from "@/components/ui/Section";
import { ProductGrid } from "@/components/product/ProductGrid";
import { PageHero } from "@/components/ui/PageHero";
import { ToyPhoto } from "@/components/ui/ToyPhoto";
import { formatDate, toTitleCase } from "@/lib/utils";

export const metadata: Metadata = {
  title: "Discover",
};

const scenes = [
  {
    src: categoryImage.squishies,
    title: "Squishy lane",
    text: "Every slow-rise, dumpling and butter squishy is in one aisle.",
    href: "/shop/squishies",
  },
  {
    src: categoryCovers["cars-vehicles"] || categoryImage["outdoor-sports"],
    title: "Cars and garden play",
    text: "Die-cast cars, trucks and outdoor toys.",
    href: "/shop/cars-vehicles",
  },
];

export default function DiscoverPage() {
  const lookbook = getLookbook();
  const notes = posts.slice(0, 3);

  return (
    <>
      <PageHero
        image={img.pageDiscover}
        eyebrow="Lookbook"
        title="Open the window. See how they play."
        description="A slower browse than the shop floor — scenes, window pieces, and notes before you wrap."
      />

      <Section className="bg-gradient-to-b from-coral-50 to-white">
        <Container>
          <GlowHeading eyebrow="Scenes" title="Two ways a Saturday starts" tone="pink" />
          <div className="mt-6 grid gap-4 sm:grid-cols-2">
            {scenes.map((scene) => (
              <Link
                key={scene.title}
                href={scene.href}
                className="media-hover group overflow-hidden rounded-[1.6rem] bg-white shadow-soft"
              >
                <ToyPhoto
                  src={scene.src}
                  alt={scene.title}
                  sizes="(min-width: 1024px) 22vw, 50vw"
                  fit="contain"
                  className="aspect-[4/3]"
                />
                <div className="p-4">
                  <h2 className="heading-glow-soft font-display text-lg font-extrabold text-[#E85D8C]">
                    {toTitleCase(scene.title)}
                  </h2>
                  <p className="mt-1 text-sm text-ink-500">{scene.text}</p>
                </div>
              </Link>
            ))}
          </div>
        </Container>
      </Section>

      <Section tone="white">
        <Container>
          <GlowHeading eyebrow="Window" title="Pieces we keep on the glass" tone="brown" />
          <div className="mt-6">
            <ProductGrid products={lookbook} compact />
          </div>
        </Container>
      </Section>

      <Section className="bg-sun-50">
        <Container>
          <GlowHeading eyebrow="Journal" title="Read before you wrap" tone="orange" />
          <div className="mt-6 grid gap-4 md:grid-cols-3">
            {notes.map((post) => (
              <Link
                key={post.slug}
                href={`/blog/${post.slug}`}
                className="blog-card group overflow-hidden rounded-3xl border border-transparent bg-white shadow-soft"
              >
                <div className="blog-card-media relative overflow-hidden">
                  <ToyPhoto
                    src={post.image}
                    alt=""
                    sizes="33vw"
                    quality={40}
                    fit={post.image.includes("/products/") ? "contain" : "cover"}
                    className="aspect-[16/9]"
                  />
                  <span className="blog-shine" />
                </div>
                <div className="p-4">
                  <p className="text-xs font-bold uppercase tracking-wider text-[#C45C26]">
                    {post.category}
                  </p>
                  <h3 className="blog-underline heading-glow-soft mt-1 w-fit font-display text-lg font-extrabold text-ink-900">
                    {toTitleCase(post.title)}
                  </h3>
                  <p className="mt-2 text-sm text-ink-500">{post.excerpt}</p>
                  <p className="mt-3 text-xs text-ink-400">{formatDate(post.date)}</p>
                </div>
              </Link>
            ))}
          </div>
        </Container>
      </Section>
    </>
  );
}
