"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Heart, Minus, Plus } from "lucide-react";
import type { Product } from "@/lib/types";
import { getBoxDeal, isPriceOnRequest, isSquishyCategorySlug, isSquishyEachCategorySlug } from "@/lib/utils";
import { useCart } from "@/lib/context/CartContext";
import { useWishlist } from "@/lib/context/WishlistContext";
import { Button } from "@/components/ui/Button";

export function ProductActions({ product }: { product: Product }) {
  const deal = getBoxDeal(product);
  const ask = isPriceOnRequest(product);
  const soldEachMoq12 = isSquishyEachCategorySlug(product.categorySlug);
  const minQty = soldEachMoq12 ? 12 : 1;
  const [qty, setQty] = useState(minQty);
  const { addItem } = useCart();
  const { toggle, has } = useWishlist();
  const router = useRouter();
  const wished = has(product.slug);
  const wholesale = product.brand === "Toy Bloom Wholesale" && !(isSquishyCategorySlug(product.categorySlug) && deal.soldAsBox);
  const unitLabel = deal.soldAsBox && !ask && !wholesale ? "boxes" : "items";

  if (ask) {
    return (
      <div className="space-y-4">
        <Button href="/contact/" size="lg" className="w-full">
          Ask for price
        </Button>
        <button
          type="button"
          onClick={() => toggle(product.slug)}
          className="inline-flex items-center gap-2 rounded-full border border-ink-200 px-4 py-2.5 text-sm font-semibold hover:border-coral-300"
        >
          <Heart className={wished ? "h-4 w-4 fill-coral-500 text-coral-500" : "h-4 w-4"} />
          {wished ? "Saved" : "Wishlist"}
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-3">
        <div className="inline-flex items-center rounded-full border border-ink-200 bg-white">
          <button
            type="button"
            className="p-3"
            aria-label={`Decrease ${unitLabel}`}
            onClick={() => setQty((value) => Math.max(minQty, value - 1))}
          >
            <Minus className="h-4 w-4" />
          </button>
          <span className="min-w-[2rem] text-center font-display font-bold">{qty}</span>
          <button
            type="button"
            className="p-3"
            aria-label={`Increase ${unitLabel}`}
            onClick={() => setQty((value) => value + 1)}
          >
            <Plus className="h-4 w-4" />
          </button>
        </div>
        <span className="text-sm font-semibold text-ink-500">
          {qty} {wholesale ? (qty === 1 ? "piece" : "pieces") : deal.soldAsBox ? (qty === 1 ? "box" : "boxes") : qty === 1 ? "item" : "items"}
        </span>
        <button
          type="button"
          onClick={() => toggle(product.slug)}
          className="ml-auto inline-flex items-center gap-2 rounded-full border border-ink-200 px-4 py-2.5 text-sm font-semibold hover:border-coral-300"
        >
          <Heart className={wished ? "h-4 w-4 fill-coral-500 text-coral-500" : "h-4 w-4"} />
          {wished ? "Saved" : "Wishlist"}
        </button>
      </div>
      <div className="flex flex-col gap-3 sm:flex-row">
        <Button type="button" size="lg" className="flex-1" onClick={() => addItem(product.slug, qty)}>
          {wholesale ? "Add to Cart" : deal.soldAsBox ? "Add box to cart" : "Add to Cart"}
        </Button>
        <Button
          type="button"
          size="lg"
          variant="secondary"
          className="flex-1"
          onClick={() => {
            addItem(product.slug, qty);
            router.push("/pay");
          }}
        >
          {wholesale ? "Buy Now" : deal.soldAsBox ? "Buy this box" : "Buy Now"}
        </Button>
      </div>
    </div>
  );
}
