import type { CartItem, Product } from "@/lib/types";
import { getProduct } from "@/lib/data/products";

export function resolveCartLines(items: CartItem[]) {
  return items
    .map((item) => {
      const product = getProduct(item.slug);
      return product ? { product, quantity: item.quantity } : null;
    })
    .filter((line): line is { product: Product; quantity: number } => line !== null);
}

export function cartSubtotal(lines: { product: Product; quantity: number }[]) {
  return lines.reduce(
    (sum, line) => sum + (line.product.priceTBC ? 0 : line.product.price * line.quantity),
    0,
  );
}
