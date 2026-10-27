"use client";

import { useState } from "react";
import type { Product } from "@/lib/types";
import { cn } from "@/lib/utils";

export function ProductTabs({ product }: { product: Product }) {
  const [tab, setTab] = useState<"story" | "details">("story");

  return (
    <div className="mt-8">
      <div className="flex gap-2 border-b border-ink-100" role="tablist">
        {(
          [
            ["story", "Overview"],
            ["details", "Details"],
          ] as const
        ).map(([id, label]) => (
          <button
            key={id}
            type="button"
            role="tab"
            aria-selected={tab === id}
            className={cn(
              "px-4 py-2.5 font-display text-sm font-bold",
              tab === id ? "border-b-2 border-coral-500 text-coral-600" : "text-ink-400",
            )}
            onClick={() => setTab(id)}
          >
            {label}
          </button>
        ))}
      </div>
      <div className="pt-5 text-sm leading-relaxed text-ink-600">
        {tab === "story" ? (
          <p>{product.shortDescription}</p>
        ) : (
          <p>{product.description}</p>
        )}
      </div>
    </div>
  );
}
