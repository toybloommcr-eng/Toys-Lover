"use client";

import { useMemo, useState } from "react";
import { Lock, Loader2 } from "lucide-react";
import { useCart } from "@/lib/context/CartContext";
import { cartSubtotal, resolveCartLines } from "@/lib/cart-lines";
import { formatPrice, isPriceOnRequest, toTitleCase } from "@/lib/utils";
import { CONTACT } from "@/lib/constants";
import { buildPaypalCheckoutUrl, buildStripeCheckoutUrl } from "@/lib/payments";
import { Input, Select, Textarea } from "@/components/ui/Input";
import { Button } from "@/components/ui/Button";

const methodLabel: Record<string, string> = {
  stripe: "Stripe",
  paypal: "PayPal",
  card: "Credit / debit card",
};

export function CheckoutForm({ method = "stripe" }: { method?: string }) {
  const { items, itemCount } = useCart();
  const lines = useMemo(() => resolveCartLines(items), [items]);
  const subtotal = useMemo(() => cartSubtotal(lines), [lines]);
  const shipping = subtotal >= 60 || itemCount === 0 ? 0 : 4.5;
  const total = subtotal + shipping;
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const payName = methodLabel[method] ?? "Stripe";
  const usePaypal = method === "paypal";

  if (lines.length === 0) {
    return (
      <div className="rounded-3xl border border-dashed border-ink-200 bg-white p-10 text-center">
        <p className="heading-glow font-display text-xl font-extrabold">
          {toTitleCase("Add something to the bag first.")}
        </p>
        <Button href="/shop" className="mt-5">
          Shop Now
        </Button>
      </div>
    );
  }

  return (
    <form
      className="grid gap-8 lg:grid-cols-[1fr_20rem]"
      onSubmit={(event) => {
        event.preventDefault();
        setError("");
        setBusy(true);
        const form = new FormData(event.currentTarget);
        try {
          const name = String(form.get("name") || "").trim();
          const email = String(form.get("email") || "").trim().toLowerCase();
          const phone = String(form.get("phone") || "").trim();
          const note = String(form.get("note") || "").trim();
          if (name.length < 2) throw new Error("Please enter your full name.");
          if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) throw new Error("Please enter a valid email address.");
          if (phone.replace(/\D/g, "").length < 7) throw new Error("Please enter a valid phone number.");
          if (total < 1) throw new Error("Add a priced item before paying.");
          const slugs = lines.map(({ product, quantity }) => `${product.slug}x${quantity}`).join(",");
          if (usePaypal) {
            window.location.assign(buildPaypalCheckoutUrl(total));
            return;
          }
          window.location.assign(
            buildStripeCheckoutUrl({
              email,
              amountGbp: total,
              reference: `${name}|${phone}|${total}|${slugs}|${note}`,
            }),
          );
        } catch (err) {
          setError(err instanceof Error ? err.message : "Payment could not be started.");
          setBusy(false);
        }
      }}
    >
      <div className="space-y-6 rounded-3xl bg-white p-6 shadow-soft">
        <h2 className="heading-glow font-display text-xl font-extrabold">Contact</h2>
        <div className="grid gap-4 sm:grid-cols-2">
          <Input label="Full name" name="name" required />
          <Input label="Email" name="email" type="email" required />
          <Input label="Phone" name="phone" required defaultValue="" placeholder={CONTACT.phone} />
        </div>
        <h2 className="heading-glow font-display text-xl font-extrabold">Address</h2>
        <Input label="Street address" name="street" required />
        <div className="grid gap-4 sm:grid-cols-3">
          <Input label="City" name="city" required defaultValue={CONTACT.city} />
          <Input label="Region" name="region" required defaultValue={CONTACT.region} />
          <Input label="Country" name="country" required defaultValue={CONTACT.country} />
        </div>
        <Select label="Delivery" name="delivery" defaultValue="standard">
          <option value="standard">Standard (2–5 days)</option>
          <option value="pickup">Pickup in {CONTACT.city}</option>
        </Select>
        <h2 className="heading-glow font-display text-xl font-extrabold">
          Payment · {toTitleCase(payName)}
        </h2>
        <div className="flex items-start gap-2 rounded-2xl bg-mint-50 p-4 text-sm text-mint-800">
          <Lock className="mt-0.5 h-4 w-4 shrink-0" />
          <p>
            Card numbers are not collected on this form. You finish on {payName}’s official
            checkout so we never see full card data.
          </p>
        </div>
        <Textarea label="Gift note (optional)" name="note" placeholder="Happy birthday…" />
      </div>
      <aside className="h-fit rounded-3xl bg-white p-6 shadow-card">
        <h2 className="heading-glow font-display text-lg font-extrabold">
          Pay With {toTitleCase(payName)}
        </h2>
        <ul className="mt-4 space-y-2 text-sm">
          {lines.map(({ product, quantity }) => (
            <li key={product.slug} className="flex justify-between gap-3">
              <span>
                {toTitleCase(product.name)} × {quantity}
              </span>
              <span>{isPriceOnRequest(product) ? "Price on request" : formatPrice(product.price * quantity)}</span>
            </li>
          ))}
        </ul>
        <p className="mt-4 flex justify-between text-sm">
          <span>Shipping</span>
          <span>{shipping === 0 ? "Free" : formatPrice(shipping)}</span>
        </p>
        <p className="mt-3 flex justify-between font-display text-lg font-extrabold">
          <span>Total</span>
          <span>{formatPrice(subtotal + shipping)}</span>
        </p>
        {error ? (
          <p className="mt-4 rounded-xl bg-coral-500/90 px-3 py-2 text-sm font-semibold text-white">{error}</p>
        ) : null}
        <Button type="submit" size="lg" variant="buy" className="mt-6 w-full" disabled={busy}>
          {busy ? (
            <>
              <Loader2 className="h-5 w-5 animate-spin" />
              Opening {payName}…
            </>
          ) : (
            `Pay ${formatPrice(total)} with ${payName}`
          )}
        </Button>
        <Button href="/pay" variant="outline" className="mt-3 w-full">
          Change payment method
        </Button>
      </aside>
    </form>
  );
}
