"use client";

import { useMemo, useState } from "react";
import { useSearchParams } from "next/navigation";
import { CheckCircle2, CreditCard, Loader2, Lock, ShieldCheck, Wallet } from "lucide-react";
import { CONTACT, SITE_NAME } from "@/lib/constants";
import {
  DEFAULT_DEPOSIT_GBP,
  DEPOSIT_PRESETS_GBP,
  PAYMENT_ACCOUNTS,
  buildPaypalCheckoutUrl,
  buildStripeCheckoutUrl,
  type PayMethodId,
} from "@/lib/payments";
import { cn, formatPrice } from "@/lib/utils";
import { Button } from "@/components/ui/Button";
import { Input, Textarea } from "@/components/ui/Input";

function StripeMark({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 60 25" aria-hidden="true">
      <path
        fill="currentColor"
        d="M59.64 14.28s-1.45-.72-1.45-2.72.9-3.27 2.72-3.27c1.09 0 1.81.36 1.81.36l.36-2.18s-.91-.54-2.54-.54c-3.27 0-5.45 2.36-5.45 5.63 0 4.18 3.81 4.18 3.81 6.36 0 1.45-1.27 2.18-2.54 2.18-1.81 0-2.91-.91-2.91-.91l-.36 2.27s1.27.91 3.45.91c3.45 0 5.81-2.18 5.81-5.81.01-3.45-3.71-3.81-3.71-6.28zM48.3 8.2c-1.09 0-1.81.54-2.36 1.09l-.18-.91h-2.54v14.9h2.91v-8.9c.36-.54.91-1.09 1.81-1.09 1.09 0 1.45.72 1.45 1.81v8.18h2.91V14c0-3.81-1.81-5.8-4-5.8zm-9.45 0c-2.18 0-3.81 1.09-3.81 1.09l.36 2.18s1.45-.91 2.72-.91c1.45 0 2.18.91 2.18 2.18v.36h-2.72c-3.09 0-4.72 1.45-4.72 3.81 0 2.36 1.63 3.81 4 3.81 1.63 0 2.72-.72 3.27-1.27l.18.91h2.54v-7.45c0-3.09-1.81-4.71-4-4.71zm1.09 8.72c-.36.54-1.09.91-1.81.91-1.09 0-1.81-.72-1.81-1.81 0-1.09.72-1.81 2.18-1.81h1.45v2.71zm-11.08-8.72c-1.09 0-1.81.54-2.36 1.09l-.18-.91h-2.54v14.9h2.91v-8.9c.36-.54.91-1.09 1.81-1.09 1.09 0 1.45.72 1.45 1.81v8.18h2.91V14c0-3.81-1.81-5.8-4-5.8zM19.4 7.83c-1.09-.36-1.81-.54-2.91-.54-3.45 0-5.81 2.18-5.81 5.81s2.36 5.81 5.81 5.81c1.09 0 1.81-.18 2.91-.54l-.54-2.18s-.72.36-1.81.36c-1.81 0-3.09-1.27-3.09-3.45s1.27-3.45 3.09-3.45c1.09 0 1.81.36 1.81.36l.54-2.18zM8.54 5.29L5.45 6.2l-.18 9.99c0 1.81-.72 2.36-1.81 2.36-.72 0-1.27-.18-1.81-.36l-.36 2.36s.91.54 2.36.54c2.72 0 4.18-1.45 4.18-4.54V5.29h.71z"
      />
    </svg>
  );
}

function PayPalMark({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 80 20" aria-hidden="true">
      <text x="0" y="15" fill="currentColor" fontFamily="Arial, sans-serif" fontWeight="800" fontSize="16">
        PayPal
      </text>
    </svg>
  );
}

