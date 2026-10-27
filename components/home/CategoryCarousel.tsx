"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { ChevronLeft, ChevronRight } from "lucide-react";
import type { Category } from "@/lib/types";
import { cn } from "@/lib/utils";
import { Container } from "@/components/ui/Container";
import { Section } from "@/components/ui/Section";
import { GlowHeading } from "@/components/home/GlowHeading";
import { AisleCard } from "@/components/shop/AisleCard";

function usePerView() {
  const [perView, setPerView] = useState(1);

  useEffect(() => {
    const apply = () => {
      const width = window.innerWidth;
      setPerView(width >= 1024 ? 3 : width >= 640 ? 2 : 1);
    };
    apply();
    window.addEventListener("resize", apply);
    return () => window.removeEventListener("resize", apply);
  }, []);

  return perView;
}

function chunk<T>(items: T[], size: number) {
  const pages: T[][] = [];
  for (let index = 0; index < items.length; index += size) {
    pages.push(items.slice(index, index + size));
  }
  return pages;
}

export function CategoryCarousel({
  categories,
  counts,
}: {
  categories: Category[];
  counts: Record<string, number>;
}) {
  const topLevel = useMemo(() => categories.filter((category) => !category.parentSlug), [categories]);
  const perView = usePerView();
  const slides = useMemo(() => chunk(topLevel, perView), [topLevel, perView]);
  const pageCount = Math.max(1, slides.length);
  const [page, setPage] = useState(0);
  const [paused, setPaused] = useState(false);
  const [reduceMotion, setReduceMotion] = useState(false);

  useEffect(() => {
    setPage((current) => Math.min(current, pageCount - 1));
  }, [pageCount]);

  useEffect(() => {
    const media = window.matchMedia("(prefers-reduced-motion: reduce)");
    const apply = () => setReduceMotion(media.matches);
    apply();
    media.addEventListener("change", apply);
    return () => media.removeEventListener("change", apply);
  }, []);

  useEffect(() => {
    if (paused || reduceMotion || pageCount < 2) return;
    const timer = window.setInterval(() => {
      setPage((current) => (current + 1) % pageCount);
    }, 8000);
    return () => window.clearInterval(timer);
  }, [paused, reduceMotion, pageCount]);

  const go = (next: number) => {
    setPage(((next % pageCount) + pageCount) % pageCount);
  };

  return (
    <Section className="overflow-hidden bg-coral-50 py-8">
      <Container>
        <div className="mb-5 flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
          <GlowHeading eyebrow={`${topLevel.length} aisles`} title="Find a toy by type" />
          <div className="flex items-center gap-2">
            <Link
              href="/shop"
              className="mr-1 rounded-full bg-white px-4 py-2 font-display text-xs font-black uppercase tracking-wide text-coral-600 ring-1 ring-coral-200"
            >
              All aisles
            </Link>
            <button
              type="button"
              onClick={() => go(page - 1)}
              className="grid h-10 w-10 place-items-center rounded-full bg-white text-ink-800 shadow-soft ring-1 ring-coral-100"
              aria-label="Previous slide"
            >
              <ChevronLeft className="h-5 w-5" />
            </button>
            <button
              type="button"
              onClick={() => go(page + 1)}
              className="grid h-10 w-10 place-items-center rounded-full bg-coral-500 text-white shadow-soft"
              aria-label="Next slide"
            >
              <ChevronRight className="h-5 w-5" />
            </button>
          </div>
        </div>

        <div
          className="relative overflow-hidden rounded-[1.75rem]"
          onMouseEnter={() => setPaused(true)}
          onMouseLeave={() => setPaused(false)}
          onFocusCapture={() => setPaused(true)}
          onBlurCapture={(event) => {
            if (!event.currentTarget.contains(event.relatedTarget as Node | null)) {
              setPaused(false);
            }
          }}
        >
          <div
            className={cn("flex", !reduceMotion && "transition-transform duration-[1200ms] ease-in-out")}
            style={{ transform: `translateX(-${page * 100}%)` }}
          >
            {slides.map((slide, slideIndex) => (
              <div
                key={slide.map((item) => item.slug).join("-")}
                className="grid min-w-full grid-cols-1 gap-4 px-0.5 sm:grid-cols-2 lg:grid-cols-3"
                aria-hidden={slideIndex !== page}
              >
                {slide.map((category, index) => (
                  <AisleCard
                    key={category.slug}
                    category={category}
                    count={counts[category.slug]}
                    priority={slideIndex === 0 && index < 2}
                  />
                ))}
              </div>
            ))}
          </div>
        </div>

        <div className="mt-5 flex flex-wrap items-center justify-center gap-2">
          {slides.map((slide, index) => (
            <button
              key={slide[0]?.slug ?? index}
              type="button"
              onClick={() => go(index)}
              aria-label={`Go to slide ${index + 1}`}
              aria-current={index === page}
              className={cn(
                "h-2.5 rounded-full transition-all duration-300",
                index === page ? "w-8 bg-coral-500" : "w-2.5 bg-coral-200 hover:bg-coral-300",
              )}
            />
          ))}
        </div>
        <p className="mt-3 text-center text-xs font-medium text-ink-400">
          Slides rotate on their own. Hover or tap a card to pause.
        </p>
      </Container>
    </Section>
  );
}
