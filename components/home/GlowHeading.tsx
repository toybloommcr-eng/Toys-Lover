import Link from "next/link";
import { ChevronLeft, ChevronRight } from "lucide-react";
import { cn } from "@/lib/utils";

export function GlowHeading({
  eyebrow,
  title,
  href,
  className,
}: {
  eyebrow?: string;
  title: string;
  href?: string;
  tone?: string;
  className?: string;
}) {
  const titleNode = (
    <h2 className="font-display text-3xl font-extrabold tracking-tight sm:text-4xl lg:text-[2.85rem]">
      <span className="heading-glow-coral">{title}</span>
    </h2>
  );

  return (
    <div className={cn("flex flex-col items-center text-center", className)}>
      {eyebrow ? (
        <p className="mb-2 text-xs font-black uppercase tracking-[0.2em] text-teal-600 sm:text-sm">
          {eyebrow}
        </p>
      ) : null}
      <div className="flex items-center gap-2 sm:gap-3">
        <ChevronLeft className="h-7 w-7 shrink-0 text-coral-400 sm:h-8 sm:w-8" aria-hidden />
        {href ? (
          <Link
            href={href}
            className="rounded-lg outline-none transition hover:opacity-90 focus-visible:ring-2 focus-visible:ring-coral-400"
          >
            {titleNode}
          </Link>
        ) : (
          titleNode
        )}
        <ChevronRight className="h-7 w-7 shrink-0 text-coral-400 sm:h-8 sm:w-8" aria-hidden />
      </div>
    </div>
  );
}
