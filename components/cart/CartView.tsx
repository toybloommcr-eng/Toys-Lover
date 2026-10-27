"use client";

import { useMemo } from "react";
import Link from "next/link";
import { Minus, Plus, Trash2 } from "lucide-react";
import { useCart } from "@/lib/context/CartContext";
import { cartSubtotal, resolveCartLines } from "@/lib/cart-lines";
import { formatPrice, isPriceOnRequest, toTitleCase } from "@/lib/utils";
import { Button } from "@/components/ui/Button";
import { ToyPhoto } from "@/components/ui/ToyPhoto";

export function CartView() {
  const { items, updateQuantity, removeItem, itemCount } = useCart();
  const lines = useMemo(() => resolveCartLines(items), [items]);
  const subtotal = useMemo(() => cartSubtotal(lines), [lines]);

  if (lines.length === 0) {
    return (
      <div className="rounded-3xl bg-white p-8 text-center shadow-card sm:p-10">
        <p className="font-display text-2xl font-extrabold text-ink-900">Your cart is empty</p>
        <p className="mt-2 text-ink-500">Find a toy you would happily give at bedtime.</p>
        <Button href="/shop" className="mt-6">
          Shop Now
        </Button>
      </div>
    );
  }

  const shipping = subtotal >= 60 ? 0 : 4.5;
  const total = subtotal + shipping;

  return (
    <div className="grid gap-8 pb-28 lg:grid-cols-[1fr_20rem] lg:pb-0">
      <ul className="space-y-4">
        {lines.map(({ product, quantity }) => (
          <li
            key={product.slug}
            className="flex gap-4 rounded-3xl border border-ink-100 bg-white p-4 shadow-soft"
          >
            <Link
              href={`/product/${product.slug}`}
              className="media-hover-frame h-32 w-32 shrink-0 overflow-hidden rounded-2xl sm:h-36 sm:w-36"
            >
              <ToyPhoto src={product.images[0]} alt={product.name} sizes="96px" className="h-24 w-24" />
            </Link>
            <div className="min-w-0 flex-1">
              <Link
                href={`/product/${product.slug}`}
                className="font-display font-extrabold text-ink-900 hover:text-coral-600"
              >
                {toTitleCase(product.name)}
              </Link>
              <p className="text-sm text-ink-400">{product.brand}</p>
              <p className="mt-1 font-semibold">{isPriceOnRequest(product) ? "Price on request" : formatPrice(product.price)}</p>
              <div className="mt-3 flex flex-wrap items-center gap-3">
                <div className="inline-flex items-center rounded-full border border-ink-200">
                  <button
                    type="button"
                    className="grid h-11 w-11 place-items-center"
                    aria-label="Decrease quantity"
                    onClick={() => updateQuantity(product.slug, quantity - 1)}
                  >
                    <Minus className="h-4 w-4" />
                  </button>
                  <span className="min-w-[1.75rem] text-center text-sm font-bold">{quantity}</span>
                  <button
                    type="button"
                    className="grid h-11 w-11 place-items-center"
                    aria-label="Increase quantity"
                    onClick={() => updateQuantity(product.slug, quantity + 1)}
                  >
                    <Plus className="h-4 w-4" />
                  </button>
                </div>
                <button
                  type="button"
                  onClick={() => removeItem(product.slug)}
                  className="inline-flex min-h-11 items-center gap-1 text-sm text-ink-400 hover:text-coral-600"
                >
                  <Trash2 className="h-4 w-4" />
                  Remove
                </button>
              </div>
            </div>
          </li>
        ))}
      </ul>

      <aside className="hidden h-fit rounded-3xl bg-white p-6 shadow-card lg:block">
        <h2 className="font-display text-lg font-extrabold">Order Summary</h2>
        <p className="mt-4 flex justify-between text-sm">
          <span>{itemCount} items</span>
          <span>{formatPrice(subtotal)}</span>
        </p>
        <p className="mt-2 flex justify-between text-sm text-ink-500">
          <span>Shipping</span>
          <span>{shipping === 0 ? "Free" : formatPrice(shipping)}</span>
        </p>
        <p className="mt-4 flex justify-between font-display text-lg font-extrabold">
          <span>Total</span>
          <span>{formatPrice(total)}</span>
        </p>
        <Button href="/pay" size="lg" className="mt-6 w-full">
          Buy Online
        </Button>
      </aside>

      <div className="fixed inset-x-0 bottom-0 z-40 border-t border-cream-200 bg-white/95 p-3 shadow-[0_-8px_24px_rgba(0,0,0,0.08)] backdrop-blur-md lg:hidden">
        <div className="mx-auto flex max-w-7xl items-center gap-3">
          <div className="min-w-0 flex-1">
            <p className="text-xs text-ink-500">{itemCount} items</p>
            <p className="font-display text-lg font-extrabold text-ink-900">{formatPrice(total)}</p>
          </div>
          <Button href="/pay" size="lg" className="shrink-0 px-6">
            Buy Online
          </Button>
        </div>
      </div>
    </div>
  );
}
