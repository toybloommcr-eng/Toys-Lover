"use client";

import { useMemo, useState } from "react";
import { Lock, Loader2 } from "lucide-react";
import { useCart } from "@/lib/context/CartContext";
import { cartSubtotal, resolveCartLines } from "@/lib/cart-lines";
import { formatPrice, isPriceOnRequest, toTitleCase } from "@/lib/utils";
import { CONTACT } from "@/lib/constants";
import { buildStripeCheckoutUrl } from "@/lib/payments";
import { Input, Select, Textarea } from "@/components/ui/Input";
import { Button } from "@/components/ui/Button";

const methodLabel: Record<string, string> = {
  stripe: "Stripe",
  card: "Credit / debit card",
};

/**
 * Stripe Payment Links only accept letters, digits, "-" and "_" (max 200 chars) in
 * client_reference_id; anything else is silently dropped. Format:
 *   <slug>_x<qty>__<slug>_x<qty>[__more][__pickup]
 * Name, phone and address are collected by Stripe itself.
 */
const REF_MAX = 200;
function itemsRef(items: { slug: string; quantity: number }[], extra: string[] = []) {
  const tail = extra.map((t) => `__${t}`).join("");
  const parts = items.map(({ slug, quantity }) => {
    const s = slug.replace(/[^A-Za-z0-9-]/g, "-") || "item";
    return `${s}_x${Math.max(1, Math.floor(quantity) || 1)}`;
  });
  const full = parts.join("__") + tail;
  if (full.length <= REF_MAX) return full;
  const more = "__more" + tail;
  let out = "";
  for (const p of parts) {
    const next = out ? `${out}__${p}` : p;
    if (next.length + more.length > REF_MAX) break;
    out = next;
  }
  return ((out || "items") + more).slice(0, REF_MAX);
}

export function CheckoutForm({ method = "stripe" }: { method?: string }) {
  const { items, itemCount } = useCart();
  const lines = useMemo(() => resolveCartLines(items), [items]);
  const subtotal = useMemo(() => cartSubtotal(lines), [lines]);
  const shipping = subtotal >= 60 || itemCount === 0 ? 0 : 4.5;
  const total = subtotal + shipping;
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const payName = methodLabel[method] ?? "Stripe";

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
          const street = String(form.get("street") || "").trim();
          const city = String(form.get("city") || "").trim();
          const region = String(form.get("region") || "").trim();
          const postcode = String(form.get("postcode") || "").trim().toUpperCase();
          const country = String(form.get("country") || "").trim();
          const delivery = String(form.get("delivery") || "standard").trim();
          const note = String(form.get("note") || "").trim();
          if (name.length < 2) throw new Error("Please enter your full name.");
          if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) throw new Error("Please enter a valid email address.");
          if (phone.replace(/\D/g, "").length < 7) throw new Error("Please enter a valid phone number.");
          if (street.length < 3) throw new Error("Please enter the shipping street address.");
          if (city.length < 2) throw new Error("Please enter the shipping city / town.");
          if (postcode.length < 5) throw new Error("Please enter a valid UK postcode.");
          if (country.length < 2) throw new Error("Please enter the shipping country.");
          if (total < 1) throw new Error("Add a priced item before paying.");
          window.location.assign(
            buildStripeCheckoutUrl({
              email,
              amountGbp: total,
              reference: itemsRef(
                lines.map(({ product, quantity }) => ({ slug: product.slug, quantity })),
                delivery === "pickup" ? ["pickup"] : [],
              ),
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
          <Input label="Full name" name="name" required autoComplete="name" />
          <Input label="Email" name="email" type="email" required autoComplete="email" />
          <Input label="Phone" name="phone" required autoComplete="tel" defaultValue="" placeholder={CONTACT.phone} />
        </div>

        <h2 className="heading-glow font-display text-xl font-extrabold">Shipping address</h2>
        <p className="text-sm text-ink-500">Where should we send this order? Required before payment.</p>
        <Input label="Street address" name="street" required autoComplete="street-address" placeholder="House number and street" />
        <div className="grid gap-4 sm:grid-cols-2">
          <Input label="City / town" name="city" required autoComplete="address-level2" />
          <Input label="County / region" name="region" autoComplete="address-level1" placeholder="Optional" />
          <Input label="Postcode" name="postcode" required autoComplete="postal-code" placeholder="e.g. M1 1AE" />
          <Input label="Country" name="country" required autoComplete="country-name" defaultValue="United Kingdom" />
        </div>
        <Select label="Delivery" name="delivery" defaultValue="standard">
          <option value="standard">Standard (2–5 days)</option>
          <option value="pickup">Pickup in {CONTACT.city}</option>
        </Select>

        <Textarea label="Gift note (optional)" name="note" placeholder="Happy birthday…" />

        <h2 className="heading-glow font-display text-xl font-extrabold">
          Payment · {toTitleCase(payName)}
        </h2>
        <div className="flex items-start gap-2 rounded-2xl bg-mint-50 p-4 text-sm text-mint-800">
          <Lock className="mt-0.5 h-4 w-4 shrink-0" />
          <p>
            After your shipping address is filled in, you finish on {payName}’s official checkout so we never see full card data.
          </p>
        </div>
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
