"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import Image from "next/image";
import Link from "next/link";
import { Check, ChevronLeft, ChevronRight, ShoppingBag } from "lucide-react";
import type { Product } from "@/lib/types";
import { getCategory } from "@/lib/data/categories";
import { listingPrice, toTitleCase } from "@/lib/utils";
import { WishButton } from "@/components/product/ProductCardActions";
import { useCart } from "@/lib/context/CartContext";

function AddToCartButton({ slug, ask = false }: { slug: string; ask?: boolean }) {
  const { addItem } = useCart();
  const [added, setAdded] = useState(false);

  if (ask) {
    return (
      <Link
        href="/contact/"
        className="mt-3 inline-flex w-full items-center justify-center gap-2 rounded-full bg-coral-500 py-2.5 font-display text-sm font-bold text-white shadow-soft hover:bg-coral-600"
      >
        Ask for price
      </Link>
    );
  }

  return (
    <button
      type="button"
      onClick={() => {
        addItem(slug);
        setAdded(true);
        window.setTimeout(() => setAdded(false), 1400);
      }}
      className={`cart-pulse mt-3 inline-flex w-full items-center justify-center gap-2 rounded-full py-2.5 font-display text-sm font-bold text-white shadow-soft transition-[background-color,transform] duration-300 ease-out ${
        added ? "bg-teal-600" : "bg-coral-500 hover:bg-coral-600"
      }`}
    >
      {added ? <Check className="cart-icon h-4 w-4" /> : <ShoppingBag className="cart-icon h-4 w-4" />}
      {added ? "Added" : "Add box"}
    </button>
  );
}

function BestSellerCard({ product, index }: { product: Product; index: number }) {
  const category = getCategory(product.categorySlug);
  const price = listingPrice(product);
  const badge = product.isNew ? "New" : product.isBestSeller ? "Bestseller" : product.compareAtPrice ? "Sale" : null;
  const badgeClass = product.isNew
    ? "bg-teal-600 text-white"
    : product.isBestSeller
      ? "bg-sun-400 text-ink-800"
      : "bg-coral-500 text-white";
  // Horizontal carousel keeps most cards off-screen — Next/Image defaults to lazy,
  // so off-screen slides stay blank until the strip is scrolled. Force eager.
  const priority = index < 3;

  return (
    <article className="bestseller-card flex h-full flex-col overflow-hidden rounded-[1.6rem] bg-white ring-1 ring-cream-200 transition hover:-translate-y-0.5 hover:shadow-soft">
      <div className="relative">
        <Link
          href={`/product/${product.slug}`}
          className="relative block aspect-square overflow-hidden bg-white"
        >
          <Image
            src={product.images[0]}
            alt={product.name}
            fill
            sizes="(min-width: 1280px) 212px, (min-width: 640px) 36vw, 70vw"
            quality={78}
            priority={priority}
            loading="eager"
            decoding="async"
            className="object-contain object-center bg-white p-0.5 bestseller-photo product-shot sm:p-1"
          />
        </Link>
        {badge ? (
          <span
            className={`absolute left-3 top-3 z-10 rounded-full px-2.5 py-1 font-display text-[10px] font-bold uppercase tracking-wide ${badgeClass}`}
          >
            {badge}
          </span>
        ) : null}
        <span className="absolute bottom-2 left-2 z-10 rounded-md bg-ink-900/90 px-2 py-1 font-display text-[10px] font-black uppercase tracking-wide text-white">
          {price.badge}
        </span>
        <WishButton slug={product.slug} />
      </div>
      <div className="flex flex-1 flex-col px-3 pb-3 pt-2.5">
        <p className="text-[10px] font-bold uppercase tracking-[0.14em] text-teal-700">
          {category?.shortName ?? product.categorySlug}
        </p>
        <h3 className="mt-1 font-display text-sm font-bold leading-snug text-ink-800">
          <Link href={`/product/${product.slug}`} className="transition-colors duration-200 hover:text-coral-500">
            {toTitleCase(product.name)}
          </Link>
        </h3>
        <div className="mt-auto flex items-end justify-between gap-2 border-t border-cream-200 pt-2">
          <span className="text-[11px] font-semibold text-ink-500">{price.label}</span>
          <span className="font-display text-base font-bold text-coral-500">{price.text}</span>
        </div>
        <AddToCartButton slug={product.slug} ask={price.ask} />
      </div>
    </article>
  );
}

