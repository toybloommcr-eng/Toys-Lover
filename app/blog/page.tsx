import type { Metadata } from "next";
import Link from "next/link";
import { ArrowUpRight } from "lucide-react";
import { getFeaturedPost, posts } from "@/lib/data/blog";
import { formatDate, toTitleCase } from "@/lib/utils";
import { img } from "@/lib/media";
import { PageHero } from "@/components/ui/PageHero";
import { Container } from "@/components/ui/Container";
import { Section } from "@/components/ui/Section";
import { Badge } from "@/components/ui/Badge";
import { SafeImage } from "@/components/ui/SafeImage";

export const metadata: Metadata = {
  title: "Blog",
};

export default function BlogPage() {
  const featured = getFeaturedPost();
  const rest = posts.filter((post) => post.slug !== featured.slug);
  const featuredStudio = featured.image.includes("/products/");

  return (
    <>
      <PageHero
        image={img.pageBlog}
        eyebrow="Journal"
        title="Notes for parents who want play to feel wiser, not louder."
        description="Gift guides, safety explainers, and rainy-day ideas from the Toy Bloom team."
      />
      <Section>
        <Container>
          <Link
            href={`/blog/${featured.slug}`}
            className="blog-card group relative grid overflow-hidden rounded-4xl border border-coral-100 bg-white shadow-card lg:grid-cols-2"
          >
            <div className="blog-card-media relative min-h-[280px] overflow-hidden bg-white">
              <SafeImage
                src={featured.image}
                alt={featured.title}
                fill
                quality={72}
                className={
                  featuredStudio
                    ? "object-contain p-8"
                    : "object-cover object-center"
                }
                sizes="(min-width: 1024px) 50vw, 100vw"
                priority
              />
              <span className="blog-shine" />
              <span className="blog-read absolute bottom-5 left-5 z-10 inline-flex items-center gap-2 rounded-full bg-white/95 px-4 py-2 font-display text-xs font-black uppercase tracking-wide text-coral-600 shadow-soft">
                Read story
                <ArrowUpRight className="h-3.5 w-3.5" />
              </span>
            </div>
            <div className="relative flex flex-col justify-center p-8">
              <Badge>Featured · {featured.category}</Badge>
              <h2 className="blog-underline heading-glow mt-3 w-fit font-display text-xl font-extrabold leading-snug text-ink-900 sm:text-2xl">
                {toTitleCase(featured.title)}
              </h2>
              <p className="mt-3 text-ink-500">{featured.excerpt}</p>
              <p className="mt-4 text-sm text-ink-400">
                {formatDate(featured.date)} · {featured.readTime} · {featured.author}
              </p>
              <span className="mt-6 inline-flex items-center gap-2 font-display text-sm font-black uppercase tracking-wide text-coral-600">
                Open article
                <ArrowUpRight className="h-4 w-4 transition-transform duration-300 group-hover:-translate-y-0.5 group-hover:translate-x-0.5" />
              </span>
            </div>
          </Link>

          <div className="mt-12 grid gap-6 md:grid-cols-2 xl:grid-cols-3">
            {rest.map((post) => {
              const studio = post.image.includes("/products/");
              return (
                <Link
                  key={post.slug}
                  href={`/blog/${post.slug}`}
                  className="blog-card group flex h-full flex-col overflow-hidden rounded-3xl border border-ink-100 bg-white shadow-soft"
                >
                  <div className="blog-card-media relative aspect-[16/10] overflow-hidden bg-white">
                    <SafeImage
                      src={post.image}
                      alt={post.title}
                      fill
                      quality={72}
                      className={studio ? "object-contain p-5" : "object-cover object-center"}
                      sizes="(min-width: 1280px) 33vw, 50vw"
                    />
                    <span className="blog-shine" />
                    <span className="blog-read absolute bottom-3 left-3 z-10 inline-flex items-center gap-1.5 rounded-full bg-white px-3 py-1.5 font-display text-[10px] font-black uppercase tracking-wide text-coral-600 shadow-soft">
                      Read
                      <ArrowUpRight className="h-3 w-3" />
                    </span>
                  </div>
                  <div className="flex flex-1 flex-col p-5">
                    <p className="text-xs font-bold uppercase tracking-wider text-coral-600">
                      {post.category}
                    </p>
                    <h3 className="blog-underline heading-glow-soft mt-2 w-fit font-display text-base font-extrabold leading-snug text-ink-900 sm:text-lg">
                      {toTitleCase(post.title)}
                    </h3>
                    <p className="mt-2 flex-1 text-sm text-ink-500">{post.excerpt}</p>
                    <p className="mt-4 flex items-center justify-between text-xs text-ink-400">
                      <span>
                        {formatDate(post.date)} · {post.readTime}
                      </span>
                      <span className="inline-flex items-center gap-1 font-display text-[11px] font-black uppercase tracking-wide text-coral-500">
                        Article
                        <ArrowUpRight className="h-3.5 w-3.5 transition-transform duration-300 group-hover:-translate-y-0.5 group-hover:translate-x-0.5" />
                      </span>
                    </p>
                  </div>
                </Link>
              );
            })}
          </div>
        </Container>
      </Section>
    </>
  );
}
