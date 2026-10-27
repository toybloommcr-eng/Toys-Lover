"use client";

import Link from "next/link";
import type { Category } from "@/lib/types";
import { AisleCard } from "@/components/shop/AisleCard";

type AislePreview = {
  category: Category;
  count: number;
  productNames: string[];
};

export function CategoryTilesClient({
  aisles,
  showAll = false,
}: {
  aisles: AislePreview[];
  showAll?: boolean;
}) {
  return (
    <>
      <div className="grid grid-cols-2 gap-2.5 sm:grid-cols-3 sm:gap-3 lg:grid-cols-4 xl:grid-cols-5 2xl:grid-cols-6">
        {aisles.map(({ category, count, productNames }, index) => (
          <AisleCard
            key={category.slug}
            category={category}
            count={count}
            productNames={showAll ? [] : productNames}
            priority={index < 4}
          />
        ))}
      </div>

      <div className="mt-8 flex justify-center">
        <Link
          href="/shop"
          className="font-display text-sm font-bold text-coral-600 underline-offset-4 hover:underline"
        >
          Open full shop
        </Link>
      </div>
    </>
  );
}
