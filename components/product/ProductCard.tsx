import Link from "next/link";
import Image from "next/image";
import type { Product } from "@/lib/types";
import { getCategory } from "@/lib/data/categories";
import { listingPrice, minOrderLabel, toTitleCase } from "@/lib/utils";
import { Badge } from "@/components/ui/Badge";
import { AddButton, WishButton } from "@/components/product/ProductCardActions";

export function ProductCard({ product }: { product: Product }) {
  const category = getCategory(product.categorySlug);
  const price = listingPrice(product);
  const displayName = product.name;

  return (
    <article className="group flex h-full flex-col overflow-hidden rounded-[1.4rem] bg-white shadow-soft ring-1 ring-cream-200 transition duration-300 hover:shadow-lift hover:ring-coral-200 motion-safe:hover:-translate-y-1">
      <div className="relative overflow-hidden bg-white">
        <Link
          href={`/product/${product.slug}`}
          className="relative block aspect-square overflow-hidden bg-white"
        >
          <Image
            src={product.images[0]}
            alt={product.name}
            fill
            sizes="(min-width: 1280px) 200px, (min-width: 768px) 22vw, 50vw"
            quality={70}
            loading="lazy"
            decoding="async"
            className="object-contain object-center bg-white p-1 product-shot sm:p-1.5"
          />
        </Link>
        <div className="absolute left-2 top-2 z-10 flex flex-col gap-1">
          {product.isNew ? <Badge>New</Badge> : null}
        </div>
        <span className="absolute bottom-2 left-2 z-10 rounded-md bg-ink-900/90 px-2 py-1 font-display text-[10px] font-black uppercase tracking-wide text-white">
          {price.badge}
        </span>
        <WishButton slug={product.slug} />
      </div>
      <div className="flex flex-1 flex-col gap-1.5 px-3 py-3">
        <p className="text-[10px] font-bold uppercase tracking-wide text-teal-700">
          {category?.shortName ?? product.categorySlug}
        </p>
        <h3 className="font-display text-sm font-bold leading-snug text-ink-800 sm:text-base">
          <Link href={`/product/${product.slug}`} className="line-clamp-3 hover:text-coral-500">
            {toTitleCase(displayName)}
          </Link>
        </h3>
        <p className="w-fit max-w-full rounded-full bg-teal-50 px-2 py-0.5 text-[11px] font-bold leading-snug text-teal-800">
          {minOrderLabel(product)}
        </p>
        <div className="mt-auto flex items-end justify-between gap-2 border-t border-cream-200 pt-2">
          <span className="text-[11px] font-bold uppercase tracking-wide text-ink-400">{price.label}</span>
          <span className="font-display text-xl font-bold text-coral-500">{price.text}</span>
        </div>
        <AddButton slug={product.slug} ask={price.ask} label={price.ask ? "Ask for price" : price.label === "Box price" && product.piecesPerBox && product.piecesPerBox > 1 ? "Add box" : "Add"} />
      </div>
    </article>
  );
}

