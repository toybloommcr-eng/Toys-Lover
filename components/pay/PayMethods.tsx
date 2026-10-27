"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { CreditCard, Lock, ShieldCheck, Wallet } from "lucide-react";
import { cn, toTitleCase } from "@/lib/utils";
import { Button } from "@/components/ui/Button";

const methods = [
  {
    id: "stripe",
    name: "Stripe",
    text: "Pay by card through Stripe’s encrypted checkout. Card details never sit on our servers.",
    icon: CreditCard,
    tone: "bg-[#635BFF]",
  },
  {
    id: "paypal",
    name: "PayPal",
    text: "Continue to PayPal. You can use a PayPal balance or a card stored with them.",
    icon: Wallet,
    tone: "bg-[#003087]",
  },
  {
    id: "card",
    name: "Credit / debit card",
    text: "Visa, Mastercard, and Maestro via a PCI-compliant processor — not a raw card form on this page.",
    icon: CreditCard,
    tone: "bg-[#7A4A2B]",
  },
] as const;

export function PayMethods() {
  const router = useRouter();
  const [selected, setSelected] = useState<(typeof methods)[number]["id"]>("stripe");

  return (
    <div className="mx-auto max-w-3xl">
      <div className="mb-6 flex items-start gap-3 rounded-2xl bg-mint-50 px-4 py-3 text-sm text-mint-800 ring-1 ring-mint-200">
        <ShieldCheck className="mt-0.5 h-5 w-5 shrink-0" />
        <p>
          This is a secure method picker only. No card number is typed or stored here. Stripe
          checkout opens on Stripe’s official page.
        </p>
      </div>

      <div className="grid gap-3">
        {methods.map((method) => {
          const Icon = method.icon;
          const active = selected === method.id;
          return (
            <button
              key={method.id}
              type="button"
              onClick={() => setSelected(method.id)}
              className={cn(
                "flex w-full items-start gap-4 rounded-3xl border-2 bg-white p-5 text-left transition",
                active ? "border-coral-500 shadow-lift" : "border-ink-100 hover:border-coral-200",
              )}
            >
              <span className={cn("grid h-12 w-12 shrink-0 place-items-center rounded-2xl text-white", method.tone)}>
                <Icon className="h-6 w-6" />
              </span>
              <span>
                <span className="heading-glow-soft block font-display text-lg font-extrabold text-ink-900">
                  {toTitleCase(method.name)}
                </span>
                <span className="mt-1 block text-sm text-ink-500">{method.text}</span>
              </span>
            </button>
          );
        })}
      </div>

      <div className="mt-6 flex items-center gap-2 text-xs font-semibold uppercase tracking-wide text-ink-400">
        <Lock className="h-4 w-4" />
        Encrypted connection · No card data on this page · Official checkout next
      </div>

      <Button
        type="button"
        size="lg"
        variant="buy"
        className="mt-6 w-full"
        onClick={() => router.push(`/checkout?method=${selected}`)}
      >
        Continue securely
      </Button>
    </div>
  );
}
