"use client";

import { useRef } from "react";
import { ChevronLeft, ChevronRight } from "lucide-react";
import type { Product } from "@/lib/types";
import { ProductCard } from "@/components/product/ProductCard";

export function ProductCarousel({ products }: { products: Product[] }) {
  const scroller = useRef<HTMLDivElement>(null);

  const scrollByCard = (direction: -1 | 1) => {
    const node = scroller.current;
    if (!node) return;
    node.scrollBy({ left: direction * (node.clientWidth * 0.7), behavior: "smooth" });
  };

  return (
    <div className="relative">
      <div className="mb-4 flex justify-end gap-2">
        <button
          type="button"
          onClick={() => scrollByCard(-1)}
          className="grid h-10 w-10 place-items-center rounded-full border border-ink-200 bg-white text-ink-700 hover:border-coral-300"
          aria-label="Previous products"
        >
          <ChevronLeft className="h-5 w-5" />
        </button>
        <button
          type="button"
          onClick={() => scrollByCard(1)}
          className="grid h-10 w-10 place-items-center rounded-full border border-ink-200 bg-white text-ink-700 hover:border-coral-300"
          aria-label="Next products"
        >
          <ChevronRight className="h-5 w-5" />
        </button>
      </div>
      <div
        ref={scroller}
        className="no-scrollbar flex snap-x snap-mandatory gap-3 overflow-x-auto pb-2"
      >
        {products.slice(0, 8).map((product) => (
          <div key={product.slug} className="w-[70%] shrink-0 snap-start sm:w-[44%] lg:w-[23%]">
            <ProductCard product={product} />
          </div>
        ))}
      </div>
    </div>
  );
}
