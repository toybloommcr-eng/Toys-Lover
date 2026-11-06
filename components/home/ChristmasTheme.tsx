"use client";

import { useEffect } from "react";
import { isChristmasSeason } from "@/lib/christmas";

/** Applies festive chrome while UK Christmas season is live; removes it after Boxing Day. */
export function ChristmasTheme() {
  useEffect(() => {
    const root = document.documentElement;
    const apply = () => {
      root.classList.toggle("christmas-season", isChristmasSeason());
    };
    apply();
    const id = window.setInterval(apply, 60 * 60 * 1000);
    return () => {
      window.clearInterval(id);
      root.classList.remove("christmas-season");
    };
  }, []);
  return null;
}
