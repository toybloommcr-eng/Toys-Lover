import type { Metadata } from "next";
import { Suspense } from "react";
import { Lock } from "lucide-react";
import { img } from "@/lib/media";
import { PAYMENT_ACCOUNTS } from "@/lib/payments";
import { Container } from "@/components/ui/Container";
import { Section } from "@/components/ui/Section";
import { PageHero } from "@/components/ui/PageHero";
import { DepositPayForm } from "@/components/pay/DepositPayForm";

export const metadata: Metadata = {
  title: "Pay Now · Deposit",
  description: "Pay a Toy Bloom deposit securely via official Stripe or PayPal checkout.",
  robots: { index: true, follow: true },
};

export default function PayPage() {
  return (
    <>
      <PageHero
        image={img.pageSale}
        eyebrow="Secure deposit"
        title="Pay Now with Stripe or PayPal"
        description="Enter your details, pick an account, then finish on Stripe or PayPal’s official payment page."
      />
      <Section>
        <Container>
          <div className="mb-6 grid gap-3 sm:grid-cols-2">
            <div className="rounded-2xl bg-white px-4 py-3 shadow-soft ring-1 ring-ink-100">
              <p className="text-[10px] font-bold uppercase tracking-[0.14em] text-[#635BFF]">Stripe</p>
              <p className="font-display text-base font-extrabold text-ink-900">{PAYMENT_ACCOUNTS.stripe.label}</p>
            </div>
            <div className="rounded-2xl bg-white px-4 py-3 shadow-soft ring-1 ring-ink-100">
              <p className="text-[10px] font-bold uppercase tracking-[0.14em] text-[#003087]">PayPal</p>
              <p className="font-display text-base font-extrabold text-ink-900">{PAYMENT_ACCOUNTS.paypal.label}</p>
            </div>
          </div>

          <Suspense fallback={<div className="h-80 animate-pulse rounded-[1.75rem] bg-cream-100" />}>
            <DepositPayForm />
          </Suspense>

          <p className="mx-auto mt-8 flex max-w-3xl items-start gap-2 text-sm text-ink-500">
            <Lock className="mt-0.5 h-4 w-4 shrink-0" />
            After you submit, you leave Toy Bloom and pay on Stripe or PayPal’s official page.
          </p>
        </Container>
      </Section>
    </>
  );
}
