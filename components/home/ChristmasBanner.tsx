"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Gift, Snowflake } from "lucide-react";
import { isChristmasSeason } from "@/lib/christmas";
import { Container } from "@/components/ui/Container";

export function ChristmasBanner() {
  const [on, setOn] = useState(false);
  useEffect(() => setOn(isChristmasSeason()), []);
  if (!on) return null;

  return (
    <div className="christmas-banner border-b border-emerald-800/20 bg-gradient-to-r from-[#0B3D2E] via-[#14532D] to-[#7F1D1D] text-white">
      <Container className="flex flex-wrap items-center justify-between gap-3 py-2.5 sm:py-3">
        <p className="inline-flex items-center gap-2 font-display text-sm font-extrabold tracking-tight sm:text-base">
          <Snowflake className="h-4 w-4 shrink-0 text-sky-200" aria-hidden />
          Merry Christmas from Toy Bloom - festive stock is up front until Boxing Day
        </p>
        <div className="flex flex-wrap gap-2">
          <Link
            href="/shop/christmas-squishies"
            className="inline-flex items-center gap-1.5 rounded-full bg-white/95 px-3 py-1.5 font-display text-xs font-extrabold text-emerald-900 hover:bg-white"
          >
            <Gift className="h-3.5 w-3.5" aria-hidden />
            Christmas squishies
          </Link>
          <Link
            href="/shop/seasonal"
            className="inline-flex items-center gap-1.5 rounded-full border border-white/50 px-3 py-1.5 font-display text-xs font-extrabold text-white hover:bg-white/10"
          >
            Seasonal aisle
          </Link>
        </div>
      </Container>
    </div>
  );
}
