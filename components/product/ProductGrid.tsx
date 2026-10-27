import type { Product } from "@/lib/types";
import { ProductTile } from "@/components/product/ProductTile";
import { ProductCard } from "@/components/product/ProductCard";

export function ProductGrid({
  products,
  compact = false,
  wide = false,
}: {
  products: Product[];
  compact?: boolean;
  wide?: boolean;
}) {
  if (products.length === 0) {
    return (
      <p className="rounded-3xl border border-dashed border-ink-200 bg-white p-10 text-center text-ink-500">
        No products in this aisle yet.
      </p>
    );
  }

  const Card = compact ? ProductTile : ProductCard;

  return (
    <div
      className={
        wide
          ? "grid grid-cols-2 gap-3 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6"
          : "grid grid-cols-2 gap-2.5 sm:grid-cols-3 sm:gap-3 lg:grid-cols-4 xl:grid-cols-5 2xl:grid-cols-6"
      }
    >
      {products.map((product) => (
        <Card key={product.slug} product={product} />
      ))}
    </div>
  );
}
