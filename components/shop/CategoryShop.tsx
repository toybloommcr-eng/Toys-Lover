"use client";

import { useMemo, useState } from "react";
import type { Category, Product } from "@/lib/types";
import { SORT_OPTIONS } from "@/lib/constants";
import { Select } from "@/components/ui/Input";
import { ProductGrid } from "@/components/product/ProductGrid";
import { rankProducts } from "@/lib/rank";

export function CategoryShop({
  category,
  products,
}: {
  category: Category;
  products: Product[];
}) {
  const [sort, setSort] = useState("popularity");

  const sorted = useMemo(() => {
    const next = [...products];
    if (sort === "price-asc") {
      next.sort(
        (a, b) =>
          (a.priceTBC ? Number.POSITIVE_INFINITY : a.price) - (b.priceTBC ? Number.POSITIVE_INFINITY : b.price),
      );
      return next;
    }
    if (sort === "price-desc") {
      next.sort(
        (a, b) =>
          (b.priceTBC ? Number.NEGATIVE_INFINITY : b.price) - (a.priceTBC ? Number.NEGATIVE_INFINITY : a.price),
      );
      return next;
    }
    if (sort === "newest") {
      next.sort((a, b) => Number(b.isNew) - Number(a.isNew) || a.name.localeCompare(b.name));
      return next;
    }
    return rankProducts(next);
  }, [products, sort]);

  return (
    <div>
      <div className="mb-6 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <p className="text-sm text-ink-500">
          {sorted.length} {sorted.length === 1 ? "product" : "products"} in {category.shortName}
        </p>
        <div className="sm:w-64">
          <Select label="Sort" value={sort} onChange={(event) => setSort(event.target.value)}>
            {SORT_OPTIONS.map((option) => (
              <option key={option.id} value={option.id}>
                {option.label}
              </option>
            ))}
          </Select>
        </div>
      </div>
      <ProductGrid products={sorted} compact wide />
    </div>
  );
}
