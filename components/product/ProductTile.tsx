import Link from "next/link";
import Image from "next/image";
import type { Product } from "@/lib/types";
import { listingPrice, minOrderLabel, toTitleCase } from "@/lib/utils";
import { WishButton } from "@/components/product/ProductCardActions";

export function ProductTile({ product }: { product: Product }) {
  const price = listingPrice(product);

  return (
    <article className="group flex h-full flex-col overflow-hidden rounded-[1.5rem] bg-white shadow-soft ring-1 ring-cream-200 transition duration-300 hover:-translate-y-0.5 hover:shadow-card">
      <div className="relative">
        <Link
          href={`/product/${product.slug}`}
          className="relative block aspect-square overflow-hidden bg-white"
        >
          <Image
            src={product.images[0]}
            alt={product.name}
            fill
            sizes="(min-width: 1280px) 200px, (min-width: 640px) 22vw, 50vw"
            quality={70}
            loading="lazy"
            decoding="async"
            className="object-contain object-center bg-white p-1 product-shot sm:p-1.5"
          />
        </Link>
        <span className="absolute bottom-2 left-2 z-10 rounded-md bg-ink-900/90 px-2 py-1 font-display text-[10px] font-black uppercase tracking-wide text-white">
          {price.badge}
        </span>
        <WishButton slug={product.slug} />
      </div>
      <div className="flex flex-1 flex-col px-3 pb-3 pt-2.5">
        <h3 className="font-display text-sm font-bold leading-snug text-ink-800">
          <Link href={`/product/${product.slug}`} className="line-clamp-3 break-words hover:text-coral-500">
            {toTitleCase(product.name)}
          </Link>
        </h3>
        <p className="mt-1 line-clamp-2 break-words text-[11px] font-bold leading-snug text-teal-800">
          {minOrderLabel(product)}
        </p>
        <div className="mt-auto flex items-end justify-between gap-2 border-t border-cream-200 pt-2">
          <span className="text-[11px] font-semibold text-ink-500">{price.label}</span>
          <span className="font-display text-base font-bold text-coral-500">{price.text}</span>
        </div>
      </div>
    </article>
  );
}
