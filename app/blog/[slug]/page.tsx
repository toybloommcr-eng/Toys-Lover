import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { getPost, getRelatedPosts, posts } from "@/lib/data/blog";
import { formatDate, toTitleCase } from "@/lib/utils";
import { Container } from "@/components/ui/Container";
import { Section } from "@/components/ui/Section";
import { SafeImage } from "@/components/ui/SafeImage";

type Props = { params: { slug: string } };

export function generateStaticParams() {
  return posts.map((post) => ({ slug: post.slug }));
}

export function generateMetadata({ params }: Props): Metadata {
  const post = getPost(params.slug);
  if (!post) return { title: "Article" };
  return {
    title: post.title,
    description: post.excerpt,
    alternates: { canonical: `/blog/${post.slug}/` },
    openGraph: {
      type: "article",
      title: post.title,
      description: post.excerpt,
      url: `/blog/${post.slug}/`,
      publishedTime: post.date,
      authors: [post.author],
      images: [{ url: post.image, alt: post.title }],
    },
    twitter: {
      card: "summary_large_image",
      title: post.title,
      description: post.excerpt,
      images: [post.image],
    },
  };
}

export default function BlogPostPage({ params }: Props) {
  const post = getPost(params.slug);
  if (!post) notFound();
  const related = getRelatedPosts(post);
  const studioHero = post.image.includes("/products/");

  return (
    <>
      <div className="relative isolate min-h-[46vh] overflow-hidden bg-ink-900 text-white">
        <SafeImage
          src={post.image}
          alt={post.title}
          fill
          quality={65}
          priority
          sizes="100vw"
          className={
            studioHero
              ? "object-contain bg-white p-10"
              : "object-cover object-center opacity-55"
          }
        />
        <div className="absolute inset-0 bg-gradient-to-t from-ink-900 via-ink-900/45 to-ink-900/10" />
        <Container className="relative flex min-h-[46vh] flex-col justify-end pb-12 pt-20">
          <p className="text-xs font-bold uppercase tracking-[0.18em] text-sun-300">{post.category}</p>
          <h1 className="heading-glow-light mt-3 max-w-3xl font-display text-2xl font-extrabold leading-snug sm:text-3xl">
            {toTitleCase(post.title)}
          </h1>
          <p className="mt-4 text-sm text-cream-200">
            {post.author} · {post.authorRole} · {formatDate(post.date)} · {post.readTime}
          </p>
        </Container>
      </div>

      <Section>
        <Container className="grid gap-12 lg:grid-cols-[1fr_16rem]">
          <article className="space-y-5 text-lg leading-relaxed text-ink-600">
            {post.content.map((paragraph) => (
              <p key={paragraph.slice(0, 24)}>{paragraph}</p>
            ))}
          </article>
          <aside>
            <p className="font-display text-sm font-bold uppercase tracking-wider text-ink-400">
              Related Articles
            </p>
            <ul className="mt-4 space-y-4">
              {related.map((item) => (
                <li key={item.slug}>
                  <Link href={`/blog/${item.slug}`} className="blog-card group block overflow-hidden rounded-2xl border border-transparent bg-white">
                    <div className="blog-card-media relative aspect-[16/9] overflow-hidden">
                      <SafeImage
                        src={item.image}
                        alt=""
                        fill
                        sizes="256px"
                        className={
                          item.image.includes("/products/")
                            ? "object-contain bg-white p-2"
                            : "object-cover"
                        }
                      />
                      <span className="blog-shine" />
                    </div>
                    <div className="p-3">
                      <p className="blog-underline heading-glow-soft w-fit font-display font-bold text-ink-800">
                        {toTitleCase(item.title)}
                      </p>
                      <p className="text-xs text-ink-400">{item.readTime}</p>
                    </div>
                  </Link>
                </li>
              ))}
            </ul>
          </aside>
        </Container>
      </Section>
    </>
  );
}