export function BestSellers({ products }: { products: Product[] }) {
  const scroller = useRef<HTMLDivElement>(null);
  const [paused, setPaused] = useState(false);
  const [active, setActive] = useState(0);
  const count = products.length;

  const scrollByCard = useCallback((direction: -1 | 1) => {
    const node = scroller.current;
    if (!node) return;
    const card = node.querySelector<HTMLElement>("[data-bestseller-card]");
    const step = card ? card.offsetWidth + 12 : Math.min(node.clientWidth * 0.75, 280);
    node.scrollBy({ left: direction * step, behavior: "smooth" });
  }, []);

  const syncActive = useCallback(() => {
    const node = scroller.current;
    if (!node || count === 0) return;
    const card = node.querySelector<HTMLElement>("[data-bestseller-card]");
    const step = card ? card.offsetWidth + 12 : 240;
    const index = Math.round(node.scrollLeft / step);
    setActive(Math.max(0, Math.min(count - 1, index)));
  }, [count]);

  useEffect(() => {
    const node = scroller.current;
    if (!node) return;
    node.addEventListener("scroll", syncActive, { passive: true });
    syncActive();
    return () => node.removeEventListener("scroll", syncActive);
  }, [syncActive]);

  useEffect(() => {
    if (paused || count < 2) return;
    const reduced =
      typeof window !== "undefined" &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduced) return;

    const id = window.setInterval(() => {
      const node = scroller.current;
      if (!node) return;
      const card = node.querySelector<HTMLElement>("[data-bestseller-card]");
      const step = card ? card.offsetWidth + 12 : 240;
      const atEnd = node.scrollLeft + node.clientWidth >= node.scrollWidth - 8;
      if (atEnd) {
        node.scrollTo({ left: 0, behavior: "smooth" });
      } else {
        node.scrollBy({ left: step, behavior: "smooth" });
      }
    }, 3800);

    return () => window.clearInterval(id);
  }, [paused, count]);

  if (count === 0) return null;

  return (
    <div
      className="relative"
      onMouseEnter={() => setPaused(true)}
      onMouseLeave={() => setPaused(false)}
      onFocusCapture={() => setPaused(true)}
      onBlurCapture={(event) => {
        if (!event.currentTarget.contains(event.relatedTarget as Node | null)) {
          setPaused(false);
        }
      }}
    >
      <button
        type="button"
        aria-label="Previous bestsellers"
        onClick={() => scrollByCard(-1)}
        className="absolute -left-2 top-[38%] z-10 grid h-11 w-11 place-items-center rounded-full bg-white text-coral-500 shadow-card ring-1 ring-cream-200 transition hover:bg-cream-50 hover:text-coral-600 sm:-left-3 sm:h-12 sm:w-12"
      >
        <ChevronLeft className="h-5 w-5 sm:h-6 sm:w-6" />
      </button>

      <div
        ref={scroller}
        className="no-scrollbar flex snap-x snap-mandatory gap-3 overflow-x-auto scroll-smooth px-1 pb-3"
        role="region"
        aria-roledescription="carousel"
        aria-label="Best sellers"
      >
        {products.map((product, index) => (
          <div
            key={product.slug}
            data-bestseller-card
            className="w-[72%] shrink-0 snap-start sm:w-[44%] md:w-[32%] lg:w-[24%] xl:w-[19%]"
          >
            <BestSellerCard product={product} index={index} />
          </div>
        ))}
      </div>

      <button
        type="button"
        aria-label="Next bestsellers"
        onClick={() => scrollByCard(1)}
        className="absolute -right-2 top-[38%] z-10 grid h-11 w-11 place-items-center rounded-full bg-white text-coral-500 shadow-card ring-1 ring-cream-200 transition hover:bg-cream-50 hover:text-coral-600 sm:-right-3 sm:h-12 sm:w-12"
      >
        <ChevronRight className="h-5 w-5 sm:h-6 sm:w-6" />
      </button>

      <div className="mt-5 flex items-center justify-center gap-1.5">
        {products.map((product, index) => (
          <button
            key={product.slug}
            type="button"
            aria-label={`Show ${product.name}`}
            aria-current={index === active ? "true" : undefined}
            onClick={() => {
              const node = scroller.current;
              const card = node?.querySelectorAll<HTMLElement>("[data-bestseller-card]")[index];
              card?.scrollIntoView({ behavior: "smooth", inline: "start", block: "nearest" });
            }}
            className={`h-2 rounded-full transition-all duration-300 ease-out ${
              index === active ? "w-6 bg-coral-500" : "w-2 bg-cream-300 hover:bg-cream-400"
            }`}
          />
        ))}
      </div>
    </div>
  );
}
