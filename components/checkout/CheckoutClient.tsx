"use client";

import { useSearchParams } from "next/navigation";
import { CheckoutForm } from "@/components/checkout/CheckoutForm";

export function CheckoutClient() {
  const params = useSearchParams();
  const raw = params.get("method");
  const method = raw === "paypal" || raw === "card" ? raw : "stripe";
  return <CheckoutForm method={method} />;
}
