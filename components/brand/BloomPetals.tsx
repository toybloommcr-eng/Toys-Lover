"use client";

import { useReducedMotion } from "framer-motion";

const PETALS = [
  { left: "8%", delay: "0s", duration: "9s", color: "#F2704A", kind: "petal" },
  { left: "22%", delay: "1.4s", duration: "11s", color: "#14B8A6", kind: "dot" },
  { left: "36%", delay: "0.6s", duration: "8.5s", color: "#FFC107", kind: "petal" },
  { left: "51%", delay: "2.1s", duration: "10s", color: "#3ECF9A", kind: "confetti" },
  { left: "67%", delay: "0.3s", duration: "9.5s", color: "#FF7A55", kind: "petal" },
  { left: "81%", delay: "1.8s", duration: "12s", color: "#2DD4BF", kind: "dot" },
  { left: "14%", delay: "3s", duration: "10.5s", color: "#F0A202", kind: "confetti" },
  { left: "74%", delay: "2.6s", duration: "8s", color: "#E85A38", kind: "petal" },
] as const;

export function BloomPetals() {
  const reduce = useReducedMotion();
  if (reduce) return null;

  return (
    <div className="bloom-petals pointer-events-none absolute inset-0 z-[5] overflow-hidden" aria-hidden>
      {PETALS.map((petal, index) => (
        <span
          key={index}
          className={`bloom-flake bloom-flake-${petal.kind}`}
          style={{
            left: petal.left,
            animationDelay: petal.delay,
            animationDuration: petal.duration,
            background: petal.kind === "petal" ? undefined : petal.color,
            color: petal.color,
          }}
        />
      ))}
    </div>
  );
}
