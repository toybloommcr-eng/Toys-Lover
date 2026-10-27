import Link from "next/link";
import { ArrowRight, Lock, Sparkles, Zap } from "lucide-react";
import { PAYMENT_ACCOUNTS } from "@/lib/payments";
import { Container } from "@/components/ui/Container";

export function PayNowBanner() {
  return (
    <section id="pay-now" className="py-6 sm:py-8">
      <Container>
        <div className="relative overflow-hidden rounded-[1.9rem] bg-gradient-to-br from-teal-700 via-teal-600 to-coral-500 px-6 py-9 text-white shadow-lift sm:px-10 sm:py-11">
          <div className="pointer-events-none absolute -right-10 -top-10 h-44 w-44 rounded-full bg-sun-300/25 blur-2xl" />
          <div className="pointer-events-none absolute -bottom-16 left-10 h-40 w-40 rounded-full bg-white/15 blur-2xl" />
          <div className="pointer-events-none absolute inset-0 opacity-[0.08]" style={{ backgroundImage: "radial-gradient(circle at 20% 20%, #fff 1px, transparent 1px)", backgroundSize: "18px 18px" }} />

          <div className="relative grid items-center gap-8 lg:grid-cols-[1.2fr_0.8fr]">
            <div>
              <p className="inline-flex items-center gap-2 rounded-full bg-white/15 px-3 py-1 text-[11px] font-bold uppercase tracking-[0.16em] text-sun-200 ring-1 ring-white/20">
                <Zap className="h-3.5 w-3.5 text-sun-300" />
                Secure deposit · Pay Now
              </p>
              <h2 className="heading-glow-light mt-4 font-display text-4xl font-extrabold leading-tight sm:text-5xl lg:text-[3.25rem]">
                Ready to reserve?
                <span className="block text-sun-300">Pay your deposit in seconds.</span>
              </h2>
              <p className="mt-3 max-w-xl text-sm leading-relaxed text-teal-50 sm:text-base">
                Tap Pay Now, enter your details, then finish on the official{" "}
                <strong className="text-white">Stripe</strong> or{" "}
                <strong className="text-white">PayPal</strong> page — card details never sit on Toy Bloom.
              </p>

              <div className="mt-6 flex flex-wrap items-center gap-3">
                <Link
                  href="/pay"
                  className="group inline-flex items-center gap-2 rounded-full bg-sun-300 px-7 py-3.5 font-display text-base font-black uppercase tracking-wide text-ink-900 shadow-[0_0_28px_rgba(250,204,21,0.55)] transition hover:-translate-y-0.5 hover:bg-sun-200 hover:shadow-[0_0_36px_rgba(250,204,21,0.7)]"
                >
                  <Sparkles className="h-5 w-5" />
                  Pay Now
                  <ArrowRight className="h-4 w-4 transition group-hover:translate-x-0.5" />
                </Link>
                <p className="inline-flex items-center gap-1.5 text-xs font-semibold text-teal-50">
                  <Lock className="h-3.5 w-3.5" />
                  Encrypted handoff to Stripe / PayPal
                </p>
              </div>
            </div>

            <div className="grid gap-3">
              <div className="rounded-2xl bg-white p-4 text-ink-900 shadow-soft">
                <div className="flex items-center justify-between gap-3">
                  <div>
                    <p className="text-[10px] font-bold uppercase tracking-[0.14em] text-[#635BFF]">Stripe account</p>
                    <p className="mt-1 font-display text-lg font-extrabold">{PAYMENT_ACCOUNTS.stripe.label}</p>
                    <p className="mt-0.5 text-xs text-ink-500">{PAYMENT_ACCOUNTS.stripe.blurb}</p>
                  </div>
                  <span className="rounded-xl bg-[#635BFF] px-3 py-2 font-display text-xs font-black text-white">
                    STRIPE
                  </span>
                </div>
              </div>
              <div className="rounded-2xl bg-white p-4 text-ink-900 shadow-soft">
                <div className="flex items-center justify-between gap-3">
                  <div>
                    <p className="text-[10px] font-bold uppercase tracking-[0.14em] text-[#003087]">PayPal account</p>
                    <p className="mt-1 font-display text-lg font-extrabold">{PAYMENT_ACCOUNTS.paypal.label}</p>
                    <p className="mt-0.5 text-xs text-ink-500">{PAYMENT_ACCOUNTS.paypal.blurb}</p>
                  </div>
                  <span className="rounded-xl bg-[#003087] px-3 py-2 font-display text-xs font-black text-white">
                    PayPal
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </Container>
    </section>
  );
}
