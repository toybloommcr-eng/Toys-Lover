"use client";

import { useEffect, useRef, useState, type PointerEvent as ReactPointerEvent } from "react";
import Image from "next/image";
import { motion, useReducedMotion, AnimatePresence } from "framer-motion";
import { ChevronLeft, ChevronRight } from "lucide-react";
import { img } from "@/lib/media";
import { BloomPetals } from "@/components/brand/BloomPetals";
import { cn } from "@/lib/utils";

function useIsCoarsePointer() {
  const [coarse, setCoarse] = useState(false);
  useEffect(() => {
    if (typeof window === "undefined" || !window.matchMedia) return;
    const mq = window.matchMedia("(hover: none), (pointer: coarse)");
    const apply = () => setCoarse(mq.matches);
    apply();
    mq.addEventListener?.("change", apply);
    return () => mq.removeEventListener?.("change", apply);
  }, []);
  return coarse;
}

export function ProductGallery({ images, name }: { images: string[]; name: string }) {
  const photos = images.length ? images : [img.heroToys];
  const [active, setActive] = useState(0);
  const reduce = useReducedMotion();
  const coarse = useIsCoarsePointer();
  const keepStill = Boolean(reduce || coarse);
  const dragX = useRef<number | null>(null);
  const src = photos[active] ?? photos[0];

  const go = (delta: number) => {
    if (photos.length < 2) return;
    setActive((current) => (current + delta + photos.length) % photos.length);
  };

  // Auto-advance only on desktop with fine pointer — avoid mobile lag / flip feel.
  useEffect(() => {
    if (keepStill || photos.length < 2) return;
    const id = window.setInterval(() => {
      setActive((current) => (current + 1) % photos.length);
    }, 5200);
    return () => window.clearInterval(id);
  }, [photos.length, keepStill]);

  const onPointerDown = (event: ReactPointerEvent<HTMLDivElement>) => {
    dragX.current = event.clientX;
  };

  const onPointerUp = (event: ReactPointerEvent<HTMLDivElement>) => {
    if (dragX.current == null) return;
    const dx = event.clientX - dragX.current;
    dragX.current = null;
    if (Math.abs(dx) > 46) go(dx < 0 ? 1 : -1);
  };

  return (
    <div>
      <div
        className="relative aspect-square w-full overflow-hidden rounded-[1.75rem] bg-white shadow-soft ring-1 ring-coral-100"
        onPointerDown={onPointerDown}
        onPointerUp={onPointerUp}
      >
        {!coarse ? <BloomPetals /> : null}
        <div className="absolute inset-0 bg-white">
          <AnimatePresence mode="wait" initial={false}>
            <motion.div
              key={src}
              initial={keepStill ? { opacity: 0 } : { opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={keepStill ? { opacity: 0 } : { opacity: 0 }}
              transition={{ duration: keepStill ? 0.15 : 0.25 }}
              className="absolute inset-0"
            >
              <Image
                src={src}
                alt={name}
                fill
                priority={active === 0}
                sizes="(min-width: 1024px) 420px, 100vw"
                quality={72}
                className="object-contain object-center bg-white p-3 sm:p-4"
                style={{ imageOrientation: "from-image" }}
                draggable={false}
              />
            </motion.div>
          </AnimatePresence>
        </div>

        {photos.length > 1 ? (
          <>
            <button
              type="button"
              aria-label="Previous photo"
              onClick={() => go(-1)}
              className="absolute left-2 top-1/2 z-10 grid h-10 w-10 -translate-y-1/2 place-items-center rounded-full bg-white/90 text-coral-500 shadow-soft ring-1 ring-cream-200"
            >
              <ChevronLeft className="h-5 w-5" />
            </button>
            <button
              type="button"
              aria-label="Next photo"
              onClick={() => go(1)}
              className="absolute right-2 top-1/2 z-10 grid h-10 w-10 -translate-y-1/2 place-items-center rounded-full bg-white/90 text-coral-500 shadow-soft ring-1 ring-cream-200"
            >
              <ChevronRight className="h-5 w-5" />
            </button>
            <p className="absolute bottom-2 left-1/2 z-10 -translate-x-1/2 rounded-full bg-ink-900/80 px-3 py-1 text-[11px] font-bold uppercase tracking-wide text-white sm:hidden">
              Swipe for more
            </p>
          </>
        ) : null}
      </div>
      {photos.length > 1 ? (
        <div className="mt-3 flex gap-2 overflow-x-auto pb-1">
          {photos.map((image, index) => (
            <button
              key={`${image}-${index}`}
              type="button"
              onClick={() => setActive(index)}
              aria-label={`Photo ${index + 1} of ${name}`}
              aria-current={index === active}
              className={cn(
                "relative h-16 w-16 shrink-0 overflow-hidden rounded-xl bg-white ring-2",
                index === active ? "ring-coral-500" : "ring-cream-200",
              )}
            >
              <Image
                src={image}
                alt=""
                fill
                sizes="64px"
                quality={60}
                loading="lazy"
                className="object-contain object-center bg-white p-1"
                style={{ imageOrientation: "from-image" }}
              />
            </button>
          ))}
        </div>
      ) : null}
    </div>
  );
}