export function DepositPayForm() {
  const params = useSearchParams();
  const status = params.get("status");
  const provider = params.get("provider");

  const [method, setMethod] = useState<PayMethodId>("stripe");
  const [amount, setAmount] = useState(DEFAULT_DEPOSIT_GBP);
  const [custom, setCustom] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  const effectiveAmount = useMemo(() => {
    if (custom.trim()) {
      const n = Number(custom.replace(/[^0-9.]/g, ""));
      return Number.isFinite(n) ? n : amount;
    }
    return amount;
  }, [amount, custom]);

  if (status === "success") {
    return (
      <div className="rounded-[1.75rem] bg-white p-8 text-center shadow-lift ring-1 ring-mint-200 sm:p-10">
        <CheckCircle2 className="mx-auto h-12 w-12 text-teal-600" />
        <h2 className="mt-4 font-display text-2xl font-extrabold text-ink-900 sm:text-3xl">
          Deposit received
        </h2>
        <p className="mx-auto mt-3 max-w-md text-sm leading-relaxed text-ink-600">
          Thanks — your {provider === "paypal" ? "PayPal" : "Stripe"} payment went through on their
          official page. We’ll confirm your Toy Bloom order by email shortly.
        </p>
        <Button href="/shop" className="mt-6" size="lg">
          Continue shopping
        </Button>
      </div>
    );
  }

  if (status === "cancel") {
    return (
      <div className="rounded-[1.75rem] bg-white p-8 text-center shadow-card ring-1 ring-coral-100 sm:p-10">
        <h2 className="font-display text-2xl font-extrabold text-ink-900">Checkout cancelled</h2>
        <p className="mx-auto mt-3 max-w-md text-sm text-ink-600">
          No deposit was taken. Your details are still ready — choose Stripe or PayPal below and try again.
        </p>
        <Button href="/pay" className="mt-6" size="lg">
          Try again
        </Button>
      </div>
    );
  }

  return (
    <form
      className="grid gap-6 lg:grid-cols-[1.15fr_0.85fr]"
      onSubmit={async (event) => {
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
          if (!effectiveAmount || effectiveAmount < 1) throw new Error("Enter a deposit of at least £1.");

          if (method === "stripe") {
            window.location.assign(
              buildStripeCheckoutUrl({
                email,
                amountGbp: effectiveAmount,
                reference: `${name}|${phone}|${effectiveAmount}|${note}`,
              }),
            );
            return;
          }

          window.location.assign(buildPaypalCheckoutUrl(effectiveAmount));
        } catch (err) {
          setError(err instanceof Error ? err.message : "Payment could not be started.");
          setBusy(false);
        }
      }}
    >
      <div className="space-y-5 rounded-[1.75rem] bg-white p-6 shadow-soft ring-1 ring-ink-100 sm:p-8">
        <div className="flex items-start gap-3 rounded-2xl bg-mint-50 px-4 py-3 text-sm text-mint-900 ring-1 ring-mint-200">
          <ShieldCheck className="mt-0.5 h-5 w-5 shrink-0 text-teal-600" />
          <p>
            Enter your details here, then you’ll be taken to the <strong>official Stripe or PayPal</strong>{" "}
            page to pay your deposit. Card numbers are never typed on {SITE_NAME}.
          </p>
        </div>

        <div className="grid gap-4 sm:grid-cols-2">
          <Input label="Full name" name="name" required autoComplete="name" placeholder="Alex Taylor" />
          <Input label="Email" name="email" type="email" required autoComplete="email" placeholder="you@email.com" />
          <Input
            label="Phone"
            name="phone"
            required
            autoComplete="tel"
            placeholder={CONTACT.phone}
            className="sm:col-span-2"
          />
        </div>

        <div>
          <p className="font-display text-sm font-semibold text-ink-800">Deposit amount</p>
          <div className="mt-2 flex flex-wrap gap-2">
            {DEPOSIT_PRESETS_GBP.map((preset) => (
              <button
                key={preset}
                type="button"
                onClick={() => {
                  setAmount(preset);
                  setCustom("");
                }}
                className={cn(
                  "rounded-full px-4 py-2 font-display text-sm font-bold transition",
                  !custom && amount === preset
                    ? "bg-coral-500 text-white shadow-soft"
                    : "bg-cream-100 text-ink-700 hover:bg-cream-200",
                )}
              >
                {formatPrice(preset)}
              </button>
            ))}
          </div>
          <div className="mt-3">
            <Input
              label="Or enter a custom amount (£)"
              name="customAmount"
              inputMode="decimal"
              placeholder="e.g. 35"
              value={custom}
              onChange={(e) => setCustom(e.target.value)}
            />
          </div>
        </div>

        <Textarea
          label="Order note (optional)"
          name="note"
          placeholder="Order reference, gift message, or what the deposit is for…"
          className="min-h-[100px]"
        />
      </div>

      <aside className="h-fit space-y-4 rounded-[1.75rem] bg-gradient-to-br from-teal-700 via-teal-800 to-ink-900 p-6 text-white shadow-lift sm:p-7">
        <p className="text-[11px] font-bold uppercase tracking-[0.18em] text-sun-300">Pay deposit now</p>
        <h2 className="font-display text-2xl font-extrabold leading-tight">
          Choose your account
        </h2>
        <p className="text-sm text-teal-100">
          You’ll finish on Stripe or PayPal’s own secure checkout — same pattern as professional UK shops.
        </p>

        <div className="grid gap-3">
          {(Object.keys(PAYMENT_ACCOUNTS) as PayMethodId[]).map((id) => {
            const account = PAYMENT_ACCOUNTS[id];
            const active = method === id;
            const Icon = id === "stripe" ? CreditCard : Wallet;
            return (
              <button
                key={id}
                type="button"
                onClick={() => setMethod(id)}
                className={cn(
                  "flex items-center gap-3 rounded-2xl border-2 p-4 text-left transition",
                  active
                    ? "border-sun-300 bg-white text-ink-900 shadow-soft"
                    : "border-white/20 bg-white/5 text-white hover:bg-white/10",
                )}
              >
                <span
                  className={cn(
                    "grid h-11 w-11 place-items-center rounded-xl",
                    active ? (id === "stripe" ? "bg-[#635BFF] text-white" : "bg-[#003087] text-white") : "bg-white/15",
                  )}
                >
                  <Icon className="h-5 w-5" />
                </span>
                <span className="min-w-0 flex-1">
                  <span className="flex items-center justify-between gap-2">
                    <span className="font-display text-base font-extrabold">{account.name}</span>
                    {id === "stripe" ? (
                      <StripeMark className={cn("h-4 w-14", active ? "text-[#635BFF]" : "text-white/80")} />
                    ) : (
                      <PayPalMark className={cn("h-4 w-16", active ? "text-[#003087]" : "text-white/80")} />
                    )}
                  </span>
                  <span className={cn("mt-0.5 block text-xs font-semibold", active ? "text-ink-500" : "text-teal-100")}>
                    {account.label}
                  </span>
                  <span className={cn("mt-1 block text-xs", active ? "text-ink-500" : "text-teal-100/90")}>
                    {account.blurb}
                  </span>
                </span>
              </button>
            );
          })}
        </div>

        <div className="rounded-2xl bg-white/10 px-4 py-3 text-sm">
          <p className="flex justify-between font-display text-lg font-extrabold">
            <span>Deposit</span>
            <span>{formatPrice(effectiveAmount || 0)}</span>
          </p>
          <p className="mt-1 text-xs text-teal-100">Payable now · balance later if agreed</p>
        </div>

        {error ? (
          <p className="rounded-xl bg-coral-500/90 px-3 py-2 text-sm font-semibold text-white">{error}</p>
        ) : null}

        <Button
          type="submit"
          size="lg"
          variant="sun"
          className="w-full !rounded-2xl !py-4 text-base font-black uppercase tracking-wide shadow-[0_0_24px_rgba(250,204,21,0.45)]"
          disabled={busy}
        >
          {busy ? (
            <>
              <Loader2 className="h-5 w-5 animate-spin" />
              Opening {PAYMENT_ACCOUNTS[method].name}…
            </>
          ) : (
            <>
              Pay Now with {PAYMENT_ACCOUNTS[method].name}
            </>
          )}
        </Button>

        <p className="flex items-center justify-center gap-1.5 text-[11px] font-semibold uppercase tracking-wide text-teal-100">
          <Lock className="h-3.5 w-3.5" />
          Encrypted · Official {PAYMENT_ACCOUNTS[method].name} page next
        </p>
      </aside>
    </form>
  );
}
