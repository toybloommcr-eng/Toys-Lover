"use client";

import { useState } from "react";
import { ChevronDown } from "lucide-react";
import { cn, toTitleCase } from "@/lib/utils";

export function Accordion({
  items,
}: {
  items: { question: string; answer: string }[];
}) {
  const [open, setOpen] = useState<number | null>(0);

  return (
    <div className="divide-y divide-ink-100 overflow-hidden rounded-3xl border border-ink-100 bg-white shadow-soft">
      {items.map((item, index) => {
        const isOpen = open === index;
        return (
          <div key={item.question}>
            <button
              type="button"
              className="flex w-full items-center justify-between gap-4 px-5 py-4 text-left font-display font-semibold text-ink-800 hover:bg-cream-100"
              aria-expanded={isOpen}
              onClick={() => setOpen(isOpen ? null : index)}
            >
              {toTitleCase(item.question)}
              <ChevronDown
                className={cn(
                  "h-5 w-5 shrink-0 text-coral-500 transition-transform",
                  isOpen && "rotate-180",
                )}
              />
            </button>
            <div
              className={cn(
                "grid transition-[grid-template-rows] duration-300",
                isOpen ? "grid-rows-[1fr]" : "grid-rows-[0fr]",
              )}
            >
              <p className="overflow-hidden px-5 text-sm leading-relaxed text-ink-500">
                <span className="block pb-5">{item.answer}</span>
              </p>
            </div>
          </div>
        );
      })}
    </div>
  );
}
