"use client";

import { useState } from "react";
import { Button } from "@/components/ui/Button";
import { cn } from "@/lib/utils";

export function NewsletterForm({ compact = false }: { compact?: boolean }) {
  const [email, setEmail] = useState("");
  const [done, setDone] = useState(false);

  return (
    <form
      className={cn("flex flex-col gap-3 sm:flex-row")}
      onSubmit={(event) => {
        event.preventDefault();
        setDone(true);
      }}
    >
      <label className="sr-only" htmlFor={compact ? "footer-email" : "newsletter-email"}>
        Email address
      </label>
      <input
        id={compact ? "footer-email" : "newsletter-email"}
        type="email"
        required
        value={email}
        onChange={(event) => setEmail(event.target.value)}
        placeholder="Enter your email address"
        className={cn(
          "w-full rounded-full border px-4 py-3 text-sm shadow-sm focus:outline-none focus:ring-4",
          compact
            ? "border-transparent bg-white text-ink-800 placeholder:text-ink-400 focus:ring-teal-200"
            : "border-ink-200 bg-white text-ink-800 placeholder:text-ink-300 focus:ring-coral-100",
        )}
      />
      <Button type="submit" variant="primary" className="shrink-0">
        {done ? "You are in" : "Subscribe"}
      </Button>
    </form>
  );
}
