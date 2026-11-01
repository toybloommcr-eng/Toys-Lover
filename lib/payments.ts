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
};

/** Live Toy Bloom Payment Link (acct_1UReoL1hBb7OocMn). Public URL, not a secret. */
const LIVE_STRIPE_PAYMENT_LINK = "https://buy.stripe.com/14AcMXaxigANeuIbtSb7y00";

export function stripePaymentLink(): string {
  const fromEnv = (process.env.NEXT_PUBLIC_STRIPE_PAYMENT_LINK || "").trim();
  if (fromEnv.startsWith("https://") && !fromEnv.includes("/test_")) {
    return fromEnv;
  }
  return LIVE_STRIPE_PAYMENT_LINK;
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
  url.searchParams.set("locale", "en-GB");
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
