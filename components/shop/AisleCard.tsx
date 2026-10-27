import Link from "next/link";
import Image from "next/image";
import { ArrowRight } from "lucide-react";
import type { Category } from "@/lib/types";
import { cn, toTitleCase } from "@/lib/utils";

const accentChip: Record<Category["accent"], string> = {
  coral: "bg-coral-50 text-coral-700",
  sky: "bg-sky-50 text-sky-700",
  mint: "bg-mint-50 text-mint-800",
  sun: "bg-sun-50 text-[#9A5B00]",
};

export function AisleCard({
  category,
  count,
  productNames = [],
  className,
  priority,
}: {
  category: Category;
  count?: number;
  productNames?: string[];
  className?: string;
  priority?: boolean;
}) {
  const mentioned = productNames.slice(0, 2);

  return (
    <Link
      href={`/shop/${category.slug}`}
      className={cn(
        "media-hover group flex h-full flex-col overflow-hidden rounded-2xl bg-white shadow-soft ring-1 ring-cream-200 transition hover:-translate-y-0.5 hover:shadow-card",
        className,
      )}
    >
      <div className="relative aspect-square overflow-hidden bg-white">
        <Image
          src={category.image}
          alt={category.name}
          fill
          priority={priority}
          sizes="(min-width: 1280px) 180px, (min-width: 768px) 20vw, 42vw"
          quality={72}
          loading={priority ? undefined : "lazy"}
          decoding="async"
          className="object-contain object-center bg-white p-0.5 product-shot sm:p-1"
        />
      </div>
      <div className="flex flex-1 flex-col p-3 sm:p-3.5">
        <p
          className={cn(
            "w-fit rounded-full px-2 py-0.5 font-display text-[10px] font-black uppercase tracking-wide",
            accentChip[category.accent],
          )}
        >
          {typeof count === "number" ? `${count} items` : "Category"}
        </p>
        <h3 className="mt-1.5 font-display text-sm font-extrabold leading-snug text-ink-900 sm:text-base">
          {toTitleCase(category.shortName)}
        </h3>
        {mentioned.length ? (
          <p className="mt-1 line-clamp-2 text-[11px] leading-relaxed text-ink-500">
            {mentioned.map(toTitleCase).join(" · ")}
          </p>
        ) : null}
        <span className="mt-auto inline-flex items-center gap-1 pt-2 font-display text-[11px] font-black uppercase tracking-wide text-coral-600">
          Shop
          <ArrowRight className="h-3 w-3 transition-transform duration-300 group-hover:translate-x-0.5" />
        </span>
      </div>
    </Link>
  );
}
