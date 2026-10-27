export const DEPOSIT_PRESETS_GBP = [10, 25, 50, 100] as const;

export const DEFAULT_DEPOSIT_GBP = 25;

/** Public labels shown on Pay Now UI (not secrets). */
export const PAYMENT_ACCOUNTS = {
  stripe: {
    id: "stripe" as const,
    name: "Stripe",
    label: process.env.NEXT_PUBLIC_STRIPE_ACCOUNT_LABEL || "Toy Bloom · Stripe",
    blurb: "Card checkout on Stripe’s official secure page.",
  },
  paypal: {
    id: "paypal" as const,
    name: "PayPal",
    label: process.env.NEXT_PUBLIC_PAYPAL_ACCOUNT_LABEL || "Toy Bloom · PayPal",
    blurb: "PayPal balance or card on PayPal’s official page.",
  },
};

export type PayMethodId = keyof typeof PAYMENT_ACCOUNTS;

export function stripePaymentLink(): string {
  return (process.env.NEXT_PUBLIC_STRIPE_PAYMENT_LINK || "").trim();
}

export function paypalMeLink(): string {
  return (process.env.NEXT_PUBLIC_PAYPAL_ME_LINK || "").trim();
}

/** Build a Stripe Payment Link URL with deposit/cart amount in pence. */
export function buildStripeCheckoutUrl(options: {
  email?: string;
  amountGbp?: number;
  reference?: string;
}): string {
  const stripeLink = stripePaymentLink();
  if (!stripeLink.startsWith("https://")) {
    throw new Error("Stripe Payment Link is not configured.");
  }
  const url = new URL(stripeLink);
  if (options.email) {
    url.searchParams.set("prefilled_email", options.email);
  }
  if (options.amountGbp && Number.isFinite(options.amountGbp) && options.amountGbp >= 1) {
    url.searchParams.set("prefilled_amount", String(Math.round(options.amountGbp * 100)));
  }
  if (options.reference) {
    url.searchParams.set("client_reference_id", options.reference.slice(0, 200));
  }
  return url.toString();
}

export function buildPaypalCheckoutUrl(amountGbp: number): string {
  const paypalLink = paypalMeLink();
  if (!paypalLink.startsWith("https://")) {
    throw new Error("PayPal.Me link is not configured.");
  }
  return `${paypalLink.replace(/\/$/, "")}/${amountGbp.toFixed(2)}`;
}
