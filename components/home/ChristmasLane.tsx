"use client";

import { useEffect, useState } from "react";
import { Gift } from "lucide-react";
import type { Product } from "@/lib/types";
import { isChristmasSeason } from "@/lib/christmas";
import { Container } from "@/components/ui/Container";
import { GlowHeading } from "@/components/home/GlowHeading";
import { ProductGrid } from "@/components/product/ProductGrid";
import { Button } from "@/components/ui/Button";

export function ChristmasLane({ products }: { products: Product[] }) {
  const [on, setOn] = useState(false);
  useEffect(() => setOn(isChristmasSeason()), []);
  if (!on || products.length === 0) return null;

  return (
    <section className="christmas-lane content-visibility-auto bg-gradient-to-b from-[#FEF2F2] via-[#ECFDF5] to-cream-50 py-10">
      <Container>
        <GlowHeading
          eyebrow="Festive favourites"
          title="Christmas on top."
        />
        <p className="mx-auto mt-2 max-w-2xl text-center text-sm text-ink-600 sm:text-base">
          Christmas squishies and seasonal gifts first — this aisle softens back to normal after Christmas Day.
        </p>
        <div className="mt-8">
          <ProductGrid products={products.slice(0, 12)} />
        </div>
        <div className="mt-6 flex flex-wrap justify-center gap-3">
          <Button href="/shop/christmas-squishies" size="lg">
            <Gift className="h-4 w-4" />
            Shop Christmas squishies
          </Button>
          <Button href="/shop/seasonal" variant="outline" size="lg">
            Seasonal aisle
          </Button>
        </div>
      </Container>
    </section>
  );
}
